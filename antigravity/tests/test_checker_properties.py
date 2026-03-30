"""
Property-based tests for DeterministicChecker.

Feature: antigravity-architecture-upgrade
Tests error normalization and delta computation using Hypothesis.
"""

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st
from datetime import datetime

from core.checker import DeterministicChecker


# Feature: antigravity-architecture-upgrade, Property 12: Error Normalization Stability
@given(
    error_msg=st.text(min_size=10, max_size=100),
    path1=st.text(min_size=1, max_size=50),
    path2=st.text(min_size=1, max_size=50),
    line=st.integers(min_value=1, max_value=1000),
    timestamp1=st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2030, 12, 31)),
    timestamp2=st.datetimes(min_value=datetime(2020, 1, 1), max_value=datetime(2030, 12, 31)),
)
@settings(max_examples=50)
def test_error_normalization_stability(error_msg, path1, path2, line, timestamp1, timestamp2):
    """
    Property 12: Error Normalization Stability
    Validates: Requirements 3.5
    
    Verify that errors with same root cause but different paths/timestamps
    normalize to the same signature.
    """
    # Assume paths are different (otherwise test is trivial)
    assume(path1 != path2)
    assume(timestamp1 != timestamp2)
    
    # Create two error messages with same root cause but different metadata
    error_type = "NameError"
    error1 = f"{path1}:{line}: {error_type}: {error_msg} (at {timestamp1.isoformat()})"
    error2 = f"{path2}:{line}: {error_type}: {error_msg} (at {timestamp2.isoformat()})"
    
    checker = DeterministicChecker()
    
    # Normalize both errors
    normalized1 = checker._normalize_errors([error1])
    normalized2 = checker._normalize_errors([error2])
    
    # Assert: Same signature after normalization
    assert normalized1 == normalized2, (
        f"Error normalization not stable:\n"
        f"Error 1: {error1}\n"
        f"Error 2: {error2}\n"
        f"Normalized 1: {normalized1}\n"
        f"Normalized 2: {normalized2}"
    )
