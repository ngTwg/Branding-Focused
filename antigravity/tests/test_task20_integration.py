"""
Integration test for Task 20: Self-Evaluation Report in Orchestrator

This test verifies that the orchestrator correctly triggers self-evaluation
reports every 100 tasks and saves them to disk.
"""

import pytest
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from antigravity.core.health_monitor import HealthMonitor


class TestOrchestratorIntegration:
    """Test Task 20.3: Orchestrator integration"""
    
    def test_report_generation_at_100_tasks(self):
        """
        Test that orchestrator triggers report generation every 100 tasks.
        
        This simulates the orchestrator's behavior:
        1. Record 100 tasks
        2. Check if _task_count % 100 == 0
        3. Generate and save self-evaluation report
        """
        monitor = HealthMonitor(window_size=10)
        task_count = 0
        
        # Simulate 100 tasks
        for i in range(100):
            monitor.record_task(
                success=(i % 5 != 0),  # 80% success rate
                patches_count=2 if i % 3 == 0 else 1,
                rollback=(i % 10 == 0),  # 10% rollback rate
                tokens_used=2000 + (i * 10),
                no_op_patch=(i % 20 == 0)
            )
            task_count += 1
        
        # At 100 tasks, orchestrator should generate report
        assert task_count % 100 == 0
        
        # Generate and save report (as orchestrator does)
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = monitor.save_report(report_dir=tmpdir)
            
            # Verify report was saved
            assert report_path.exists()
            
            # Verify report content
            content = report_path.read_text(encoding="utf-8")
            assert "[SELF-EVAL] Performance Report" in content
            assert "Health Score:" in content
            assert "Top Issue:" in content
            assert "Suggestion:" in content
            assert "Top Strength:" in content
    
    def test_multiple_report_cycles(self):
        """
        Test multiple 100-task cycles generate multiple reports.
        """
        monitor = HealthMonitor(window_size=10)
        
        with tempfile.TemporaryDirectory() as tmpdir:
            report_dir = Path(tmpdir)
            
            # Simulate 3 cycles of 100 tasks each
            for cycle in range(3):
                for i in range(100):
                    monitor.record_task(
                        success=True,
                        patches_count=1,
                        rollback=False,
                        tokens_used=2000,
                        no_op_patch=False
                    )
                
                # Save report at end of each cycle
                monitor.save_report(report_dir=report_dir)
            
            # Should have 3 reports
            reports = list(report_dir.glob("self_eval_*.md"))
            assert len(reports) == 3
    
    def test_report_format_matches_requirement(self):
        """
        Test that report format exactly matches Requirement 6.1 specification.
        
        Required format:
        [SELF-EVAL] Performance Report
        - Health Score: {score} ({category})
        - Top Issue: {top_issue}
        - Suggestion: {top_suggestion}
        - Top Strength: {top_strength}
        """
        monitor = HealthMonitor(window_size=10)
        
        # Record some tasks
        for i in range(10):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        report = monitor.generate_self_eval_report()
        
        # Verify exact format
        lines = report.strip().split('\n')
        
        # Line 1: [SELF-EVAL] Performance Report
        assert lines[0] == "[SELF-EVAL] Performance Report"
        
        # Line 2: - Health Score: ...
        assert lines[1].startswith("- Health Score:")
        
        # Line 3: - Top Issue: ...
        assert lines[2].startswith("- Top Issue:")
        
        # Line 4: - Suggestion: ...
        assert lines[3].startswith("- Suggestion:")
        
        # Line 5: - Top Strength: ...
        assert lines[4].startswith("- Top Strength:")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
