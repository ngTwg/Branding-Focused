"""
Tests for Circuit Breaker Pattern - v6.5.0-SLIM
"""

import pytest
import time
from datetime import datetime, timedelta

from antigravity.core.circuit_breaker import (
    CircuitBreaker,
    CircuitState,
    CircuitConfig,
    CircuitStats,
)


@pytest.fixture
def breaker():
    """Create circuit breaker with default config."""
    return CircuitBreaker()


@pytest.fixture
def fast_breaker():
    """Create circuit breaker with fast timeout for testing."""
    config = CircuitConfig(
        failure_threshold=3,
        timeout_seconds=1,  # 1 second timeout
        success_threshold=1,
    )
    return CircuitBreaker(config)


def test_init_default_config():
    """Test initialization with default config."""
    breaker = CircuitBreaker()
    assert breaker.config.failure_threshold == 3
    assert breaker.config.timeout_seconds == 300
    assert breaker.config.success_threshold == 1


def test_init_custom_config():
    """Test initialization with custom config."""
    config = CircuitConfig(
        failure_threshold=5,
        timeout_seconds=60,
        success_threshold=2,
    )
    breaker = CircuitBreaker(config)
    assert breaker.config.failure_threshold == 5
    assert breaker.config.timeout_seconds == 60
    assert breaker.config.success_threshold == 2


def test_config_validation():
    """Test config validation."""
    with pytest.raises(ValueError):
        CircuitConfig(failure_threshold=0)
    
    with pytest.raises(ValueError):
        CircuitConfig(timeout_seconds=0)
    
    with pytest.raises(ValueError):
        CircuitConfig(success_threshold=0)


def test_initial_state(breaker):
    """Test initial circuit state is CLOSED."""
    state = breaker.get_state("test_error")
    assert state == CircuitState.CLOSED


def test_can_attempt_initially(breaker):
    """Test that attempts are allowed initially."""
    assert breaker.can_attempt("test_error") is True


def test_record_success(breaker):
    """Test recording successful attempt."""
    breaker.record_success("test_error")
    stats = breaker.get_stats("test_error")
    
    assert stats.success_count == 1
    assert stats.failure_count == 0
    assert stats.last_success_time is not None


def test_record_failure(breaker):
    """Test recording failed attempt."""
    breaker.record_failure("test_error")
    stats = breaker.get_stats("test_error")
    
    assert stats.failure_count == 1
    assert stats.success_count == 0
    assert stats.last_failure_time is not None


def test_transition_to_open(breaker):
    """Test circuit opens after failure threshold."""
    error_type = "test_error"
    
    # Record failures up to threshold
    for i in range(3):
        assert breaker.get_state(error_type) == CircuitState.CLOSED
        breaker.record_failure(error_type)
    
    # Circuit should now be open
    assert breaker.get_state(error_type) == CircuitState.OPEN


def test_blocked_when_open(breaker):
    """Test that attempts are blocked when circuit is open."""
    error_type = "test_error"
    
    # Open the circuit
    for i in range(3):
        breaker.record_failure(error_type)
    
    # Attempts should be blocked
    assert breaker.can_attempt(error_type) is False
    
    stats = breaker.get_stats(error_type)
    assert stats.total_blocked == 1


def test_transition_to_half_open(fast_breaker):
    """Test circuit transitions to half-open after timeout."""
    error_type = "test_error"
    
    # Open the circuit
    for i in range(3):
        fast_breaker.record_failure(error_type)
    
    assert fast_breaker.get_state(error_type) == CircuitState.OPEN
    
    # Wait for timeout
    time.sleep(1.1)
    
    # Should transition to half-open
    assert fast_breaker.get_state(error_type) == CircuitState.HALF_OPEN


def test_half_open_allows_attempts(fast_breaker):
    """Test that half-open state allows attempts."""
    error_type = "test_error"
    
    # Open the circuit
    for i in range(3):
        fast_breaker.record_failure(error_type)
    
    # Wait for timeout
    time.sleep(1.1)
    
    # Should allow attempt in half-open
    assert fast_breaker.can_attempt(error_type) is True


def test_half_open_to_closed_on_success(fast_breaker):
    """Test circuit closes from half-open after success."""
    error_type = "test_error"
    
    # Open the circuit
    for i in range(3):
        fast_breaker.record_failure(error_type)
    
    # Wait for timeout
    time.sleep(1.1)
    
    # Trigger half-open transition
    fast_breaker.get_state(error_type)
    
    # Record success
    fast_breaker.record_success(error_type)
    
    # Should be closed now
    assert fast_breaker.get_state(error_type) == CircuitState.CLOSED


def test_half_open_to_open_on_failure(fast_breaker):
    """Test circuit reopens from half-open after failure."""
    error_type = "test_error"
    
    # Open the circuit
    for i in range(3):
        fast_breaker.record_failure(error_type)
    
    # Wait for timeout
    time.sleep(1.1)
    
    # Trigger half-open transition
    fast_breaker.get_state(error_type)
    
    # Record failure
    fast_breaker.record_failure(error_type)
    
    # Should be open again
    assert fast_breaker.get_state(error_type) == CircuitState.OPEN


def test_success_resets_failure_count(breaker):
    """Test that success resets failure count."""
    error_type = "test_error"
    
    # Record some failures
    breaker.record_failure(error_type)
    breaker.record_failure(error_type)
    
    stats = breaker.get_stats(error_type)
    assert stats.failure_count == 2
    
    # Record success
    breaker.record_success(error_type)
    
    stats = breaker.get_stats(error_type)
    assert stats.failure_count == 0
    assert stats.success_count == 1


def test_failure_resets_success_count(breaker):
    """Test that failure resets success count."""
    error_type = "test_error"
    
    # Record some successes
    breaker.record_success(error_type)
    breaker.record_success(error_type)
    
    stats = breaker.get_stats(error_type)
    assert stats.success_count == 2
    
    # Record failure
    breaker.record_failure(error_type)
    
    stats = breaker.get_stats(error_type)
    assert stats.success_count == 0
    assert stats.failure_count == 1


def test_multiple_error_types(breaker):
    """Test handling multiple error types independently."""
    # Open circuit for error1
    for i in range(3):
        breaker.record_failure("error1")
    
    # error1 should be open
    assert breaker.get_state("error1") == CircuitState.OPEN
    
    # error2 should still be closed
    assert breaker.get_state("error2") == CircuitState.CLOSED
    assert breaker.can_attempt("error2") is True


def test_state_transitions_logged(breaker):
    """Test that state transitions are logged."""
    error_type = "test_error"
    
    # Open the circuit
    for i in range(3):
        breaker.record_failure(error_type)
    
    stats = breaker.get_stats(error_type)
    
    # Should have transition from CLOSED to OPEN
    assert len(stats.state_transitions) == 1
    transition = stats.state_transitions[0]
    assert transition["from"] == "closed"
    assert transition["to"] == "open"
    assert "threshold" in transition["reason"].lower()


def test_reset_specific_circuit(breaker):
    """Test resetting specific circuit."""
    error_type = "test_error"
    
    # Open the circuit
    for i in range(3):
        breaker.record_failure(error_type)
    
    assert breaker.get_state(error_type) == CircuitState.OPEN
    
    # Reset
    breaker.reset(error_type)
    
    # Should be closed now
    assert breaker.get_state(error_type) == CircuitState.CLOSED
    stats = breaker.get_stats(error_type)
    assert stats.failure_count == 0
    assert stats.success_count == 0


def test_reset_all_circuits(breaker):
    """Test resetting all circuits."""
    # Open multiple circuits
    for i in range(3):
        breaker.record_failure("error1")
        breaker.record_failure("error2")
    
    assert breaker.get_state("error1") == CircuitState.OPEN
    assert breaker.get_state("error2") == CircuitState.OPEN
    
    # Reset all
    breaker.reset()
    
    # All should be closed
    assert breaker.get_state("error1") == CircuitState.CLOSED
    assert breaker.get_state("error2") == CircuitState.CLOSED


def test_force_open(breaker):
    """Test forcing circuit to open."""
    error_type = "test_error"
    
    assert breaker.get_state(error_type) == CircuitState.CLOSED
    
    breaker.force_open(error_type, "Testing")
    
    assert breaker.get_state(error_type) == CircuitState.OPEN


def test_force_close(breaker):
    """Test forcing circuit to close."""
    error_type = "test_error"
    
    # Open the circuit
    for i in range(3):
        breaker.record_failure(error_type)
    
    assert breaker.get_state(error_type) == CircuitState.OPEN
    
    breaker.force_close(error_type, "Testing")
    
    assert breaker.get_state(error_type) == CircuitState.CLOSED


def test_callbacks_on_open(breaker):
    """Test callbacks are triggered when circuit opens."""
    callback_called = []
    
    def on_open(error_type, stats):
        callback_called.append((error_type, stats.state))
    
    breaker.register_callback(CircuitState.OPEN, on_open)
    
    # Open the circuit
    for i in range(3):
        breaker.record_failure("test_error")
    
    assert len(callback_called) == 1
    assert callback_called[0][0] == "test_error"
    assert callback_called[0][1] == CircuitState.OPEN


def test_callbacks_on_close(fast_breaker):
    """Test callbacks are triggered when circuit closes."""
    callback_called = []
    
    def on_close(error_type, stats):
        callback_called.append((error_type, stats.state))
    
    fast_breaker.register_callback(CircuitState.CLOSED, on_close)
    
    # Open the circuit
    for i in range(3):
        fast_breaker.record_failure("test_error")
    
    # Wait and transition to half-open
    time.sleep(1.1)
    fast_breaker.get_state("test_error")
    
    # Close the circuit
    fast_breaker.record_success("test_error")
    
    assert len(callback_called) == 1
    assert callback_called[0][0] == "test_error"
    assert callback_called[0][1] == CircuitState.CLOSED


def test_get_summary(breaker):
    """Test getting summary of all circuits."""
    # Create some circuits in different states
    for i in range(3):
        breaker.can_attempt("error1")  # Track attempts
        breaker.record_failure("error1")  # Open
    
    breaker.can_attempt("error2")  # Track attempt
    breaker.record_success("error2")  # Closed
    
    summary = breaker.get_summary()
    
    assert summary["total_circuits"] == 2
    assert summary["open"] == 1
    assert summary["closed"] == 1
    assert summary["total_attempts"] == 4  # 3 for error1 + 1 for error2


def test_total_attempts_tracked(breaker):
    """Test that total attempts are tracked."""
    error_type = "test_error"
    
    # Make some attempts
    breaker.can_attempt(error_type)
    breaker.can_attempt(error_type)
    breaker.can_attempt(error_type)
    
    stats = breaker.get_stats(error_type)
    assert stats.total_attempts == 3


def test_total_blocked_tracked(breaker):
    """Test that blocked attempts are tracked."""
    error_type = "test_error"
    
    # Open the circuit
    for i in range(3):
        breaker.record_failure(error_type)
    
    # Try to make attempts (should be blocked)
    breaker.can_attempt(error_type)
    breaker.can_attempt(error_type)
    
    stats = breaker.get_stats(error_type)
    assert stats.total_blocked == 2


def test_opened_at_timestamp(breaker):
    """Test that opened_at timestamp is set."""
    error_type = "test_error"
    
    # Open the circuit
    for i in range(3):
        breaker.record_failure(error_type)
    
    stats = breaker.get_stats(error_type)
    assert stats.opened_at is not None
    assert isinstance(stats.opened_at, datetime)


def test_get_all_stats(breaker):
    """Test getting stats for all circuits."""
    breaker.record_failure("error1")
    breaker.record_success("error2")
    
    all_stats = breaker.get_all_stats()
    
    assert len(all_stats) == 2
    assert "error1" in all_stats
    assert "error2" in all_stats
