"""
Property-based tests for BudgetGuard.

Feature: antigravity-architecture-upgrade
Tests budget enforcement and termination using Hypothesis.
"""

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

from core.budget_guard import BudgetGuard, BudgetExceededError


# Feature: antigravity-architecture-upgrade, Property 17: Budget Pre-Call Enforcement
@given(
    tokens_used=st.integers(0, 90000),
    estimated_input=st.integers(1000, 5000),
    max_output=st.integers(1000, 5000),
)
@settings(max_examples=50)
def test_budget_pre_call_enforcement(tokens_used, estimated_input, max_output):
    """
    Property 17: Budget Pre-Call Enforcement
    Validates: Requirements 7.7
    
    Verify that check_pre_call() raises BudgetExceededError when
    remaining budget insufficient for estimated cost.
    """
    max_tokens = 100000
    guard = BudgetGuard(max_tokens=max_tokens)
    
    # Record tokens used
    for _ in range(tokens_used // 1000):
        guard.record_call(1000)
    guard.record_call(tokens_used % 1000)
    
    estimated_cost = estimated_input + max_output
    will_exceed = tokens_used + estimated_cost > max_tokens
    
    if will_exceed:
        # Should raise exception
        with pytest.raises(BudgetExceededError) as exc_info:
            guard.check_pre_call(estimated_input, max_output)
        assert "tokens" in exc_info.value.termination_reason.lower()
    else:
        # Should not raise
        guard.check_pre_call(estimated_input, max_output)



# Feature: antigravity-architecture-upgrade, Property 18: Budget Termination với Reason
@given(limit_type=st.sampled_from(['steps', 'tokens', 'repairs']))
@settings(max_examples=30)
def test_budget_termination_with_reason(limit_type):
    """
    Property 18: Budget Termination với Reason
    Validates: Requirements 7.2
    
    Verify that termination_reason correctly identifies which limit was exceeded.
    """
    if limit_type == 'steps':
        guard = BudgetGuard(max_steps=5, max_tokens=100000, max_repair_attempts=10)
        for _ in range(6):
            guard.record_step()
    elif limit_type == 'tokens':
        guard = BudgetGuard(max_steps=100, max_tokens=1000, max_repair_attempts=10)
        guard.record_call(1001)
    else:  # repairs
        guard = BudgetGuard(max_steps=100, max_tokens=100000, max_repair_attempts=3)
        for _ in range(4):
            guard.record_repair()
    
    status = guard.get_status()
    
    # Assert: termination_reason contains the exceeded dimension
    assert limit_type in status.termination_reason.lower(), (
        f"Expected termination_reason to contain '{limit_type}', "
        f"got: {status.termination_reason}"
    )


# Feature: antigravity-architecture-upgrade, Property 19: Token Accumulation Additivity
@given(token_counts=st.lists(st.integers(100, 1000), min_size=2, max_size=20))
@settings(max_examples=50)
def test_token_accumulation_additivity(token_counts):
    """
    Property 19: Token Accumulation Additivity
    Validates: Requirements 7.3
    
    Verify that token usage accumulates correctly across multiple calls.
    """
    guard = BudgetGuard(max_tokens=sum(token_counts) + 10000)
    
    # Record each token count
    for tokens in token_counts:
        guard.record_call(tokens)
    
    status = guard.get_status()
    
    # Assert: Total tokens used equals sum of all calls
    assert status.tokens_used == sum(token_counts), (
        f"Token accumulation incorrect: expected {sum(token_counts)}, "
        f"got {status.tokens_used}"
    )
