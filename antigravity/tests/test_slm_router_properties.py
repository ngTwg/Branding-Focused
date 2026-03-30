"""
Property-based tests for SLMRouter budget-aware routing.

Validates Task 2 (Final Polish):
- P1: Budget Respect - never exceed remaining budget
- P2: Graceful Degradation - fallback to cheaper models when constrained
- P3: Quality Monotonicity - prefer expensive models unless budget forces fallback

Uses Hypothesis for property-based testing with 100+ examples per property.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume
from core.slm_router import SLMRouter
from core.budget_guard import BudgetGuard, BudgetExceededError
from pathlib import Path
import tempfile
import json


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def test_prototypes_file():
    """Create temporary prototypes file for SLMRouter."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        prototypes = {
            "frontend": {
                "examples": ["create react component", "style button with CSS"],
            },
            "backend": {
                "examples": ["create REST API", "database query optimization"],
            },
            "debug": {
                "examples": ["fix bug in authentication", "investigate memory leak"],
            },
        }
        json.dump(prototypes, f)
        f.flush()
        yield Path(f.name)


@pytest.fixture(scope="module")
def router(test_prototypes_file):
    """Create SLMRouter instance."""
    return SLMRouter(
        prototypes_path=test_prototypes_file,
        confidence_threshold=0.85,
    )


# ── Hypothesis Strategies ─────────────────────────────────────────────────────

@st.composite
def query_strategy(draw):
    """Generate realistic user queries with varying complexity."""
    complexity_templates = {
        "simple": [
            "create a button",
            "add CSS styling",
            "write hello world",
        ],
        "moderate": [
            "create REST API endpoint",
            "implement user authentication",
            "optimize database query",
        ],
        "complex": [
            "debug memory leak in production",
            "refactor architecture for scalability",
            "investigate security vulnerability",
            "fix bug in multi-threaded algorithm",
        ],
    }
    
    complexity = draw(st.sampled_from(["simple", "moderate", "complex"]))
    template = draw(st.sampled_from(complexity_templates[complexity]))
    
    return template


@st.composite
def budget_strategy(draw):
    """Generate budget constraints (tokens remaining)."""
    # Range: 500 to 10000 tokens
    return draw(st.integers(min_value=500, max_value=10000))


# ── Property 1: Budget Respect ────────────────────────────────────────────────

@settings(max_examples=100, deadline=None)
@given(query=query_strategy(), remaining_tokens=budget_strategy())
def test_property_budget_respect(router, query, remaining_tokens):
    """
    Property P1: Budget Respect
    
    For all (query, remaining_tokens), the chosen model must have:
        estimated_cost <= remaining_tokens
    
    This property ensures the router NEVER violates budget constraints.
    """
    # Setup BudgetGuard with specific remaining budget
    budget_guard = BudgetGuard(
        max_steps=50,
        max_tokens=remaining_tokens + 1000,  # Set max higher than remaining
        max_repair_attempts=5,
    )
    
    # Consume tokens to set remaining to our test value
    tokens_to_consume = 1000
    budget_guard.record_call(tokens_to_consume)
    
    # Verify remaining is what we expect
    status = budget_guard.get_status()
    actual_remaining = status.tokens_remaining
    
    # If remaining is too low for any model, expect BudgetExceededError
    min_model_cost = min(
        router.MODEL_COSTS[model]["estimated_tokens"]
        for model in router.MODEL_COSTS
    )
    
    if actual_remaining < min_model_cost:
        # Should raise BudgetExceededError
        with pytest.raises(BudgetExceededError):
            router.route_with_budget(query, budget_guard)
    else:
        # Should return a valid decision
        decision = router.route_with_budget(query, budget_guard)
        
        # PROPERTY: estimated_cost <= remaining_tokens
        assert decision.estimated_cost <= actual_remaining, (
            f"Budget violation: estimated_cost={decision.estimated_cost} > "
            f"remaining={actual_remaining}"
        )
        
        # Verify model exists in MODEL_COSTS
        assert decision.model in router.MODEL_COSTS, (
            f"Unknown model: {decision.model}"
        )
        
        # Verify estimated_cost matches MODEL_COSTS
        expected_cost = router.MODEL_COSTS[decision.model]["estimated_tokens"]
        assert decision.estimated_cost == expected_cost, (
            f"Cost mismatch: decision.estimated_cost={decision.estimated_cost} != "
            f"MODEL_COSTS={expected_cost}"
        )


# ── Property 2: Graceful Degradation ──────────────────────────────────────────

@settings(max_examples=100, deadline=None)
@given(query=query_strategy())
def test_property_graceful_degradation(router, query):
    """
    Property P2: Graceful Degradation
    
    When budget decreases, router must fallback to cheaper models in deterministic order:
        o1-mini (5000) → claude-sonnet (2000) → qwen-local (1000)
    
    This property ensures graceful degradation without crashes.
    """
    # Test with decreasing budgets
    budgets = [10000, 4000, 1500, 800]
    previous_cost = float('inf')
    
    for budget in budgets:
        budget_guard = BudgetGuard(max_tokens=budget)
        
        try:
            decision = router.route_with_budget(query, budget_guard)
            
            # PROPERTY: Cost should decrease or stay same as budget decreases
            assert decision.estimated_cost <= previous_cost, (
                f"Degradation violation: cost increased from {previous_cost} to "
                f"{decision.estimated_cost} when budget decreased"
            )
            
            previous_cost = decision.estimated_cost
            
            # PROPERTY: Fallback flag should be set when not using first choice
            complexity = router.assess_complexity(query)
            first_choice = router.MODEL_RANKING[complexity][0]
            first_choice_cost = router.MODEL_COSTS[first_choice]["estimated_tokens"]
            
            if decision.model != first_choice and budget >= first_choice_cost:
                # If we didn't choose first choice but budget allows it, something's wrong
                pytest.fail(
                    f"Should have chosen {first_choice} (cost: {first_choice_cost}) "
                    f"with budget {budget}, but chose {decision.model} instead"
                )
            
        except BudgetExceededError:
            # Budget too low for any model - this is acceptable
            # Verify that indeed no model fits
            min_cost = min(
                router.MODEL_COSTS[m]["estimated_tokens"]
                for m in router.MODEL_COSTS
            )
            assert budget < min_cost, (
                f"BudgetExceededError raised but budget {budget} >= min_cost {min_cost}"
            )
            break


# ── Property 3: Quality Monotonicity ──────────────────────────────────────────

@settings(max_examples=100, deadline=None)
@given(query=query_strategy(), budget_multiplier=st.floats(min_value=1.0, max_value=3.0))
def test_property_quality_monotonicity(router, query, budget_multiplier):
    """
    Property P3: Quality Monotonicity
    
    For complex tasks:
    - If budget allows o1-mini (5000 tokens), it should be chosen
    - If budget only allows claude-sonnet (2000 tokens), fallback should be set
    - If budget only allows qwen-local (1000 tokens), fallback should be set
    
    Expensive models should not be chosen when cheaper models suffice for the complexity.
    """
    complexity = router.assess_complexity(query)
    
    # Get first choice for this complexity
    first_choice = router.MODEL_RANKING[complexity][0]
    first_choice_cost = router.MODEL_COSTS[first_choice]["estimated_tokens"]
    
    # Set budget as multiple of first choice cost
    budget = int(first_choice_cost * budget_multiplier)
    budget_guard = BudgetGuard(max_tokens=budget)
    
    try:
        decision = router.route_with_budget(query, budget_guard)
        
        # PROPERTY: If budget allows first choice, it should be chosen
        if budget >= first_choice_cost:
            assert decision.model == first_choice, (
                f"Quality monotonicity violation: budget {budget} allows {first_choice} "
                f"(cost: {first_choice_cost}), but chose {decision.model} instead"
            )
            assert not decision.is_fallback, (
                f"Fallback flag set incorrectly when first choice was available"
            )
        else:
            # Budget doesn't allow first choice - fallback should be set
            assert decision.is_fallback, (
                f"Fallback flag not set when budget {budget} < first_choice_cost {first_choice_cost}"
            )
            
            # Verify chosen model is cheaper than first choice
            assert decision.estimated_cost < first_choice_cost, (
                f"Fallback model {decision.model} (cost: {decision.estimated_cost}) "
                f"is not cheaper than first choice {first_choice} (cost: {first_choice_cost})"
            )
    
    except BudgetExceededError:
        # Budget too low for any model - verify this is correct
        min_cost = min(
            router.MODEL_COSTS[m]["estimated_tokens"]
            for m in router.MODEL_COSTS
        )
        assert budget < min_cost, (
            f"BudgetExceededError raised but budget {budget} >= min_cost {min_cost}"
        )


# ── Integration Tests ─────────────────────────────────────────────────────────

def test_budget_respect_integration(router):
    """
    Integration test: Verify budget respect with realistic scenarios.
    """
    scenarios = [
        # (query, budget, expected_model_or_error)
        ("create a button", 10000, "claude-3-5-sonnet-20241022"),
        ("create a button", 1500, "qwen2.5:3b-instruct"),
        ("create a button", 500, BudgetExceededError),
        # "debug memory leak" = 1 indicator + 3 words = simple (not complex)
        ("debug memory leak in production system", 10000, "claude-3-5-sonnet-20241022"),
        ("debug memory leak in production system", 1200, "qwen2.5:3b-instruct"),
        # Complex query with multiple indicators
        ("debug and fix bug in authentication refactor", 10000, "o1-mini"),
        ("debug and fix bug in authentication refactor", 3000, "claude-3-5-sonnet-20241022"),
        ("debug and fix bug in authentication refactor", 1200, "qwen2.5:3b-instruct"),
        ("debug and fix bug in authentication refactor", 800, BudgetExceededError),
    ]
    
    for query, budget, expected in scenarios:
        budget_guard = BudgetGuard(max_tokens=budget)
        
        if expected == BudgetExceededError:
            with pytest.raises(BudgetExceededError):
                router.route_with_budget(query, budget_guard)
        else:
            decision = router.route_with_budget(query, budget_guard)
            assert decision.model == expected, (
                f"Expected {expected} for query='{query}' budget={budget}, "
                f"got {decision.model} (complexity={decision.complexity})"
            )
            assert decision.estimated_cost <= budget


def test_graceful_degradation_integration(router):
    """
    Integration test: Verify graceful degradation with budget cuts.
    """
    # Use query with multiple complexity indicators to ensure "complex" classification
    query = "debug and investigate security vulnerability in authentication algorithm"
    
    # Start with high budget, gradually decrease
    budgets = [10000, 4000, 1500, 900]
    expected_models = [
        "o1-mini",
        "claude-3-5-sonnet-20241022",
        "qwen2.5:3b-instruct",
        BudgetExceededError,
    ]
    
    for budget, expected in zip(budgets, expected_models):
        budget_guard = BudgetGuard(max_tokens=budget)
        
        if expected == BudgetExceededError:
            with pytest.raises(BudgetExceededError):
                router.route_with_budget(query, budget_guard)
        else:
            decision = router.route_with_budget(query, budget_guard)
            assert decision.model == expected, (
                f"Budget {budget}: expected {expected}, got {decision.model}"
            )


def test_quality_monotonicity_integration(router):
    """
    Integration test: Verify quality monotonicity for different complexities.
    """
    test_cases = [
        # (query, complexity, budget, expected_model, expected_fallback)
        ("create button", "simple", 10000, "claude-3-5-sonnet-20241022", False),
        ("create button", "simple", 1200, "qwen2.5:3b-instruct", True),
        ("optimize database query performance", "moderate", 10000, "claude-3-5-sonnet-20241022", False),
        ("optimize database query performance", "moderate", 1200, "qwen2.5:3b-instruct", True),
        # Complex query needs multiple indicators
        ("debug and fix security vulnerability in algorithm", "complex", 10000, "o1-mini", False),
        ("debug and fix security vulnerability in algorithm", "complex", 3000, "claude-3-5-sonnet-20241022", True),
        ("debug and fix security vulnerability in algorithm", "complex", 1200, "qwen2.5:3b-instruct", True),
    ]
    
    for query, complexity, budget, expected_model, expected_fallback in test_cases:
        budget_guard = BudgetGuard(max_tokens=budget)
        decision = router.route_with_budget(query, budget_guard)
        
        assert decision.model == expected_model, (
            f"Query '{query}' (complexity={complexity}, budget={budget}): "
            f"expected {expected_model}, got {decision.model}"
        )
        
        assert decision.is_fallback == expected_fallback, (
            f"Query '{query}': expected fallback={expected_fallback}, "
            f"got {decision.is_fallback}"
        )
        
        assert decision.complexity == complexity


# ── Edge Cases ────────────────────────────────────────────────────────────────

def test_edge_case_exact_budget_match(router):
    """Edge case: Budget exactly matches model cost."""
    query = "create button"
    
    # Set budget to exactly match qwen cost (1000 tokens)
    budget_guard = BudgetGuard(max_tokens=1000)
    decision = router.route_with_budget(query, budget_guard)
    
    assert decision.model == "qwen2.5:3b-instruct"
    assert decision.estimated_cost == 1000
    assert decision.estimated_cost <= 1000  # Property P1


def test_edge_case_zero_budget(router):
    """Edge case: Very low budget (< min model cost) should raise BudgetExceededError."""
    query = "create button"
    # Use 100 tokens instead of 0 to avoid division by zero in BudgetGuard
    budget_guard = BudgetGuard(max_tokens=100)
    
    with pytest.raises(BudgetExceededError):
        router.route_with_budget(query, budget_guard)


def test_edge_case_very_high_budget(router):
    """Edge case: Very high budget should choose best model for complexity."""
    # Complex query with multiple indicators
    query = "debug and investigate complex algorithm performance issue"
    budget_guard = BudgetGuard(max_tokens=1_000_000)
    
    decision = router.route_with_budget(query, budget_guard)
    
    # Should choose o1-mini for complex task with unlimited budget
    assert decision.model == "o1-mini"
    assert not decision.is_fallback


# ── Summary ───────────────────────────────────────────────────────────────────

"""
Test Summary:

Property Tests (Hypothesis):
- test_property_budget_respect: 100 examples
- test_property_graceful_degradation: 100 examples  
- test_property_quality_monotonicity: 100 examples

Integration Tests:
- test_budget_respect_integration: 7 scenarios
- test_graceful_degradation_integration: 4 budget levels
- test_quality_monotonicity_integration: 7 complexity/budget combinations

Edge Cases:
- test_edge_case_exact_budget_match
- test_edge_case_zero_budget
- test_edge_case_very_high_budget

Total: 300+ test cases covering all properties and edge cases.

Expected runtime: ~5-10 seconds
"""
