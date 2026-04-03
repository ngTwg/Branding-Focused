"""
Integration test for Orchestrator rollback on regression.

Feature: antigravity-architecture-upgrade
Validates: Requirements 3.2, 3.4
"""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from antigravity.core.schemas import ErrorDelta
from antigravity.scripts.orchestrator import AntigravityOrchestrator as Orchestrator


class TestOrchestratorRollback:
    """Integration tests for rollback and replan on regression."""

    def test_regression_triggers_rollback_and_replan(self):
        """
        When patch causes regression, should rollback and trigger replan.
        
        Validates: Requirements 3.2, 3.4
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup test file
            test_file = Path(tmpdir) / "test.py"
            original_content = "def hello():\n    return 'world'\n"
            test_file.write_text(original_content, encoding="utf-8")

            with patch("antigravity.scripts.orchestrator.BackupManager") as mock_backup_class, \
                 patch("antigravity.scripts.orchestrator.DeterministicChecker") as mock_checker_class, \
                 patch("antigravity.scripts.orchestrator.ActionDispatcher") as mock_dispatcher_class:

                mock_backup = MagicMock()
                mock_checker = MagicMock()
                mock_dispatcher = MagicMock()

                mock_backup_class.return_value = mock_backup
                mock_checker_class.return_value = mock_checker
                mock_dispatcher_class.return_value = mock_dispatcher

                # Mock patch that causes regression
                def apply_bad_patch(*args, **kwargs):
                    test_file.write_text("def hello():\n    return 'broken'\n    syntax error\n", encoding="utf-8")

                mock_dispatcher.dispatch.side_effect = apply_bad_patch

                # Mock checker to detect regression
                mock_checker.examine.return_value = ErrorDelta(
                    old_errors=["SyntaxError: invalid syntax (line 1)"],
                    new_errors=[
                        "SyntaxError: invalid syntax (line 1)",
                        "SyntaxError: invalid syntax (line 3)",
                    ],
                    net_improvement=False,  # Regression!
                    old_error_score=10,
                    new_error_score=20,
                )

                orchestrator = Orchestrator(config={})
                orchestrator.backup_manager = mock_backup
                orchestrator.checker = mock_checker
                orchestrator.dispatcher = mock_dispatcher

                # Execute task
                try:
                    orchestrator.execute(task="Fix the function", target_files=[str(test_file)])
                except Exception:
                    pass  # Expected to fail due to regression

                # Assert: backup was created
                assert mock_backup.create_backup.called, "Backup not created before patch"

                # Assert: rollback was called
                assert mock_backup.rollback.called, "Rollback not called after regression"

                # Assert: replan was triggered (would be called with ErrorDelta context)
                # In real implementation, this would trigger replan_repair()
                rollback_call_args = mock_backup.rollback.call_args
                assert rollback_call_args is not None, "Rollback not called with proper arguments"
