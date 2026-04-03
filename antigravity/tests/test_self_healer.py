"""
Tests for Self-Healing System - v6.5.0-SLIM
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime

from antigravity.core.self_healer import (
    SelfHealer,
    ErrorType,
    HealingStatus,
    ErrorPattern,
)


@pytest.fixture
def temp_log_dir():
    """Create temporary log directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def healer(temp_log_dir):
    """Create SelfHealer instance."""
    return SelfHealer(log_dir=temp_log_dir, enable_auto_fix=True)


def test_init(healer, temp_log_dir):
    """Test SelfHealer initialization."""
    assert healer.log_dir == temp_log_dir
    assert healer.enable_auto_fix is True
    assert healer.max_attempts_per_error == 3
    assert len(healer.error_patterns) > 0
    assert healer.log_dir.exists()


def test_detect_syntax_error(healer):
    """Test syntax error detection."""
    error_msg = "SyntaxError: invalid syntax at line 10"
    pattern = healer.detect_error_type(error_msg)
    
    assert pattern is not None
    assert pattern.error_type == ErrorType.SYNTAX_ERROR
    assert pattern.fix_strategy == "fix_syntax_error"


def test_detect_import_error(healer):
    """Test import error detection."""
    error_msg = "ModuleNotFoundError: No module named 'nonexistent'"
    pattern = healer.detect_error_type(error_msg)
    
    assert pattern is not None
    assert pattern.error_type == ErrorType.IMPORT_ERROR
    assert pattern.fix_strategy == "fix_import_error"


def test_detect_type_error(healer):
    """Test type error detection."""
    error_msg = "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
    pattern = healer.detect_error_type(error_msg)
    
    assert pattern is not None
    assert pattern.error_type == ErrorType.TYPE_ERROR


def test_detect_attribute_error(healer):
    """Test attribute error detection."""
    error_msg = "AttributeError: 'NoneType' object has no attribute 'value'"
    pattern = healer.detect_error_type(error_msg)
    
    assert pattern is not None
    assert pattern.error_type == ErrorType.ATTRIBUTE_ERROR


def test_detect_name_error(healer):
    """Test name error detection."""
    error_msg = "NameError: name 'undefined_var' is not defined"
    pattern = healer.detect_error_type(error_msg)
    
    assert pattern is not None
    assert pattern.error_type == ErrorType.NAME_ERROR


def test_detect_unknown_error(healer):
    """Test unknown error detection."""
    error_msg = "SomeWeirdError: something went wrong"
    pattern = healer.detect_error_type(error_msg)
    
    assert pattern is None


def test_register_fix_strategy(healer):
    """Test registering a fix strategy."""
    def mock_fix(error_msg, context):
        return True
    
    healer.register_fix_strategy("mock_fix", mock_fix)
    assert "mock_fix" in healer.fix_strategies
    assert healer.fix_strategies["mock_fix"] == mock_fix


def test_should_attempt_fix_enabled(healer):
    """Test should_attempt_fix when enabled."""
    error_sig = "test_error:message"
    
    # First 3 attempts should be allowed
    assert healer.should_attempt_fix(error_sig) is True
    healer.error_attempts[error_sig] = 1
    assert healer.should_attempt_fix(error_sig) is True
    healer.error_attempts[error_sig] = 2
    assert healer.should_attempt_fix(error_sig) is True
    
    # 4th attempt should be blocked
    healer.error_attempts[error_sig] = 3
    assert healer.should_attempt_fix(error_sig) is False


def test_should_attempt_fix_disabled(temp_log_dir):
    """Test should_attempt_fix when disabled."""
    healer = SelfHealer(log_dir=temp_log_dir, enable_auto_fix=False)
    assert healer.should_attempt_fix("any_error") is False


def test_attempt_heal_unknown_error(healer):
    """Test healing attempt for unknown error."""
    error_msg = "UnknownError: weird stuff"
    attempt = healer.attempt_heal(error_msg)
    
    assert attempt.error_type == ErrorType.UNKNOWN
    assert attempt.status == HealingStatus.SKIPPED
    assert "Unknown error type" in attempt.details


def test_attempt_heal_no_strategy(healer):
    """Test healing attempt when strategy not registered."""
    error_msg = "SyntaxError: invalid syntax"
    attempt = healer.attempt_heal(error_msg)
    
    assert attempt.error_type == ErrorType.SYNTAX_ERROR
    assert attempt.status == HealingStatus.FAILED
    assert "not registered" in attempt.details


def test_attempt_heal_success(healer):
    """Test successful healing attempt."""
    # Register mock fix strategy
    def mock_fix(error_msg, context):
        return True
    
    healer.register_fix_strategy("fix_syntax_error", mock_fix)
    
    error_msg = "SyntaxError: invalid syntax"
    attempt = healer.attempt_heal(error_msg)
    
    assert attempt.error_type == ErrorType.SYNTAX_ERROR
    assert attempt.status == HealingStatus.SUCCESS
    assert "successfully" in attempt.details.lower()


def test_attempt_heal_failure(healer):
    """Test failed healing attempt."""
    # Register mock fix strategy that fails
    def mock_fix(error_msg, context):
        return False
    
    healer.register_fix_strategy("fix_import_error", mock_fix)
    
    error_msg = "ImportError: No module named 'test'"
    attempt = healer.attempt_heal(error_msg)
    
    assert attempt.error_type == ErrorType.IMPORT_ERROR
    assert attempt.status == HealingStatus.FAILED


def test_attempt_heal_exception(healer):
    """Test healing attempt that raises exception."""
    # Register mock fix strategy that raises
    def mock_fix(error_msg, context):
        raise ValueError("Fix failed")
    
    healer.register_fix_strategy("fix_type_error", mock_fix)
    
    error_msg = "TypeError: bad type"
    attempt = healer.attempt_heal(error_msg)
    
    assert attempt.error_type == ErrorType.TYPE_ERROR
    assert attempt.status == HealingStatus.FAILED
    assert "exception" in attempt.details.lower()


def test_attempt_heal_max_attempts(healer):
    """Test max attempts limit."""
    # Register mock fix strategy
    def mock_fix(error_msg, context):
        return False
    
    healer.register_fix_strategy("fix_syntax_error", mock_fix)
    
    error_msg = "SyntaxError: invalid syntax"
    
    # First 3 attempts should proceed
    for i in range(3):
        attempt = healer.attempt_heal(error_msg)
        assert attempt.status == HealingStatus.FAILED
    
    # 4th attempt should be skipped
    attempt = healer.attempt_heal(error_msg)
    assert attempt.status == HealingStatus.SKIPPED
    assert "Max attempts" in attempt.details


def test_healing_history(healer):
    """Test healing history tracking."""
    # Register mock fix
    healer.register_fix_strategy("fix_syntax_error", lambda e, c: True)
    
    assert len(healer.healing_history) == 0
    
    healer.attempt_heal("SyntaxError: test")
    assert len(healer.healing_history) == 1
    
    healer.attempt_heal("SyntaxError: test2")
    assert len(healer.healing_history) == 2


def test_get_healing_stats_empty(healer):
    """Test healing stats when no attempts."""
    stats = healer.get_healing_stats()
    
    assert stats["total_attempts"] == 0
    assert stats["success_rate"] == 0.0
    assert stats["by_error_type"] == {}
    assert stats["by_status"] == {}


def test_get_healing_stats(healer):
    """Test healing stats calculation."""
    # Register mock fixes
    healer.register_fix_strategy("fix_syntax_error", lambda e, c: True)
    healer.register_fix_strategy("fix_import_error", lambda e, c: False)
    
    # Make some attempts
    healer.attempt_heal("SyntaxError: test1")  # success
    healer.attempt_heal("SyntaxError: test2")  # success
    healer.attempt_heal("ImportError: test3")  # failure
    healer.attempt_heal("UnknownError: test4")  # skipped
    
    stats = healer.get_healing_stats()
    
    assert stats["total_attempts"] == 4
    assert stats["success_rate"] == 50.0  # 2/4
    assert "syntax_error" in stats["by_error_type"]
    assert stats["by_error_type"]["syntax_error"]["total"] == 2
    assert stats["by_error_type"]["syntax_error"]["success"] == 2
    assert stats["by_status"]["success"] == 2
    assert stats["by_status"]["failed"] == 1
    assert stats["by_status"]["skipped"] == 1


def test_reset_error_attempts_specific(healer):
    """Test resetting specific error attempts."""
    healer.error_attempts["error1"] = 3
    healer.error_attempts["error2"] = 2
    
    healer.reset_error_attempts("error1")
    
    assert "error1" not in healer.error_attempts
    assert healer.error_attempts["error2"] == 2


def test_reset_error_attempts_all(healer):
    """Test resetting all error attempts."""
    healer.error_attempts["error1"] = 3
    healer.error_attempts["error2"] = 2
    
    healer.reset_error_attempts()
    
    assert len(healer.error_attempts) == 0


def test_healing_log_created(healer, temp_log_dir):
    """Test that healing log file is created."""
    # Register mock fix
    healer.register_fix_strategy("fix_syntax_error", lambda e, c: True)
    
    healer.attempt_heal("SyntaxError: test")
    
    log_file = temp_log_dir / "healing_log.txt"
    assert log_file.exists()
    
    content = log_file.read_text()
    assert "syntax_error" in content
    assert "success" in content


def test_error_pattern_priority(healer):
    """Test that highest priority pattern is selected."""
    # Add a custom high-priority pattern
    high_priority = ErrorPattern(
        ErrorType.SYNTAX_ERROR,
        r"SyntaxError",
        "high_priority_fix",
        priority=1,
    )
    
    low_priority = ErrorPattern(
        ErrorType.SYNTAX_ERROR,
        r"SyntaxError",
        "low_priority_fix",
        priority=5,
    )
    
    healer.error_patterns.extend([low_priority, high_priority])
    
    pattern = healer.detect_error_type("SyntaxError: test")
    
    # Should select the original pattern (priority 1) or high_priority
    assert pattern.priority == 1


def test_context_passed_to_fix(healer):
    """Test that context is passed to fix function."""
    context_received = []
    
    def mock_fix(error_msg, context):
        context_received.append(context)
        return True
    
    healer.register_fix_strategy("fix_syntax_error", mock_fix)
    
    healer.attempt_heal("SyntaxError: test", context="file.py:10")
    
    assert len(context_received) == 1
    assert context_received[0] == "file.py:10"
