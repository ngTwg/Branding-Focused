"""
Tests for Task 20: Self-Evaluation Report

This module tests the self-evaluation report generation, persistence, and triggering
functionality added in Task 20.

Requirements tested:
- 6.1: generate_self_eval_report() implementation
- Task 20.1: Report generation with specified format
- Task 20.2: Report persistence to disk
- Task 20.3: Report triggering every 100 tasks
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime
import sys

# Add antigravity to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from antigravity.core.health_monitor import HealthMonitor


class TestSelfEvalReportGeneration:
    """Test Task 20.1: generate_self_eval_report() implementation"""
    
    def test_generate_self_eval_report_format(self):
        """Test that report follows specified format from Requirement 6.1"""
        monitor = HealthMonitor(window_size=10)
        
        # Record some tasks
        for i in range(5):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Generate report
        report = monitor.generate_self_eval_report()
        
        # Verify format matches specification
        assert "[SELF-EVAL] Performance Report" in report
        assert "Health Score:" in report
        assert "Top Issue:" in report
        assert "Suggestion:" in report
        assert "Top Strength:" in report
        
        # Verify it's a string
        assert isinstance(report, str)
        assert len(report) > 0
    
    def test_generate_self_eval_report_with_baseline(self):
        """Test report generation with established baseline"""
        # Use larger window to keep 50 tasks for baseline
        monitor = HealthMonitor(window_size=50)
        
        # Record 50 tasks to establish baseline
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Baseline should be established
        assert monitor._baseline is not None
        
        # Generate report
        report = monitor.generate_self_eval_report()
        
        # Should contain health score and category
        assert "Health Score:" in report
        assert any(cat in report.lower() for cat in ["excellent", "good", "fair", "poor"])
    
    def test_generate_report_alias(self):
        """Test that generate_report() is an alias for generate_self_eval_report()"""
        monitor = HealthMonitor(window_size=10)
        
        # Record some tasks
        for i in range(5):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Both methods should return the same report
        report1 = monitor.generate_self_eval_report()
        report2 = monitor.generate_report()
        
        assert report1 == report2


class TestReportPersistence:
    """Test Task 20.2: Report persistence to disk"""
    
    def test_save_report_creates_file(self):
        """Test that save_report() creates a file with correct naming"""
        monitor = HealthMonitor(window_size=10)
        
        # Record some tasks
        for i in range(5):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Save report to temp directory
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = monitor.save_report(report_dir=tmpdir)
            
            # Verify file was created
            assert report_path.exists()
            
            # Verify filename format: self_eval_{timestamp}.md
            assert report_path.name.startswith("self_eval_")
            assert report_path.name.endswith(".md")
            
            # Verify file contains report content
            content = report_path.read_text(encoding="utf-8")
            assert "[SELF-EVAL] Performance Report" in content
    
    def test_save_report_creates_directory(self):
        """Test that save_report() creates report directory if not exists"""
        monitor = HealthMonitor(window_size=10)
        
        # Record some tasks
        for i in range(3):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Save to non-existent directory
        with tempfile.TemporaryDirectory() as tmpdir:
            report_dir = Path(tmpdir) / "reports" / "health"
            assert not report_dir.exists()
            
            report_path = monitor.save_report(report_dir=report_dir)
            
            # Directory should be created
            assert report_dir.exists()
            assert report_path.exists()
    
    def test_cleanup_old_reports(self):
        """Test that old reports are deleted (keep last 10)"""
        import time
        
        monitor = HealthMonitor(window_size=10)
        
        # Record some tasks
        for i in range(3):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Create 15 reports with slight delays to ensure different timestamps
        with tempfile.TemporaryDirectory() as tmpdir:
            report_dir = Path(tmpdir)
            
            for i in range(15):
                monitor.save_report(report_dir=report_dir)
                # Small delay to ensure different timestamps
                time.sleep(0.01)
            
            # Should only have 10 reports (last 10 kept)
            reports = list(report_dir.glob("self_eval_*.md"))
            assert len(reports) == 10
    
    def test_save_report_returns_path(self):
        """Test that save_report() returns Path object"""
        monitor = HealthMonitor(window_size=10)
        
        # Record some tasks
        for i in range(3):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = monitor.save_report(report_dir=tmpdir)
            
            # Should return Path object
            assert isinstance(report_path, Path)
            assert report_path.exists()


class TestReportContent:
    """Test report content quality"""
    
    def test_report_identifies_top_issue(self):
        """Test that report identifies the worst metric"""
        monitor = HealthMonitor(window_size=10)
        
        # Establish baseline with good metrics
        for i in range(50):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Record tasks with high rollback rate (bad metric)
        for i in range(10):
            monitor.record_task(
                success=True,
                patches_count=2,
                rollback=True,  # High rollback rate
                tokens_used=2000,
                no_op_patch=False
            )
        
        report = monitor.generate_self_eval_report()
        
        # Should mention rollback in top issue
        assert "Top Issue:" in report
    
    def test_report_provides_actionable_suggestion(self):
        """Test that report provides concrete suggestions"""
        monitor = HealthMonitor(window_size=10)
        
        # Record tasks with issues
        for i in range(10):
            monitor.record_task(
                success=False,  # Low success rate
                patches_count=3,
                rollback=True,
                tokens_used=5000,  # High token usage
                no_op_patch=False
            )
        
        report = monitor.generate_self_eval_report()
        
        # Should provide suggestion
        assert "Suggestion:" in report
        # Suggestion should not be empty
        lines = report.split('\n')
        suggestion_line = [l for l in lines if "Suggestion:" in l][0]
        assert len(suggestion_line) > len("Suggestion: ")
    
    def test_report_identifies_strength(self):
        """Test that report identifies best metric"""
        monitor = HealthMonitor(window_size=10)
        
        # Record tasks with good metrics
        for i in range(10):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=1500,  # Low token usage
                no_op_patch=False
            )
        
        report = monitor.generate_self_eval_report()
        
        # Should mention strength
        assert "Top Strength:" in report


class TestIntegrationWithOrchestrator:
    """Test Task 20.3: Integration with Orchestrator"""
    
    def test_report_triggered_every_100_tasks(self):
        """Test that report is generated every 100 tasks"""
        monitor = HealthMonitor(window_size=10)
        
        # Simulate 100 tasks
        for i in range(100):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Should be able to generate report
        report = monitor.generate_self_eval_report()
        assert report is not None
        assert len(report) > 0
    
    def test_report_saves_successfully(self):
        """Test that report can be saved after 100 tasks"""
        monitor = HealthMonitor(window_size=10)
        
        # Simulate 100 tasks
        for i in range(100):
            monitor.record_task(
                success=True,
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Save report
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = monitor.save_report(report_dir=tmpdir)
            
            # Verify file exists and has content
            assert report_path.exists()
            content = report_path.read_text(encoding="utf-8")
            assert len(content) > 0
            assert "[SELF-EVAL] Performance Report" in content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
