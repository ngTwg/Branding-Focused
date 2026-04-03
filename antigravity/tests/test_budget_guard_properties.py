"""
Property-based tests for BudgetGuard.

Feature: antigravity-architecture-upgrade
Validates: Requirements 7.2, 7.3, 7.7
"""

import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

from antigravity.core.budget_guard import BudgetExceededError, BudgetGuard


class TestBudgetGuardProperties:
    """Property tests for budget enforcement and tracking."""

    @given(
        tokens_used=st.integers(0, 90000),
        estimated_input=st.integers(1000, 5000),
        max_output=st.integers(1000, 5000),
    )
    @settings(max_examples=100)
    def test_budget_pre_call_enforcement(self, tokens_used, estimated_input, max_output):
        """
        Property 17: Budget Pre-Call Enforcement.
        
        Validates: Requirements 7.7
        
        check_pre_call() must raise BudgetExceededError when estimated cost exceeds remaining budget.
        """
        max_tokens = 100000
        guard = BudgetGuard(max_steps=1000, max_tokens=max_tokens, max_repair_attempts=10)

        # Record tokens used
        for _ in range(tokens_used // 1000):
            guard.record_call(1000)
        guard.record_call(tokens_used % 1000)

        # Check if we should exceed
        total_estimated = tokens_used + estimated_input + max_output
        should_exceed = total_estimated > max_tokens

        if should_exceed:
            with pytest.raises(BudgetExceededError) as exc_info:
                guard.check_pre_call(estimated_input, max_output)
            assert "tokens" in exc_info.value.termination_reason.lower()
        else:
            # Should not raise
            guard.check_pre_call(estimated_input, max_output)

    @given(limit_type=st.sampled_from(["steps", "tokens", "repairs"]))
    @settings(max_examples=30)
    def test_budget_termination_with_reason(self, limit_type):
        """
        Property 18: Budget Termination với Reason.
        
        Validates: Requirements 7.2
        
        When a limit is exceeded, termination_reason must indicate which dimension.
        """
        guard = BudgetGuard(max_steps=5, max_tokens=10000, max_repair_attempts=3)

        # Exceed the specified limit
        if limit_type == "steps":
            for _ in range(6):
                guard.record_step()
        elif limit_type == "tokens":
            for _ in range(11):
                guard.record_call(1000)
        elif limit_type == "repairs":
            for _ in range(4):
                guard.record_repair()

        status = guard.get_status()

        # Assert: termination_reason contains the exceeded dimension
        assert limit_type in status.termination_reason.lower(), (
            f"Expected '{limit_type}' in termination_reason, got: {status.termination_reason}"
        )

    @given(token_counts=st.lists(st.integers(100, 1000), min_size=2, max_size=20))
    @settings(max_examples=100)
    def test_token_accumulation_additivity(self, token_counts):
        """
        Property 19: Token Accumulation Additivity.
        
        Validates: Requirements 7.3
        
        Total tokens_used must equal sum of all recorded token counts.
        """
        guard = BudgetGuard(max_steps=1000, max_tokens=1000000, max_repair_attempts=100)

        # Record tokens
        for count in token_counts:
            guard.record_call(count)

        status = guard.get_status()

        # Assert: additivity
        expected_total = sum(token_counts)
        assert status.tokens_used == expected_total, (
            f"Token accumulation not additive: expected {expected_total}, got {status.tokens_used}"
        )
