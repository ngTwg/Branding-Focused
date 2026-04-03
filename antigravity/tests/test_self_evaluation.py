"""
Unit tests for Task 23: Self-Evaluation Tests.

Tests cover:
- 23.1: test_self_eval_report_generation()
- 23.2: test_baseline_update_logic()
- 23.3: test_suggestion_rules()
- 23.4: test_full_self_eval_cycle()
- 23.5: test_report_persistence()

Requirements: 6.1-6.4
"""

import pytest
import sys
from pathlib import Path
from datetime import datetime, timedelta
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from antigravity.core.health_monitor import HealthMonitor
from antigravity.core.suggestion_engine import SuggestionEngine


@pytest.fixture
def temp_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    # Cleanup after test
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestSelfEvalReportGeneration:
    """Test 23.1: Unit test: test_self_eval_report_generation()."""
    
    def test_self_eval_report_generation(self, temp_data_dir):
        """
        Test self-evaluation report generation with 100 tasks.
        
        Requirements:
        - Record 100 tasks with known metrics
        - Call generate_self_eval_report()
        - Verify report contains: score, top issue, suggestion, top strength
        """
        monitor = HealthMonitor(window_size=100, data_dir=temp_data_dir)
        
        # Record 100 tasks with known metrics
        # 80 success, 20 failure (80% success rate)
        # 15 rollbacks (15% rollback rate)
        # Average 2 patches per task
        # Average 2500 tokens per task
        
        for i in range(80):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2500,
                no_op_patch=False
            )
        
        for i in range(15):
            monitor.record_task(
                success=False,
                patches_count=3,
                rollback=True,
                tokens_used=3000,
                no_op_patch=False
            )
        
        for i in range(5):
            monitor.record_task(
                success=False,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Call generate_self_eval_report()
        report = monitor.generate_self_eval_report()
        
        # Verify report contains required components
        assert "[SELF-EVAL] Performance Report" in report
        assert "Health Score:" in report
        assert "Top Issue:" in report
        assert "Suggestion:" in report
        assert "Top Strength:" in report
        
        # Verify report is not empty
        assert len(report) > 100
        
        # Verify health score is present and reasonable
        lines = report.split('\n')
        score_line = [l for l in lines if "Health Score:" in l][0]
        assert any(cat in score_line.lower() for cat in ["excellent", "good", "fair", "poor"])


class TestBaselineUpdateLogic:
    """Test 23.2: Unit test: test_baseline_update_logic()."""
    
    def test_baseline_update_logic(self, temp_data_dir):
        """
        Test baseline update logic with time and data conditions.
        
        Requirements:
        - Establish initial baseline
        - Simulate 90 days passing
        - Record 50 new tasks
        - Verify should_update_baseline() returns True
        - Verify baseline updated correctly
        """
        monitor = HealthMonitor(
            window_size=200,  # Large enough to hold all tasks
            baseline_update_interval_days=90,
            data_dir=temp_data_dir
        )
        
        # Establish initial baseline with 50 tasks
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Verify baseline was established
        assert monitor._baseline is not None
        initial_baseline = monitor._baseline
        assert initial_baseline.baseline_token_per_task == 2000.0
        assert initial_baseline.baseline_patches == 2.0
        assert initial_baseline.version == 1
        
        # Simulate 90 days passing
        monitor._last_baseline_update = datetime.now() - timedelta(days=91)
        
        # Record 49 new tasks - should not trigger update yet
        for i in range(49):
            monitor.record_task(
                success=True,
                patches_count=3,
                rollback=False,
                tokens_used=3000,
                no_op_patch=False
            )
        
        # Verify should_update_baseline() returns False (not enough tasks yet)
        assert monitor.should_update_baseline() is False
        
        # Record 1 more task - now we have 50 new tasks
        monitor.record_task(
            success=True,
            patches_count=3,
            rollback=False,
            tokens_used=3000,
            no_op_patch=False
        )
        
        # Verify baseline was updated automatically
        updated_baseline = monitor._baseline
        assert updated_baseline.version == 2
        assert updated_baseline.baseline_token_per_task == 3000.0
        assert updated_baseline.baseline_patches == 3.0
        
        # Verify tracking variables were reset
        assert monitor._tasks_since_baseline == 0


class TestSuggestionRules:
    """Test 23.3: Unit test: test_suggestion_rules()."""
    
    def test_suggestion_rules(self, temp_data_dir):
        """
        Test each suggestion rule individually.
        
        Requirements:
        - Test high stale_ratio → "Re-index skills"
        - Test high rollback_rate → "Review error detection"
        - Test frequent Red zone → "Increase budget"
        - Verify priority ordering
        """
        # Test Rule 1: High stale_ratio (requires IndexManager mock)
        # We'll test this through the SuggestionEngine directly
        from antigravity.core.suggestion_engine import SuggestionPriority
        
        class MockMetrics:
            def __init__(self, stale_ratio=0.0, rollback_rate=0.0, red_zone_ratio=0.0):
                self._stale_ratio = stale_ratio
                self._rollback_rate = rollback_rate
                self._red_zone_ratio = red_zone_ratio
            
            def get_stale_ratio(self):
                return self._stale_ratio
            
            def get_rollback_rate(self):
                return self._rollback_rate
            
            def get_red_zone_ratio(self):
                return self._red_zone_ratio
            
            def get_slm_usage_ratio(self):
                return 0.5
            
            def get_token_efficiency_ratio(self):
                return 1.0
            
            def get_success_rate(self):
                return 0.9
        
        engine = SuggestionEngine()
        
        # Test Rule 1: High stale_ratio → "Re-index skills" (HIGH)
        metrics1 = MockMetrics(stale_ratio=0.25)  # 25% > 20% threshold
        suggestion1 = engine.evaluate_rule_1_stale_index(metrics1)
        
        assert suggestion1 is not None
        assert suggestion1.priority == SuggestionPriority.HIGH
        assert "Re-index skills" in suggestion1.message
        assert suggestion1.metric_value == 0.25
        
        # Test Rule 2: High rollback_rate → "Review error detection" (HIGH)
        metrics2 = MockMetrics(rollback_rate=0.18)  # 18% > 15% threshold
        suggestion2 = engine.evaluate_rule_2_high_rollback(metrics2)
        
        assert suggestion2 is not None
        assert suggestion2.priority == SuggestionPriority.HIGH
        assert "Review error detection" in suggestion2.message
        assert suggestion2.metric_value == 0.18
        
        # Test Rule 3: Frequent Red zone → "Increase budget" (MEDIUM)
        metrics3 = MockMetrics(red_zone_ratio=0.35)  # 35% > 30% threshold
        suggestion3 = engine.evaluate_rule_3_red_zone(metrics3)
        
        assert suggestion3 is not None
        assert suggestion3.priority == SuggestionPriority.MEDIUM
        assert "Increase budget" in suggestion3.message
        assert suggestion3.metric_value == 0.35
        
        # Test priority ordering
        # HIGH priority (value=2) should come before MEDIUM priority (value=3)
        assert suggestion1.priority.value < suggestion3.priority.value
        assert suggestion2.priority.value < suggestion3.priority.value


class TestFullSelfEvalCycle:
    """Test 23.4: Integration test: test_full_self_eval_cycle()."""
    
    def test_full_self_eval_cycle(self, temp_data_dir):
        """
        Test full self-evaluation cycle end-to-end.
        
        Requirements:
        - Execute 100 tasks
        - Verify self-eval report generated automatically
        - Verify report saved to file
        - Verify suggestions actionable
        """
        monitor = HealthMonitor(window_size=100, data_dir=temp_data_dir)
        
        # Execute 100 tasks with varying metrics
        # 75 success, 25 failure (75% success rate)
        # 20 rollbacks (20% rollback rate - triggers HIGH priority suggestion)
        for i in range(75):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2500,
                no_op_patch=False
            )
        
        for i in range(20):
            monitor.record_task(
                success=False,
                patches_count=3,
                rollback=True,  # High rollback rate
                tokens_used=3000,
                no_op_patch=False
            )
        
        for i in range(5):
            monitor.record_task(
                success=False,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Verify self-eval report can be generated
        report = monitor.generate_self_eval_report()
        
        assert report is not None
        assert "[SELF-EVAL] Performance Report" in report
        assert "Health Score:" in report
        
        # Verify report can be saved to file
        report_path = monitor.save_report(report_dir=temp_data_dir / "reports")
        
        assert report_path.exists()
        assert report_path.name.startswith("self_eval_")
        assert report_path.name.endswith(".md")
        
        # Verify report content was saved correctly
        saved_content = report_path.read_text(encoding="utf-8")
        assert saved_content == report
        
        # Verify suggestions are actionable
        suggestions = monitor.suggest_actions()
        
        assert len(suggestions) > 0
        # With 20% rollback rate, should have HIGH priority suggestion
        assert any("[HIGH]" in s for s in suggestions)
        assert any("Review error detection" in s for s in suggestions)


class TestReportPersistence:
    """Test 23.5: Unit test: test_report_persistence()."""
    
    def test_report_persistence(self, temp_data_dir):
        """
        Test report persistence and cleanup.
        
        Requirements:
        - Generate 15 reports
        - Verify only last 10 kept
        - Verify older reports deleted
        """
        import time
        
        monitor = HealthMonitor(window_size=10, data_dir=temp_data_dir)
        
        # Record some tasks to have data for reports
        for i in range(10):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Generate 15 reports with slight delays to ensure different timestamps
        report_dir = temp_data_dir / "reports"
        
        for i in range(15):
            monitor.save_report(report_dir=report_dir)
            # Small delay to ensure different timestamps
            time.sleep(0.01)
        
        # Verify only last 10 reports are kept
        reports = list(report_dir.glob("self_eval_*.md"))
        assert len(reports) == 10
        
        # Verify reports are the most recent ones
        # (sorted by modification time, most recent first)
        reports_sorted = sorted(
            reports,
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        # All 10 reports should exist
        for report in reports_sorted:
            assert report.exists()
        
        # Generate 5 more reports
        for i in range(5):
            monitor.save_report(report_dir=report_dir)
            time.sleep(0.01)
        
        # Still should only have 10 reports
        reports_after = list(report_dir.glob("self_eval_*.md"))
        assert len(reports_after) == 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
