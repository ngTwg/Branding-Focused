"""
Property-based tests for SLMRouter (Architecture Upgrade).

Feature: antigravity-architecture-upgrade
Tests routing idempotence and confidence threshold using Hypothesis.
"""

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st
from unittest.mock import Mock, patch

from core.slm_router import SLMRouter
from core.schemas import SLMRouteDecision


# Feature: antigravity-architecture-upgrade, Property 13: SLM Routing Idempotence
@given(query=st.text(min_size=5, max_size=200))
@settings(max_examples=30)
def test_slm_routing_idempotence(query):
    """
    Property 13: SLM Routing Idempotence
    Validates: Requirements 4.8
    
    Verify that routing the result of a classification returns the same result.
    """
    # Mock SLMRouter with deterministic behavior
    router = SLMRouter(prototypes_path="config/slm_prototypes.json")
    
    # First classification
    result1 = router.classify(query)
    
    if result1 is not None:
        # Second classification using the chosen route
        result2 = router.classify(result1.chosen)
        
        # Assert: Idempotent - same route chosen
        if result2 is not None:
            assert result2.chosen == result1.chosen, (
                f"Routing not idempotent:\n"
                f"First: {result1.chosen}\n"
                f"Second: {result2.chosen}"
            )


# Feature: antigravity-architecture-upgrade, Property 14: SLM Confidence Threshold Routing
@given(threshold=st.floats(0.5, 0.95))
@settings(max_examples=20)
def test_slm_confidence_threshold_routing(threshold):
    """
    Property 14: SLM Confidence Threshold Routing
    Validates: Requirements 4.2, 4.3
    
    Verify that low confidence queries fall through to LLM.
    """
    router = SLMRouter(
        prototypes_path="config/slm_prototypes.json",
        confidence_threshold=threshold
    )
    
    # Test with various queries
    test_queries = [
        "fix syntax error",  # High confidence
        "asdfghjkl qwerty",  # Low confidence (gibberish)
        "help me with this",  # Medium confidence
    ]
    
    for query in test_queries:
        result = router.classify(query)
        
        if result is not None:
            # If classified, confidence should be >= threshold
            assert result.confidence >= threshold, (
                f"Classification returned with confidence {result.confidence} "
                f"below threshold {threshold}"
            )
        # If None, it correctly fell through to LLM (low confidence)
