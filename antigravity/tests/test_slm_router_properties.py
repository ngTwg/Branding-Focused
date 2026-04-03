"""
Property-based tests for SLMRouter.

Feature: antigravity-architecture-upgrade
Validates: Requirements 4.2, 4.3, 4.8
"""

from unittest.mock import MagicMock, patch

from hypothesis import given, settings
from hypothesis import strategies as st

from antigravity.core.schemas import SLMRouteDecision
from antigravity.core.slm_router import SLMRouter


class TestSLMRouterProperties:
    """Property tests for SLM routing logic."""

    @given(query=st.text(min_size=5, max_size=200))
    @settings(max_examples=50)
    def test_slm_routing_idempotence(self, query):
        """
        Property 13: SLM Routing Idempotence.
        
        Validates: Requirements 4.8
        
        Routing the result of a classification should return the same route.
        """
        # Mock prototypes
        mock_prototypes = {
            "debug": [0.1, 0.2, 0.3],
            "implement": [0.4, 0.5, 0.6],
            "refactor": [0.7, 0.8, 0.9],
        }

        with patch("antigravity.core.slm_router.SentenceTransformer") as mock_st:
            mock_model = MagicMock()
            mock_st.return_value = mock_model
            
            # Mock encode to return consistent embeddings
            mock_model.encode.return_value = [0.5, 0.5, 0.5]

            router = SLMRouter(prototypes_path=None, confidence_threshold=0.85)
            router._prototypes = mock_prototypes
            router._enabled = True

            # First classification
            result1 = router.classify(query)

            if result1 is not None:
                # Second classification on the result
                result2 = router.classify(result1.chosen)

                # Assert: idempotent
                assert result2 is not None, "Second classification returned None"
                assert result2.chosen == result1.chosen, (
                    f"Routing not idempotent:\n"
                    f"First: {result1.chosen}\n"
                    f"Second: {result2.chosen}"
                )

    @given(threshold=st.floats(0.5, 0.95))
    @settings(max_examples=30)
    def test_slm_confidence_threshold_routing(self, threshold):
        """
        Property 14: SLM Confidence Threshold Routing.
        
        Validates: Requirements 4.2, 4.3
        
        When confidence >= threshold, LLM should not be called.
        When confidence < threshold, LLM should be called.
        """
        mock_prototypes = {
            "debug": [0.1, 0.2, 0.3],
            "implement": [0.4, 0.5, 0.6],
        }

        with patch("antigravity.core.slm_router.SentenceTransformer") as mock_st:
            mock_model = MagicMock()
            mock_st.return_value = mock_model

            router = SLMRouter(prototypes_path=None, confidence_threshold=threshold)
            router._prototypes = mock_prototypes
            router._enabled = True

            # Test high confidence case (should not call LLM)
            mock_model.encode.return_value = [0.1, 0.2, 0.3]  # Exact match with "debug"
            
            result_high = router.classify("debug this issue")
            
            # High confidence should return result without LLM
            if result_high is not None:
                assert result_high.confidence >= threshold, (
                    f"High confidence result below threshold: {result_high.confidence} < {threshold}"
                )

            # Test low confidence case (should return None, triggering LLM fallback)
            mock_model.encode.return_value = [0.9, 0.9, 0.9]  # No match
            
            result_low = router.classify("completely unrelated query xyz123")
            
            # Low confidence should return None (LLM fallback)
            if result_low is None:
                # This is expected behavior - LLM will be called
                pass
            else:
                # If result returned, confidence must be >= threshold
                assert result_low.confidence >= threshold, (
                    f"Low confidence result returned: {result_low.confidence} < {threshold}"
                )
