"""
Integration tests for Error Prioritization with ASTAnalyzer.

Tests the full error prioritization pipeline:
- ErrorPrioritizer classification and filtering
- ASTAnalyzer integration with error context
- Multi-error scenarios with clustering
- Context size limiting

Validates Requirements: 2.1-2.6
"""

import pytest
from pathlib import Path
from antigravity.core.error_prioritizer import ErrorPrioritizer, ErrorSeverity, PrioritizedError
from antigravity.core.ast_analyzer import ASTAnalyzer


# ── Test Fixtures ──────────────────────────────────────────────────────────────

@pytest.fixture
def temp_python_file(tmp_path):
    """Create a temporary Python file with multiple errors."""
    file_path = tmp_path / "test_errors.py"
    content = """
def foo():
    x = 1
    y = 2
    return x + y

def bar():
    # Missing import will cause NameError
    result = undefined_function()
    return result

class MyClass:
    def method1(self):
        # Syntax error on next line
        if True
            pass
    
    def method2(self):
        # Type error
        return "string" + 123
"""
    file_path.write_text(content)
    return str(file_path)


# ── Unit Tests ─────────────────────────────────────────────────────────────────

def test_error_classification():
    """
    Test error severity classification.
    
    Validates: Requirement 2.1
    """
    prioritizer = ErrorPrioritizer()
    
    # Test SYNTAX classification
    syntax_error = "SyntaxError: invalid syntax at line 10"
    assert prioritizer._classify_error(syntax_error) == ErrorSeverity.SYNTAX
    
    # Test RUNTIME classification
    runtime_error = "NameError: name 'undefined_function' is not defined"
    assert prioritizer._classify_error(runtime_error) == ErrorSeverity.RUNTIME
    
    # Test LINT classification
    lint_error = "W0612: Unused variable 'x'"
    assert prioritizer._classify_error(lint_error) == ErrorSeverity.LINT


def test_prioritization_order():
    """
    Test that errors are prioritized by severity.
    
    Validates: Requirement 2.2
    """
    prioritizer = ErrorPrioritizer()
    
    errors = [
        "W0612: Unused variable 'x'",  # LINT
        "SyntaxError: invalid syntax",  # SYNTAX
        "NameError: undefined",  # RUNTIME
        "C0103: Invalid name",  # LINT
    ]
    
    prioritized = prioritizer.prioritize_errors(errors, max_k=3)
    
    # Should return top-3: SYNTAX, RUNTIME, LINT
    assert len(prioritized) == 3
    assert prioritized[0].severity == ErrorSeverity.SYNTAX
    assert prioritized[1].severity == ErrorSeverity.RUNTIME
    assert prioritized[2].severity == ErrorSeverity.LINT


def test_error_chains():
    """
    Test error chain detection (root cause identification).
    
    Validates: Requirement 2.3
    """
    prioritizer = ErrorPrioritizer()
    
    errors = [
        'File "test.py", line 5\nImportError: No module named "missing_module"',
        'File "test.py", line 10\nNameError: name "missing_function" is not defined',
    ]
    
    prioritized = prioritizer.prioritize_errors(errors, max_k=10)
    root_causes = prioritizer.detect_error_chains(prioritized)
    
    # ImportError should be marked as root cause
    import_error = next((e for e in root_causes if "ImportError" in e.error_text), None)
    assert import_error is not None
    assert import_error.is_root_cause
    
    # NameError should be in dependent_errors
    assert any("NameError" in dep for dep in import_error.dependent_errors)


def test_error_clustering():
    """
    Test error clustering for similar errors.
    
    Validates: Requirement 2.4
    """
    prioritizer = ErrorPrioritizer()
    
    errors = [
        'File "test.py", line 5 in foo\nNameError: name "x" is not defined',
        'File "test.py", line 10 in foo\nNameError: name "y" is not defined',
        'File "test.py", line 15 in bar\nNameError: name "z" is not defined',
        'File "test.py", line 20 in foo\nNameError: name "w" is not defined',
        'File "test.py", line 25 in baz\nNameError: name "a" is not defined',
    ]
    
    prioritized = prioritizer.prioritize_errors(errors, max_k=10)
    clusters = prioritizer.cluster_errors(prioritized)
    
    # Should create 1 cluster for NameError
    assert len(clusters) >= 1
    
    name_error_cluster = next((c for c in clusters if c.error_type == "NameError"), None)
    assert name_error_cluster is not None
    assert name_error_cluster.error_count == 5
    assert "foo" in name_error_cluster.affected_functions
    assert name_error_cluster.summary.startswith("5x NameError")


# ── Integration Tests ──────────────────────────────────────────────────────────

def test_multi_error_scenario(temp_python_file):
    """
    Test full error prioritization pipeline with multiple errors.
    
    Validates: Requirement 2.5
    """
    analyzer = ASTAnalyzer()
    
    # Simulate multiple errors from the file
    errors = [
        f'File "{temp_python_file}", line 13\nSyntaxError: invalid syntax',
        f'File "{temp_python_file}", line 9\nNameError: name "undefined_function" is not defined',
        f'File "{temp_python_file}", line 17\nTypeError: unsupported operand type(s)',
        "W0612: Unused variable 'x' at line 3",
        "W0612: Unused variable 'y' at line 4",
    ]
    
    # Analyze with error prioritization
    targets = [(temp_python_file, 13)]  # Focus on syntax error line
    contract = analyzer.analyze(targets, errors=errors)
    
    # Verify error_priority_info exists
    assert contract.error_priority_info is not None
    
    # Verify only top-3 errors returned
    prioritized = contract.error_priority_info["prioritized_errors"]
    assert len(prioritized) <= 3
    
    # Verify SYNTAX error is first
    assert prioritized[0]["severity"] == "SYNTAX"
    
    # Verify total context is reasonable
    total_context = contract.error_priority_info["total_context_tokens"]
    assert total_context <= 1000, f"Context too large: {total_context} tokens"


def test_context_limiting(temp_python_file):
    """
    Test that context size is limited to prevent token overflow.
    
    Validates: Requirement 2.5
    """
    analyzer = ASTAnalyzer()
    
    # Create many errors (>5 to trigger clustering)
    errors = [
        f'File "{temp_python_file}", line {i}\nNameError: name "var{i}" is not defined'
        for i in range(10)
    ]
    
    targets = [(temp_python_file, 1)]
    contract = analyzer.analyze(targets, errors=errors)
    
    # Verify clustering was used
    assert contract.error_priority_info is not None
    clusters = contract.error_priority_info.get("clusters", [])
    assert len(clusters) > 0, "Clustering should be used for >5 errors"
    
    # Verify context limited
    total_context = contract.error_priority_info["total_context_tokens"]
    assert total_context <= 1000


def test_root_cause_focus(temp_python_file):
    """
    Test that repair focuses on root causes, not symptoms.
    
    Validates: Requirement 2.6
    """
    analyzer = ASTAnalyzer()
    
    # Create error chain: ImportError → NameError
    errors = [
        f'File "{temp_python_file}", line 8\nImportError: No module named "missing"',
        f'File "{temp_python_file}", line 9\nNameError: name "undefined_function" is not defined',
        f'File "{temp_python_file}", line 10\nNameError: name "another_undefined" is not defined',
    ]
    
    targets = [(temp_python_file, 8)]
    contract = analyzer.analyze(targets, errors=errors)
    
    # Verify root causes identified
    assert contract.error_priority_info is not None
    root_causes = contract.error_priority_info["root_causes"]
    assert root_causes >= 1, "Should identify at least 1 root cause"
    
    # Verify ImportError is prioritized (root cause)
    prioritized = contract.error_priority_info["prioritized_errors"]
    import_error = next((e for e in prioritized if "ImportError" in e["error_text"]), None)
    assert import_error is not None
    assert import_error["is_root_cause"]


# ── Property Tests ─────────────────────────────────────────────────────────────

@pytest.mark.parametrize("error_count", [1, 3, 5, 10, 20])
def test_priority_ordering_property(error_count):
    """
    Property test: Output always sorted by severity.
    
    Validates: Requirement 2.2
    """
    prioritizer = ErrorPrioritizer()
    
    # Generate mixed errors
    errors = []
    for i in range(error_count):
        if i % 3 == 0:
            errors.append(f"SyntaxError: error {i}")
        elif i % 3 == 1:
            errors.append(f"NameError: error {i}")
        else:
            errors.append(f"W0612: warning {i}")
    
    prioritized = prioritizer.prioritize_errors(errors, max_k=error_count)
    
    # Verify sorted by severity
    for i in range(len(prioritized) - 1):
        assert prioritized[i].severity <= prioritized[i + 1].severity


def test_context_size_estimation():
    """
    Test context size estimation accuracy.
    
    Validates: Requirement 2.5
    """
    prioritizer = ErrorPrioritizer()
    
    error_text = "NameError: name 'undefined_function' is not defined"
    
    error = PrioritizedError(
        error_text=error_text,
        severity=ErrorSeverity.RUNTIME,
        line_number=10,
        file_path="test.py"
    )
    
    estimated = prioritizer.estimate_context_size(error)
    
    # Should be reasonable (text + metadata + context)
    assert estimated > 0
    assert estimated < 500  # Should not be too large for single error
