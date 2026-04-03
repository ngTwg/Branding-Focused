"""
Unit tests for Task 21: Performance Baseline Update.

Tests cover:
- Baseline update interval logic
- Automatic baseline updates
- Baseline persistence (save/load)
- Baseline versioning

Requirements: 6.4 (Task 21.1-21.5)
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta
import tempfile
import shutil
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from antigravity.core.health_monitor import (
    HealthMonitor,
    BaselineMetrics
)


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    # Cleanup after test
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestBaselineUpdateLogic:
    """Test baseline update logic (Task 21.1, 21.2)."""
    
    def test_baseline_update_interval_initialization(self, temp_data_dir):
        """Test that baseline update interval is initialized correctly."""
        monitor = HealthMonitor(
            window_size=100,
            baseline_update_interval_days=90,
            data_dir=temp_data_dir
        )
        
        # Check interval is set correctly
        assert monitor._baseline_update_interval == timedelta(days=90)
        assert monitor._last_baseline_update is None
        assert monitor._tasks_since_baseline == 0
    
    def test_should_update_baseline_no_baseline(self, temp_data_dir):
        """Test should_update_baseline returns False when no baseline exists."""
        monitor = HealthMonitor(window_size=100, data_dir=temp_data_dir)
        
        # Should return False if no baseline
        assert monitor.should_update_baseline() is False
    
    def test_should_update_baseline_time_condition(self, temp_data_dir):
        """Test should_update_baseline checks time condition."""
        monitor = HealthMonitor(
            window_size=200,  # Larger window to hold all tasks
            baseline_update_interval_days=90,
            data_dir=temp_data_dir
        )
        
        # Establish baseline
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        assert monitor._baseline is not None
        
        # Just established - should not update yet
        assert monitor.should_update_baseline() is False
        
        # Simulate 91 days passing
        monitor._last_baseline_update = datetime.now() - timedelta(days=91)
        
        # Still need 50 successful tasks
        assert monitor.should_update_baseline() is False
        
        # Add 49 more successful tasks - should not trigger yet
        for i in range(49):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Should not update yet (only 49 tasks since baseline)
        assert monitor.should_update_baseline() is False
        
        # Add 1 more task - now we have 50
        monitor.record_task(
            success=True,
            patches_count=2,
            rollback=False,
            tokens_used=2000,
            no_op_patch=False
        )
        
        # Now both conditions met (but automatic update already happened in record_task)
        # So we need to check that it was updated
        assert monitor._baseline.version == 2  # Was automatically updated
    
    def test_should_update_baseline_data_condition(self, temp_data_dir):
        """Test should_update_baseline checks data condition (50 tasks)."""
        monitor = HealthMonitor(
            window_size=100,
            baseline_update_interval_days=90,
            data_dir=temp_data_dir
        )
        
        # Establish baseline
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Simulate time passing
        monitor._last_baseline_update = datetime.now() - timedelta(days=91)
        
        # Only 0 tasks since baseline - should not update
        assert monitor._tasks_since_baseline == 0
        assert monitor.should_update_baseline() is False


class TestBaselineUpdate:
    """Test baseline update functionality (Task 21.3)."""
    
    def test_update_baseline_recomputes_metrics(self, temp_data_dir):
        """Test that update_baseline recomputes metrics correctly."""
        monitor = HealthMonitor(window_size=200, data_dir=temp_data_dir)
        
        # Establish initial baseline with 2000 tokens/task
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        old_baseline = monitor._baseline
        assert old_baseline.baseline_token_per_task == 2000.0
        assert old_baseline.version == 1
        
        # Simulate time passing and add new tasks with 3000 tokens/task
        monitor._last_baseline_update = datetime.now() - timedelta(days=91)
        
        # Add 50 tasks with 3000 tokens (so last 50 successful will be all 3000)
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=3,
                rollback=False,
                tokens_used=3000,
                no_op_patch=False
            )
        
        # Check new baseline (automatic update should have happened)
        new_baseline = monitor._baseline
        assert new_baseline.baseline_token_per_task == 3000.0
        assert new_baseline.baseline_patches == 3.0
        assert new_baseline.version == 2  # Version incremented
    
    def test_update_baseline_insufficient_data(self, temp_data_dir):
        """Test update_baseline handles insufficient data gracefully."""
        monitor = HealthMonitor(window_size=200, data_dir=temp_data_dir)
        
        # Establish baseline
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        old_baseline = monitor._baseline
        old_version = old_baseline.version
        
        # Try to update with only 10 successful tasks
        monitor._last_baseline_update = datetime.now() - timedelta(days=91)
        
        for i in range(10):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Manually call update_baseline (should not update due to insufficient data)
        monitor.update_baseline()
        
        # Baseline version should be unchanged (update was rejected)
        # Note: The baseline object itself may have changed due to automatic update
        # being triggered, but if we only have 10 tasks, update should be rejected
        # Actually, with window_size=200, we still have the original 50 tasks in history
        # So the update will succeed. Let me adjust the test.
        
        # Clear most of the history to simulate insufficient data
        # We need to test the case where update_baseline is called but there aren't
        # enough successful tasks in the deque
        monitor2 = HealthMonitor(window_size=20, data_dir=temp_data_dir)
        
        # Add only 10 successful tasks
        for i in range(10):
            monitor2.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Try to update (should fail - not enough tasks)
        monitor2._baseline = BaselineMetrics(
            baseline_token_per_task=2000.0,
            baseline_patches=2.0,
            baseline_success_rate=1.0,
            established_at=datetime.now(),
            task_count=50,
            version=1
        )
        monitor2._last_baseline_update = datetime.now()
        
        old_version2 = monitor2._baseline.version
        monitor2.update_baseline()
        
        # Version should be unchanged (update rejected)
        assert monitor2._baseline.version == old_version2


class TestAutomaticBaselineUpdate:
    """Test automatic baseline updates (Task 21.4)."""
    
    def test_automatic_update_triggered(self, temp_data_dir):
        """Test that baseline updates automatically when conditions are met."""
        monitor = HealthMonitor(
            window_size=100,
            baseline_update_interval_days=90,
            data_dir=temp_data_dir
        )
        
        # Establish initial baseline
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        initial_version = monitor._baseline.version
        
        # Simulate time passing
        monitor._last_baseline_update = datetime.now() - timedelta(days=91)
        
        # Add 49 tasks - should not trigger update yet
        for i in range(49):
            monitor.record_task(
                success=True,
                patches_count=3,
                rollback=False,
                tokens_used=3000,
                no_op_patch=False
            )
        
        assert monitor._baseline.version == initial_version
        
        # Add 1 more task - should trigger automatic update
        monitor.record_task(
            success=True,
            patches_count=3,
            rollback=False,
            tokens_used=3000,
            no_op_patch=False
        )
        
        # Baseline should be updated
        assert monitor._baseline.version == initial_version + 1
        assert monitor._baseline.baseline_token_per_task == 3000.0


class TestBaselinePersistence:
    """Test baseline persistence (Task 21.5)."""
    
    def test_baseline_save_and_load(self, temp_data_dir):
        """Test that baseline is saved to and loaded from disk."""
        # Create monitor and establish baseline
        monitor1 = HealthMonitor(window_size=100, data_dir=temp_data_dir)
        
        for i in range(50):
            monitor1.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        baseline1 = monitor1._baseline
        
        # Check that baseline.json was created
        baseline_path = temp_data_dir / "baseline.json"
        assert baseline_path.exists()
        
        # Create new monitor with same data_dir - should load baseline
        monitor2 = HealthMonitor(window_size=100, data_dir=temp_data_dir)
        
        baseline2 = monitor2._baseline
        
        # Check that baseline was loaded correctly
        assert baseline2 is not None
        assert baseline2.baseline_token_per_task == baseline1.baseline_token_per_task
        assert baseline2.baseline_patches == baseline1.baseline_patches
        assert baseline2.baseline_success_rate == baseline1.baseline_success_rate
        assert baseline2.version == baseline1.version
    
    def test_baseline_json_format(self, temp_data_dir):
        """Test that baseline.json has correct format with metadata."""
        monitor = HealthMonitor(window_size=100, data_dir=temp_data_dir)
        
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Read baseline.json
        baseline_path = temp_data_dir / "baseline.json"
        with open(baseline_path, 'r') as f:
            baseline_data = json.load(f)
        
        # Check required fields
        assert "baseline_token_per_task" in baseline_data
        assert "baseline_patches" in baseline_data
        assert "baseline_success_rate" in baseline_data
        assert "established_at" in baseline_data
        assert "task_count" in baseline_data
        assert "version" in baseline_data
        
        # Check values
        assert baseline_data["task_count"] == 50
        assert baseline_data["version"] == 1
    
    def test_baseline_persistence_across_updates(self, temp_data_dir):
        """Test that baseline updates are persisted correctly."""
        monitor = HealthMonitor(
            window_size=100,
            baseline_update_interval_days=90,
            data_dir=temp_data_dir
        )
        
        # Establish initial baseline
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Simulate time passing and update baseline
        monitor._last_baseline_update = datetime.now() - timedelta(days=91)
        
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=3,
                rollback=False,
                tokens_used=3000,
                no_op_patch=False
            )
        
        # Baseline should be version 2 now
        assert monitor._baseline.version == 2
        
        # Create new monitor - should load version 2
        monitor2 = HealthMonitor(window_size=100, data_dir=temp_data_dir)
        
        assert monitor2._baseline.version == 2
        assert monitor2._baseline.baseline_token_per_task == 3000.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
