"""
Integration test for full Orchestrator execution loop.

Feature: antigravity-architecture-upgrade
Validates: Requirements 1.6, 2.6, 4.2
"""

from unittest.mock import MagicMock, patch

from antigravity.scripts.orchestrator import AntigravityOrchestrator as Orchestrator


class TestOrchestratorFullLoop:
    """Integration tests for complete execution flow."""

    def test_full_execution_loop(self):
        """
        Test complete execution: route → plan → execute → check → complete.
        
        Validates: Requirements 1.6, 2.6, 4.2
        """
        with patch("antigravity.scripts.orchestrator.SLMRouter") as mock_slm_class, \
             patch("antigravity.scripts.orchestrator.HybridRetriever") as mock_retriever_class, \
             patch("antigravity.scripts.orchestrator.BackupManager") as mock_backup_class, \
             patch("antigravity.scripts.orchestrator.DeterministicChecker") as mock_checker_class, \
             patch("antigravity.scripts.orchestrator.TracingService") as mock_tracer_class, \
             patch("antigravity.scripts.orchestrator.LLMClient") as mock_llm_class:

            # Setup mocks
            mock_slm = MagicMock()
            mock_retriever = MagicMock()
            mock_backup = MagicMock()
            mock_checker = MagicMock()
            mock_tracer = MagicMock()
            mock_llm = MagicMock()

            mock_slm_class.return_value = mock_slm
            mock_retriever_class.return_value = mock_retriever
            mock_backup_class.return_value = mock_backup
            mock_checker_class.return_value = mock_checker
            mock_tracer_class.return_value = mock_tracer
            mock_llm_class.return_value = mock_llm

            # Mock SLM routing
            from antigravity.core.schemas import SLMRouteDecision
            mock_slm.classify.return_value = SLMRouteDecision(
                chosen="implement",
                confidence=0.92,
                top_k=[("implement", 0.92), ("debug", 0.75)],
            )

            # Mock skill retrieval
            from antigravity.core.schemas import RankedSkill
            mock_retriever.retrieve.return_value = [
                RankedSkill(
                    skill_id="backend-api",
                    content="REST API design patterns",
                    domain_tags=["backend"],
                    tier=2,
                    final_score=0.85,
                    bm25_norm=0.8,
                    cosine_norm=0.9,
                )
            ]

            # Mock checker (no errors)
            from antigravity.core.schemas import ErrorDelta
            mock_checker.examine.return_value = ErrorDelta(
                old_errors=[],
                new_errors=[],
                net_improvement=True,
                old_error_score=0,
                new_error_score=0,
            )

            # Create orchestrator
            orchestrator = Orchestrator(config={})

            # Execute task
            result = orchestrator.execute(task="Create a REST API endpoint")

            # Assert: SLM Router was called
            assert mock_slm.classify.called, "SLM Router not called"

            # Assert: Skills were retrieved
            assert mock_retriever.retrieve.called, "HybridRetriever not called"

            # Assert: Backup was created
            assert mock_backup.create_backup.called, "Backup not created"

            # Assert: ErrorDelta was computed
            assert mock_checker.examine.called, "Checker not called"

            # Assert: Trace was flushed
            assert mock_tracer.flush.called, "Trace not flushed"

            # Assert: All components wired correctly
            assert result is not None, "Execution returned None"
