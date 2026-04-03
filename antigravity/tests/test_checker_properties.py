"""
Property-based tests for DeterministicChecker.

Feature: antigravity-architecture-upgrade
Validates: Requirements 3.5
"""

from datetime import datetime

from hypothesis import given, settings
from hypothesis import strategies as st

from antigravity.core.checker import DeterministicChecker


class TestCheckerProperties:
    """Property tests for error normalization."""

    @given(
        error_msg=st.text(min_size=10, max_size=100),
        path1=st.text(min_size=5, max_size=50),
        path2=st.text(min_size=5, max_size=50),
        timestamp1=st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2030, 12, 31)),
        timestamp2=st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2030, 12, 31)),
        line=st.integers(min_value=1, max_value=1000),
    )
    @settings(max_examples=100)
    def test_error_normalization_stability(
        self, error_msg, path1, path2, timestamp1, timestamp2, line
    ):
        """
        Property 12: Error Normalization Stability.
        
        Validates: Requirements 3.5
        
        Errors with same root cause but different paths/timestamps should normalize to same signature.
        """
        # Format errors with different paths/timestamps
        error1 = f"{path1}:{line}: SyntaxError: {error_msg} (at {timestamp1.isoformat()})"
        error2 = f"{path2}:{line}: SyntaxError: {error_msg} (at {timestamp2.isoformat()})"

        checker = DeterministicChecker()

        # Normalize
        normalized1 = checker._normalize_errors([error1])
        normalized2 = checker._normalize_errors([error2])

        # Assert: same signature (error type + message, ignoring path/timestamp)
        assert normalized1 == normalized2, (
            f"Error normalization unstable:\n"
            f"Error 1: {error1}\n"
            f"Error 2: {error2}\n"
            f"Normalized 1: {normalized1}\n"
            f"Normalized 2: {normalized2}"
        )
