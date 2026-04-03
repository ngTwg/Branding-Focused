"""
Integration test for Orchestrator budget enforcement.

Feature: antigravity-architecture-upgrade
Validates: Requirements 7.7
"""

import pytest
from unittest.mock import MagicMock, patch

from antigravity.core.budget_guard import BudgetExceededError
from antigravity.scripts.orchestrator import AntigravityOrchestrator as Orchestrator


class TestOrchestratorBudget:
    """Integration tests for budget termination before LLM calls."""

    def test_budget_terminates_before_llm_call(self):
        """
        Budget should terminate execution before making LLM call when limit exceeded.
        
        Validates: Requirements 7.7
        """
        with patch("antigravity.scripts.orchestrator.LLMClient") as mock_llm_class:
            mock_llm = MagicMock()
            mock_llm_class.return_value = mock_llm

            # Create orchestrator with tight budget
            orchestrator = Orchestrator(
                config={
                    "max_tokens": 5000,
                    "max_steps": 100,
                    "max_repair_attempts": 5,
                }
            )

            # Simulate 4500 tokens already used
            orchestrator.budget_guard.record_call(4500)

            # Attempt task requiring 1000 tokens (would exceed 5000 limit)
            with pytest.raises(BudgetExceededError) as exc_info:
                orchestrator.execute(
                    task="Implement a simple function",
                    estimated_input_tokens=500,
                    max_output_tokens=500,
                )

            # Assert: BudgetExceededError raised
            assert "tokens" in exc_info.value.termination_reason.lower()

            # Assert: LLM was NOT called
            assert not mock_llm.generate_structured.called, (
                "LLM was called despite budget exceeded"
            )
            assert not mock_llm.generate_text.called, (
                "LLM was called despite budget exceeded"
            )
