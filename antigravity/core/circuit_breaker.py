"""
Circuit Breaker Pattern - v6.5.0-SLIM

Prevents repeated failed fix attempts by tracking failure patterns.
Implements three states: CLOSED, OPEN, HALF_OPEN.

States:
- CLOSED: Normal operation, attempts allowed
- OPEN: Too many failures, attempts blocked
- HALF_OPEN: Testing if system recovered, limited attempts

Transitions:
- CLOSED -> OPEN: After N consecutive failures
- OPEN -> HALF_OPEN: After timeout period
- HALF_OPEN -> CLOSED: After successful attempt
- HALF_OPEN -> OPEN: After failed attempt
"""

import time
from enum import Enum
from typing import Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Blocking attempts
    HALF_OPEN = "half_open"  # Testing recovery


@dataclass
class CircuitConfig:
    """Configuration for circuit breaker."""
    failure_threshold: int = 3  # Failures before opening
    timeout_seconds: int = 300  # 5 minutes before half-open
    success_threshold: int = 1  # Successes to close from half-open
    
    def __post_init__(self):
        """Validate configuration."""
        if self.failure_threshold < 1:
            raise ValueError("failure_threshold must be >= 1")
        if self.timeout_seconds < 1:
            raise ValueError("timeout_seconds must be >= 1")
        if self.success_threshold < 1:
            raise ValueError("success_threshold must be >= 1")


@dataclass
class CircuitStats:
    """Statistics for a circuit breaker."""
    error_type: str
    state: CircuitState
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[datetime] = None
    last_success_time: Optional[datetime] = None
    opened_at: Optional[datetime] = None
    total_attempts: int = 0
    total_blocked: int = 0
    state_transitions: list = field(default_factory=list)


class CircuitBreaker:
    """
    Circuit Breaker for error recovery attempts.
    
    Tracks fix attempts per error type and prevents repeated failures
    by opening the circuit after threshold is reached.
    """
    
    def __init__(self, config: Optional[CircuitConfig] = None):
        self.config = config or CircuitConfig()
        
        # Circuit state per error type
        self.circuits: Dict[str, CircuitStats] = {}
        
        # Callbacks for state transitions
        self.on_open_callbacks: list[Callable] = []
        self.on_close_callbacks: list[Callable] = []
        self.on_half_open_callbacks: list[Callable] = []
    
    def register_callback(
        self,
        state: CircuitState,
        callback: Callable[[str, CircuitStats], None],
    ):
        """
        Register callback for state transitions.
        
        Args:
            state: State to trigger callback (OPEN, CLOSED, HALF_OPEN)
            callback: Function(error_type, stats) to call
        """
        if state == CircuitState.OPEN:
            self.on_open_callbacks.append(callback)
        elif state == CircuitState.CLOSED:
            self.on_close_callbacks.append(callback)
        elif state == CircuitState.HALF_OPEN:
            self.on_half_open_callbacks.append(callback)
    
    def _get_or_create_circuit(self, error_type: str) -> CircuitStats:
        """Get or create circuit stats for error type."""
        if error_type not in self.circuits:
            self.circuits[error_type] = CircuitStats(
                error_type=error_type,
                state=CircuitState.CLOSED,
            )
        return self.circuits[error_type]
    
    def _transition_to(
        self,
        error_type: str,
        new_state: CircuitState,
        reason: str = "",
    ):
        """Transition circuit to new state."""
        stats = self._get_or_create_circuit(error_type)
        old_state = stats.state
        
        if old_state == new_state:
            return  # No transition
        
        stats.state = new_state
        stats.state_transitions.append({
            "timestamp": datetime.now(),
            "from": old_state.value,
            "to": new_state.value,
            "reason": reason,
        })
        
        # Track when circuit opened
        if new_state == CircuitState.OPEN:
            stats.opened_at = datetime.now()
        
        # Trigger callbacks
        if new_state == CircuitState.OPEN:
            for callback in self.on_open_callbacks:
                try:
                    callback(error_type, stats)
                except Exception:
                    pass  # Don't let callback errors break circuit
        elif new_state == CircuitState.CLOSED:
            for callback in self.on_close_callbacks:
                try:
                    callback(error_type, stats)
                except Exception:
                    pass
        elif new_state == CircuitState.HALF_OPEN:
            for callback in self.on_half_open_callbacks:
                try:
                    callback(error_type, stats)
                except Exception:
                    pass
    
    def _should_attempt_half_open(self, stats: CircuitStats) -> bool:
        """Check if circuit should transition to half-open."""
        if stats.state != CircuitState.OPEN:
            return False
        
        if not stats.opened_at:
            return False
        
        elapsed = (datetime.now() - stats.opened_at).total_seconds()
        return elapsed >= self.config.timeout_seconds
    
    def can_attempt(self, error_type: str) -> bool:
        """
        Check if fix attempt is allowed for this error type.
        
        Returns:
            True if attempt allowed, False if circuit is open
        """
        stats = self._get_or_create_circuit(error_type)
        
        # Check if we should transition to half-open
        if self._should_attempt_half_open(stats):
            self._transition_to(
                error_type,
                CircuitState.HALF_OPEN,
                f"Timeout elapsed ({self.config.timeout_seconds}s)",
            )
        
        # Allow attempts in CLOSED and HALF_OPEN states
        if stats.state in (CircuitState.CLOSED, CircuitState.HALF_OPEN):
            stats.total_attempts += 1
            return True
        
        # Block attempts in OPEN state
        stats.total_blocked += 1
        return False
    
    def record_success(self, error_type: str):
        """
        Record successful fix attempt.
        
        May transition circuit from HALF_OPEN to CLOSED.
        """
        stats = self._get_or_create_circuit(error_type)
        stats.success_count += 1
        stats.last_success_time = datetime.now()
        
        # Reset failure count on success
        stats.failure_count = 0
        
        # Transition based on current state
        if stats.state == CircuitState.HALF_OPEN:
            # Check if we have enough successes to close
            if stats.success_count >= self.config.success_threshold:
                self._transition_to(
                    error_type,
                    CircuitState.CLOSED,
                    f"Success threshold reached ({self.config.success_threshold})",
                )
        elif stats.state == CircuitState.OPEN:
            # Shouldn't happen, but handle gracefully
            self._transition_to(
                error_type,
                CircuitState.CLOSED,
                "Unexpected success while open",
            )
    
    def record_failure(self, error_type: str):
        """
        Record failed fix attempt.
        
        May transition circuit from CLOSED to OPEN, or HALF_OPEN to OPEN.
        """
        stats = self._get_or_create_circuit(error_type)
        stats.failure_count += 1
        stats.last_failure_time = datetime.now()
        
        # Reset success count on failure
        stats.success_count = 0
        
        # Transition based on current state
        if stats.state == CircuitState.CLOSED:
            # Check if we've hit failure threshold
            if stats.failure_count >= self.config.failure_threshold:
                self._transition_to(
                    error_type,
                    CircuitState.OPEN,
                    f"Failure threshold reached ({self.config.failure_threshold})",
                )
        elif stats.state == CircuitState.HALF_OPEN:
            # Any failure in half-open immediately opens circuit
            self._transition_to(
                error_type,
                CircuitState.OPEN,
                "Failed while testing recovery",
            )
    
    def get_state(self, error_type: str) -> CircuitState:
        """Get current state of circuit for error type."""
        stats = self._get_or_create_circuit(error_type)
        
        # Check if we should transition to half-open
        if self._should_attempt_half_open(stats):
            self._transition_to(
                error_type,
                CircuitState.HALF_OPEN,
                f"Timeout elapsed ({self.config.timeout_seconds}s)",
            )
        
        return stats.state
    
    def get_stats(self, error_type: str) -> CircuitStats:
        """Get statistics for error type."""
        return self._get_or_create_circuit(error_type)
    
    def get_all_stats(self) -> Dict[str, CircuitStats]:
        """Get statistics for all circuits."""
        return self.circuits.copy()
    
    def reset(self, error_type: Optional[str] = None):
        """
        Reset circuit breaker.
        
        Args:
            error_type: Specific error to reset, or None to reset all
        """
        if error_type:
            if error_type in self.circuits:
                self._transition_to(
                    error_type,
                    CircuitState.CLOSED,
                    "Manual reset",
                )
                stats = self.circuits[error_type]
                stats.failure_count = 0
                stats.success_count = 0
        else:
            # Reset all circuits
            for error_type in list(self.circuits.keys()):
                self.reset(error_type)
    
    def force_open(self, error_type: str, reason: str = "Manual override"):
        """Force circuit to open state."""
        self._transition_to(error_type, CircuitState.OPEN, reason)
    
    def force_close(self, error_type: str, reason: str = "Manual override"):
        """Force circuit to closed state."""
        stats = self._get_or_create_circuit(error_type)
        stats.failure_count = 0
        stats.success_count = 0
        self._transition_to(error_type, CircuitState.CLOSED, reason)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all circuits."""
        total_circuits = len(self.circuits)
        open_circuits = sum(
            1 for s in self.circuits.values()
            if s.state == CircuitState.OPEN
        )
        half_open_circuits = sum(
            1 for s in self.circuits.values()
            if s.state == CircuitState.HALF_OPEN
        )
        closed_circuits = sum(
            1 for s in self.circuits.values()
            if s.state == CircuitState.CLOSED
        )
        
        total_attempts = sum(s.total_attempts for s in self.circuits.values())
        total_blocked = sum(s.total_blocked for s in self.circuits.values())
        
        return {
            "total_circuits": total_circuits,
            "open": open_circuits,
            "half_open": half_open_circuits,
            "closed": closed_circuits,
            "total_attempts": total_attempts,
            "total_blocked": total_blocked,
            "block_rate": (total_blocked / total_attempts * 100)
            if total_attempts > 0 else 0.0,
        }
