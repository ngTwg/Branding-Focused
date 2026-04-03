"""
Unit and Property Tests for ErrorPrioritizer

Tests error classification, prioritization, chain detection,
clustering, and context limiting.

Requirements: 2.1-2.6 from antigravity-resilience-upgrade spec.
"""

import pytest
from hypothesis import given, strategies as st, settings

from antigravity.core.error_prioritizer import (
    ErrorPrioritizer,
    ErrorSeverity,
    PrioritizedError,
    ErrorCluster
)


# ── Unit Tests: Error Classification ──────────────────────────────────────────

def test_classify_syntax_error():
    """
    Test classification of syntax errors.
    
    Requirements: 2.1
    """
    prioritizer = ErrorPrioritizer()
    
    assert prioritizer._classify_error("SyntaxError: invalid syntax") == ErrorSeverity.SYNTAX
    assert prioritizer._classify_error("IndentationError: unexpected indent") == ErrorSeverity.SYNTAX
    assert prioritizer._classify_error("TabError: inconsistent use of tabs") == ErrorSeverity.SYNTAX
    assert prioritizer._classify_error("unexpected EOF while parsing") == ErrorSeverity.SYNTAX


def test_classify_runtime_error():
    """
    Test classification of runtime errors.
    
    Requirements: 2.1
    """
    prioritizer = ErrorPrioritizer()
    
    assert prioritizer._classify_error("NameError: name 'x' is not defined") == ErrorSeverity.RUNTIME
    assert prioritizer._classify_error("TypeError: unsupported operand") == ErrorSeverity.RUNTIME
    assert prioritizer._classify_error("AttributeError: object has no attribute") == ErrorSeverity.RUNTIME
    assert prioritizer._classify_error("ImportError: cannot import name") == ErrorSeverity.RUNTIME


def test_classify_lint_error():
    """
    Test classification of lint errors.
    
    Requirements: 2.1
    """
    prioritizer = ErrorPrioritizer()
    
    assert prioritizer._classify_error("W0612: Unused variable 'x'") == ErrorSeverity.LINT
    assert prioritizer._classify_error("C0103: Invalid name") == ErrorSeverity.LINT
    assert prioritizer._classify_error("R0913: Too many arguments") == ErrorSeverity.LINT


def test_classify_unknown_defaults_to_runtime():
    """Test that unknown errors default to RUNTIME."""
    prioritizer = ErrorPrioritizer()
    
    assert prioritizer._classify_error("Some unknown error") == ErrorSeverity.RUNTIME


# ── Unit Tests: Prioritization Order ──────────────────────────────────────────

def test_prioritization_order():
    """
    Test that errors are prioritized by severity.
    
    SYNTAX > RUNTIME > LINT
    
    Requirements: 2.2
    """
    prioritizer = ErrorPrioritizer()
    
    errors = [
        "W0612: Unused variable",  # LINT
        "SyntaxError: invalid syntax",  # SYNTAX
        "NameError: name 'x' not defined",  # RUNTIME
        "C0103: Invalid name",  # LINT
    ]
    
    prioritized = prioritizer.prioritize_errors(errors, max_k=3)
    
    # Should return top 3: SYNTAX, RUNTIME, LINT
    assert len(prioritized) == 3
    assert prioritized[0].severity == ErrorSeverity.SYNTAX
    assert prioritized[1].severity == ErrorSeverity.RUNTIME
    assert prioritized[2].severity == ErrorSeverity.LINT


def test_prioritization_max_k():
    """Test that prioritize_errors respects max_k limit."""
    prioritizer = ErrorPrioritizer()
    
    errors = [f"Error {i}" for i in range(10)]
    
    prioritized = prioritizer.prioritize_errors(errors, max_k=3)
    
    assert len(prioritized) == 3


def test_prioritization_empty_list():
    """Test prioritization with empty error list."""
    prioritizer = ErrorPrioritizer()
    
    prioritized = prioritizer.prioritize_errors([], max_k=3)
    
    assert prioritized == []


# ── Unit Tests: Context Size Estimation ───────────────────────────────────────

def test_estimate_context_size():
    """
    Test context size estimation.
    
    Requirements: 2.5
    """
    prioritizer = ErrorPrioritizer()
    
    error = PrioritizedError(
        error_text="NameError: name 'variable_name' is not defined in function foo",
        severity=ErrorSeverity.RUNTIME
    )
    
    tokens = prioritizer.estimate_context_size(error)
    
    # Should be: ~10 words * 1.3 + 50 (metadata) + 100 (context) ≈ 163
    assert 150 < tokens < 200


def test_estimate_context_size_long_error():
    """Test context size estimation for long error messages."""
    prioritizer = ErrorPrioritizer()
    
    # Long error message (50 words)
    long_text = " ".join(["word"] * 50)
    error = PrioritizedError(
        error_text=long_text,
        severity=ErrorSeverity.RUNTIME
    )
    
    tokens = prioritizer.estimate_context_size(error)
    
    # Should be: 50 * 1.3 + 50 + 100 = 215
    assert 200 < tokens < 250


# ── Unit Tests: Error Chain Detection ─────────────────────────────────────────

def test_detect_import_error_chain():
    """
    Test detection of ImportError → NameError chain.
    
    Requirements: 2.3, 2.6
    """
    prioritizer = ErrorPrioritizer()
    
    errors = [
        PrioritizedError(
            error_text='File "test.py", line 5: ImportError: cannot import name "foo"',
            severity=ErrorSeverity.RUNTIME,
            line_number=5,
            file_path="test.py"
        ),
        PrioritizedError(
            error_text='File "test.py", line 10: NameError: name "foo" is not defined',
            severity=ErrorSeverity.RUNTIME,
            line_number=10,
            file_path="test.py"
        )
    ]
    
    root_causes = prioritizer.detect_error_chains(errors)
    
    # Should identify ImportError as root cause
    assert len(root_causes) == 1
    assert root_causes[0].is_root_cause is True
    assert "ImportError" in root_causes[0].error_text
    assert len(root_causes[0].dependent_errors) == 1


def test_detect_syntax_error_chain():
    """
    Test detection of SyntaxError causing downstream errors.
    
    Requirements: 2.3, 2.6
    """
    prioritizer = ErrorPrioritizer()
    
    errors = [
        PrioritizedError(
            error_text='File "test.py", line 3: SyntaxError: invalid syntax',
            severity=ErrorSeverity.SYNTAX,
            line_number=3,
            file_path="test.py"
        ),
        PrioritizedError(
            error_text='File "test.py", line 10: NameError: name "x" not defined',
            severity=ErrorSeverity.RUNTIME,
            line_number=10,
            file_path="test.py"
        ),
        PrioritizedError(
            error_text='File "test.py", line 15: TypeError: unsupported operand',
            severity=ErrorSeverity.RUNTIME,
            line_number=15,
            file_path="test.py"
        )
    ]
    
    root_causes = prioritizer.detect_error_chains(errors)
    
    # Should identify SyntaxError as root cause
    assert len(root_causes) == 1
    assert root_causes[0].severity == ErrorSeverity.SYNTAX
    assert root_causes[0].is_root_cause is True
    assert len(root_causes[0].dependent_errors) == 2


def test_no_error_chains():
    """Test that independent errors are all kept."""
    prioritizer = ErrorPrioritizer()
    
    errors = [
        PrioritizedError(
            error_text="NameError in function foo",
            severity=ErrorSeverity.RUNTIME,
            file_path="test1.py"
        ),
        PrioritizedError(
            error_text="TypeError in function bar",
            severity=ErrorSeverity.RUNTIME,
            file_path="test2.py"
        )
    ]
    
    root_causes = prioritizer.detect_error_chains(errors)
    
    # All errors should be kept (no chains detected)
    assert len(root_causes) == 2


# ── Unit Tests: Error Clustering ──────────────────────────────────────────────

def test_cluster_errors_by_type():
    """
    Test clustering of errors by type.
    
    Requirements: 2.4
    """
    prioritizer = ErrorPrioritizer()
    
    errors = [
        PrioritizedError(
            error_text="NameError: name 'x' not defined in foo",
            severity=ErrorSeverity.RUNTIME
        ),
        PrioritizedError(
            error_text="NameError: name 'y' not defined in bar",
            severity=ErrorSeverity.RUNTIME
        ),
        PrioritizedError(
            error_text="NameError: name 'z' not defined in baz",
            severity=ErrorSeverity.RUNTIME
        ),
        PrioritizedError(
            error_text="TypeError: unsupported operand",
            severity=ErrorSeverity.RUNTIME
        ),
        PrioritizedError(
            error_text="TypeError: cannot concatenate",
            severity=ErrorSeverity.RUNTIME
        )
    ]
    
    clusters = prioritizer.cluster_errors(errors)
    
    # Should create 2 clusters: NameError (3) and TypeError (2)
    assert len(clusters) == 2
    
    name_error_cluster = next(c for c in clusters if c.error_type == "NameError")
    assert name_error_cluster.error_count == 3
    assert "3x NameError" in name_error_cluster.summary
    
    type_error_cluster = next(c for c in clusters if c.error_type == "TypeError")
    assert type_error_cluster.error_count == 2


def test_cluster_errors_min_size():
    """Test that clusters require at least 2 errors."""
    prioritizer = ErrorPrioritizer()
    
    errors = [
        PrioritizedError(
            error_text="NameError: name 'x' not defined",
            severity=ErrorSeverity.RUNTIME
        ),
        PrioritizedError(
            error_text="TypeError: unsupported operand",
            severity=ErrorSeverity.RUNTIME
        )
    ]
    
    clusters = prioritizer.cluster_errors(errors)
    
    # No clusters (each type has only 1 error)
    assert len(clusters) == 0


def test_format_clusters_for_llm():
    """
    Test formatting of clusters for LLM.
    
    Requirements: 2.4, 2.5
    """
    prioritizer = ErrorPrioritizer()
    
    clusters = [
        ErrorCluster(
            cluster_id="NameError_0",
            error_type="NameError",
            affected_functions=["foo", "bar"],
            error_count=3,
            representative_error=PrioritizedError(
                error_text="NameError: name 'x' not defined",
                severity=ErrorSeverity.RUNTIME
            ),
            summary="3x NameError in foo, bar"
        )
    ]
    
    formatted = prioritizer.format_clusters_for_llm(clusters)
    
    assert "[ERROR CLUSTERS]" in formatted
    assert "3x NameError in foo, bar" in formatted
    assert "Representative:" in formatted


# ── Integration Test: Multi-Error Scenario ────────────────────────────────────

def test_multi_error_scenario():
    """
    Integration test: process 10 mixed errors.
    
    Validates: Requirements 2.1-2.6
    """
    prioritizer = ErrorPrioritizer()
    
    errors = [
        "W0612: Unused variable 'x'",
        "SyntaxError: invalid syntax at line 5",
        "NameError: name 'foo' not defined",
        "C0103: Invalid name",
        "TypeError: unsupported operand",
        "NameError: name 'bar' not defined",
        "NameError: name 'baz' not defined",
        "W0613: Unused argument",
        "AttributeError: no attribute 'method'",
        "R0913: Too many arguments"
    ]
    
    # Step 1: Prioritize (top 3)
    prioritized = prioritizer.prioritize_errors(errors, max_k=3)
    
    assert len(prioritized) == 3
    assert prioritized[0].severity == ErrorSeverity.SYNTAX
    
    # Step 2: Estimate total context
    total_tokens = sum(e.context_tokens for e in prioritized)
    
    # Should be reasonable (< 1000 tokens for 3 errors)
    assert total_tokens < 1000
    
    # Step 3: Detect chains (if applicable)
    root_causes = prioritizer.detect_error_chains(prioritized)
    
    assert len(root_causes) >= 1


# ── Property Tests: Priority Ordering ─────────────────────────────────────────

@given(errors=st.lists(
    st.sampled_from([
        "SyntaxError: test",
        "NameError: test",
        "W0612: test"
    ]),
    min_size=1,
    max_size=20
))
@settings(max_examples=50)
def test_priority_ordering_property(errors):
    """
    Property test: output always sorted by severity.
    
    SYNTAX always before RUNTIME before LINT.
    
    Requirements: 2.2
    """
    prioritizer = ErrorPrioritizer()
    
    prioritized = prioritizer.prioritize_errors(errors, max_k=10)
    
    # Verify sorted by severity
    for i in range(len(prioritized) - 1):
        assert prioritized[i].severity <= prioritized[i + 1].severity


@given(max_k=st.integers(min_value=1, max_value=10))
@settings(max_examples=50)
def test_max_k_respected(max_k):
    """
    Property test: prioritize_errors respects max_k limit.
    
    Requirements: 2.2
    """
    prioritizer = ErrorPrioritizer()
    
    errors = [f"Error {i}" for i in range(20)]
    
    prioritized = prioritizer.prioritize_errors(errors, max_k=max_k)
    
    assert len(prioritized) <= max_k
