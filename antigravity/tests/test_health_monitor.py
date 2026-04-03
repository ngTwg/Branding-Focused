"""
Unit tests for HealthMonitor (Phase 5: Health Monitoring).

Tests cover:
- Health score computation
- Derived metrics calculation
- Baseline establishment
- Anomaly detection
- Actionable suggestions
- Property-based tests for health score monotonicity

Requirements: 5.1-5.9
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta
from hypothesis import given, strategies as st
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from antigravity.core.health_monitor import (
    HealthMonitor,
    TaskMetrics,
    DerivedMetrics,
    BaselineMetrics
)


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    # Cleanup after test
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestHealthScoreComputation:
    """Test health score computation logic (Task 19.1)."""
    
    def test_health_score_with_good_metrics(self):
        """Test health score computation with good metrics."""
        monitor = HealthMonitor(window_size=10)
        
        # Record 10 tasks: 8 success, 2 rollback
        for i in range(8):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        for i in range(2):
            monitor.record_task(
                success=False,
                patches_count=2,
                rollback=True,
                tokens_used=2500,
                no_op_patch=False
            )
        
        # Compute health score
        score = monitor.compute_health_score()
        category = monitor.categorize_health(score)
        
        # Verify score is reasonable
        assert 0 <= score <= 100
        assert category in ["excellent", "good", "fair", "poor"]
        
        # With 80% success rate and 20% rollback rate, should be "good" or "excellent"
        assert category in ["good", "excellent"]
    
    def test_health_score_with_poor_metrics(self):
        """Test health score computation with poor metrics."""
        monitor = HealthMonitor(window_size=10)
        
        # Record 10 tasks: 3 success, 7 rollback (poor performance)
        for i in range(3):
            monitor.record_task(
                success=True,
                patches_count=3,
                rollback=False,
                tokens_used=5000,
                no_op_patch=False
            )
        
        for i in range(7):
            monitor.record_task(
                success=False,
                patches_count=5,
                rollback=True,
                tokens_used=6000,
                no_op_patch=False
            )
        
        # Compute health score
        score = monitor.compute_health_score()
        category = monitor.categorize_health(score)
        
        # With 30% success rate and 70% rollback rate, should be "poor" or "fair"
        assert category in ["poor", "fair"]
    
    def test_health_score_empty_history(self):
        """Test health score with no task history."""
        monitor = HealthMonitor(window_size=10)
        
        # Compute health score with empty history
        score = monitor.compute_health_score()
        
        # Should return optimistic default
        assert score == 100.0
        assert monitor.categorize_health(score) == "excellent"


class TestDerivedMetrics:
    """Test derived metrics computation (Task 19.2)."""
    
    def test_derived_metrics_computation(self):
        """Test derived metrics with known task history."""
        monitor = HealthMonitor(window_size=20)
        
        # Record 20 tasks with known metrics
        # 15 success, 5 failure
        # 3 rollbacks
        # 2 no-op patches
        for i in range(15):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        for i in range(3):
            monitor.record_task(
                success=False,
                patches_count=3,
                rollback=True,
                tokens_used=2500,
                no_op_patch=False
            )
        
        for i in range(2):
            monitor.record_task(
                success=False,
                patches_count=1,
                rollback=False,
                tokens_used=1500,
                no_op_patch=True
            )
        
        # Get derived metrics
        metrics = monitor.get_derived_metrics(window="all")
        
        # Verify metrics
        assert metrics.success_rate == 15 / 20  # 0.75
        assert metrics.rollback_rate == 3 / 20  # 0.15
        assert metrics.no_op_patch_rate == 2 / 20  # 0.10
        assert metrics.avg_patches_per_success == 30 / 15  # 2.0
        assert metrics.token_per_task == (15*2000 + 3*2500 + 2*1500) / 20  # 2025
    
    def test_derived_metrics_windows(self):
        """Test derived metrics with different time windows."""
        monitor = HealthMonitor(window_size=20)
        
        # Record tasks with timestamps
        now = datetime.now()
        
        # Add 10 old tasks (2 hours ago)
        for i in range(10):
            task = TaskMetrics(
                task_id=f"old_{i}",
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=1000,
                no_op_patch=False,
                timestamp=now - timedelta(hours=2)
            )
            monitor._task_history.append(task)
        
        # Add 10 recent tasks (now)
        for i in range(10):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Get metrics for different windows
        metrics_all = monitor.get_derived_metrics(window="all")
        metrics_last_hour = monitor.get_derived_metrics(window="last_hour")
        
        # All tasks should have avg 1.5 patches
        assert metrics_all.avg_patches_per_success == 30 / 20  # 1.5
        
        # Last hour should only have recent tasks (2 patches each)
        assert metrics_last_hour.avg_patches_per_success == 2.0
    
    def test_derived_metrics_empty_window(self):
        """Test derived metrics with empty window."""
        monitor = HealthMonitor(window_size=10)
        
        # Get metrics with no tasks
        metrics = monitor.get_derived_metrics(window="last_10")
        
        # Should return zero metrics
        assert metrics.success_rate == 0.0
        assert metrics.rollback_rate == 0.0
        assert metrics.no_op_patch_rate == 0.0
        assert metrics.avg_patches_per_success == 0.0
        assert metrics.token_per_task == 0.0


class TestBaselineEstablishment:
    """Test baseline establishment logic (Task 19.3)."""
    
    def test_baseline_establishment(self):
        """Test baseline establishment after 50 tasks."""
        monitor = HealthMonitor(window_size=100)
        
        # Record 50 tasks
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Baseline should be established automatically
        assert monitor._baseline is not None
        assert monitor._baseline.task_count == 50
        assert monitor._baseline.baseline_token_per_task == 2000
        assert monitor._baseline.baseline_patches == 2.0
        assert monitor._baseline.baseline_success_rate == 1.0
    
    def test_baseline_values_reasonable(self):
        """Test that baseline values are reasonable."""
        monitor = HealthMonitor(window_size=100)
        
        # Record 50 tasks with varying metrics
        for i in range(40):
            monitor.record_task(
                success=True,
                patches_count=1 + (i % 3),  # 1, 2, or 3 patches
                rollback=False,
                tokens_used=1500 + (i % 5) * 500,  # 1500-3500 tokens
                no_op_patch=False
            )
        
        for i in range(10):
            monitor.record_task(
                success=False,
                patches_count=4,
                rollback=True,
                tokens_used=4000,
                no_op_patch=False
            )
        
        # Check baseline
        assert monitor._baseline is not None
        assert monitor._baseline.baseline_token_per_task > 0
        assert monitor._baseline.baseline_patches > 0
        assert 0 <= monitor._baseline.baseline_success_rate <= 1.0


class TestAnomalyDetection:
    """Test anomaly detection logic (Task 19.4)."""
    
    def test_success_rate_drop_anomaly(self, temp_data_dir):
        """Test anomaly detection for success rate drop."""
        monitor = HealthMonitor(window_size=100, data_dir=temp_data_dir)
        
        # Establish baseline with 90% success rate
        for i in range(45):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        for i in range(5):
            monitor.record_task(
                success=False,
                patches_count=3,
                rollback=True,
                tokens_used=2500,
                no_op_patch=False
            )
        
        # Baseline should be established
        assert monitor._baseline is not None
        baseline_success = monitor._baseline.baseline_success_rate
        assert baseline_success == 0.9
        
        # Now record new tasks with 60% success rate (30% drop)
        for i in range(6):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        for i in range(4):
            monitor.record_task(
                success=False,
                patches_count=3,
                rollback=True,
                tokens_used=2500,
                no_op_patch=False
            )
        
        # Detect anomalies
        anomalies = monitor.detect_anomalies()
        
        # Should detect success rate drop
        assert len(anomalies) > 0
        assert any("Success rate dropped" in a for a in anomalies)
    
    def test_token_usage_spike_anomaly(self, temp_data_dir):
        """Test anomaly detection for token usage spike."""
        monitor = HealthMonitor(window_size=100, data_dir=temp_data_dir)
        
        # Establish baseline with 2000 tokens/task
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Now record tasks with 4000 tokens/task (100% increase)
        for i in range(10):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=4000,
                no_op_patch=False
            )
        
        # Detect anomalies
        anomalies = monitor.detect_anomalies()
        
        # Should detect token usage spike
        assert len(anomalies) > 0
        assert any("Token usage increased" in a for a in anomalies)


class TestActionableSuggestions:
    """Test actionable suggestions logic (Task 19.5)."""
    
    def test_high_rollback_suggestion(self):
        """Test suggestion for high rollback rate."""
        monitor = HealthMonitor(window_size=10)
        
        # Record tasks with high rollback rate (>15%)
        for i in range(8):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        for i in range(2):
            monitor.record_task(
                success=False,
                patches_count=2,
                rollback=True,
                tokens_used=2500,
                no_op_patch=False
            )
        
        # Get suggestions
        suggestions = monitor.suggest_actions()
        
        # Should suggest reviewing error detection
        assert len(suggestions) > 0
        assert any("Review error detection" in s for s in suggestions)
    
    def test_high_token_usage_suggestion(self):
        """Test suggestion for high token usage."""
        monitor = HealthMonitor(window_size=100)
        
        # Establish baseline with 2000 tokens/task
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Record tasks with high token usage (>baseline*1.5)
        for i in range(10):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=3500,
                no_op_patch=False
            )
        
        # Get suggestions
        suggestions = monitor.suggest_actions()
        
        # Should suggest optimizing prompt length
        assert len(suggestions) > 0
        assert any("Optimize prompt" in s for s in suggestions)


class TestHealthScoreMonotonicity:
    """Property-based tests for health score (Task 19.7)."""
    
    @given(success_rate=st.floats(min_value=0.0, max_value=1.0))
    def test_higher_success_rate_higher_score(self, success_rate):
        """Test that higher success rate leads to higher health score."""
        monitor1 = HealthMonitor(window_size=10)
        monitor2 = HealthMonitor(window_size=10)
        
        # Record tasks with success_rate for monitor1
        success_count1 = int(success_rate * 10)
        for i in range(success_count1):
            monitor1.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        for i in range(10 - success_count1):
            monitor1.record_task(
                success=False,
                patches_count=2,
                rollback=True,
                tokens_used=2500,
                no_op_patch=False
            )
        
        # Record tasks with higher success_rate for monitor2
        higher_success_rate = min(1.0, success_rate + 0.2)
        success_count2 = int(higher_success_rate * 10)
        for i in range(success_count2):
            monitor2.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        for i in range(10 - success_count2):
            monitor2.record_task(
                success=False,
                patches_count=2,
                rollback=True,
                tokens_used=2500,
                no_op_patch=False
            )
        
        # Compute scores
        score1 = monitor1.compute_health_score()
        score2 = monitor2.compute_health_score()
        
        # Higher success rate should lead to higher or equal score
        if success_count2 > success_count1:
            assert score2 >= score1
    
    @given(success_rate=st.floats(min_value=0.0, max_value=1.0))
    def test_health_score_in_range(self, success_rate):
        """Test that health score is always in [0, 100] range."""
        monitor = HealthMonitor(window_size=10)
        
        # Record tasks with given success_rate
        success_count = int(success_rate * 10)
        for i in range(success_count):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        for i in range(10 - success_count):
            monitor.record_task(
                success=False,
                patches_count=5,
                rollback=True,
                tokens_used=5000,
                no_op_patch=False
            )
        
        # Compute score
        score = monitor.compute_health_score()
        
        # Score must be in [0, 100]
        assert 0 <= score <= 100
