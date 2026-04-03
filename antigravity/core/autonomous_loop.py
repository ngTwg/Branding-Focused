"""
Autonomous Loop - v6.5.0-SLIM

Main self-healing loop: monitor → detect → fix → verify

Integrates:
- SelfHealer: Automatic fix attempts
- CircuitBreaker: Prevents repeated failures
- FailureMemory: Learns from past failures
- HealthMonitor: System health tracking
"""

import time
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Callable
from dataclasses import dataclass
from datetime import datetime

from antigravity.core.self_healer import SelfHealer, ErrorType, HealingStatus
from antigravity.core.circuit_breaker import CircuitBreaker, CircuitState


logger = logging.getLogger(__name__)


@dataclass
class LoopConfig:
    """Configuration for autonomous loop."""
    enabled: bool = True
    check_interval_seconds: int = 60  # Check every minute
    max_concurrent_fixes: int = 3  # Max fixes at once
    enable_per_error_type: Dict[str, bool] = None  # Enable/disable per error type
    
    def __post_init__(self):
        if self.enable_per_error_type is None:
            self.enable_per_error_type = {}


class AutonomousLoop:
    """
    Autonomous self-healing loop.
    
    Continuously monitors for errors and attempts automatic fixes.
    """
    
    def __init__(
        self,
        self_healer: SelfHealer,
        circuit_breaker: CircuitBreaker,
        config: Optional[LoopConfig] = None,
    ):
        self.healer = self_healer
        self.breaker = circuit_breaker
        self.config = config or LoopConfig()
        
        # Running state
        self.is_running = False
        self.active_fixes = 0
        
        # Statistics
        self.total_errors_detected = 0
        self.total_fixes_attempted = 0
        self.total_fixes_succeeded = 0
        self.total_fixes_blocked = 0
        
        # Error detection callbacks
        self.error_detectors: list[Callable[[], list[tuple[str, str]]]] = []
        
        # Verification callbacks
        self.verifiers: Dict[str, Callable[[str], bool]] = {}
    
    def register_error_detector(
        self,
        detector: Callable[[], list[tuple[str, str]]],
    ):
        """
        Register error detector function.
        
        Args:
            detector: Function that returns list of (error_message, context) tuples
        """
        self.error_detectors.append(detector)
    
    def register_verifier(
        self,
        error_type: str,
        verifier: Callable[[str], bool],
    ):
        """
        Register verification function for error type.
        
        Args:
            error_type: Type of error (e.g., "syntax_error")
            verifier: Function(context) that returns True if fix verified
        """
        self.verifiers[error_type] = verifier
    
    def is_enabled_for_error(self, error_type: str) -> bool:
        """Check if autonomous fixing is enabled for this error type."""
        if not self.config.enabled:
            return False
        
        # Check per-error-type config
        if error_type in self.config.enable_per_error_type:
            return self.config.enable_per_error_type[error_type]
        
        # Default: enabled
        return True
    
    def detect_errors(self) -> list[tuple[str, str]]:
        """
        Detect errors using registered detectors.
        
        Returns:
            List of (error_message, context) tuples
        """
        errors = []
        for detector in self.error_detectors:
            try:
                detected = detector()
                errors.extend(detected)
            except Exception as e:
                logger.error(f"Error detector failed: {e}")
        
        return errors
    
    def attempt_fix(
        self,
        error_message: str,
        context: str = "",
    ) -> bool:
        """
        Attempt to fix an error.
        
        Returns:
            True if fix succeeded, False otherwise
        """
        # Detect error type
        pattern = self.healer.detect_error_type(error_message)
        if not pattern:
            logger.warning(f"Unknown error type: {error_message[:100]}")
            return False
        
        error_type = pattern.error_type.value
        
        # Check if enabled for this error type
        if not self.is_enabled_for_error(error_type):
            logger.info(f"Auto-fix disabled for {error_type}")
            return False
        
        # Check circuit breaker
        if not self.breaker.can_attempt(error_type):
            logger.info(f"Circuit breaker blocking {error_type}")
            self.total_fixes_blocked += 1
            return False
        
        # Attempt healing
        self.total_fixes_attempted += 1
        self.active_fixes += 1
        
        try:
            attempt = self.healer.attempt_heal(error_message, context)
            
            # Record result in circuit breaker
            if attempt.status == HealingStatus.SUCCESS:
                self.breaker.record_success(error_type)
                self.total_fixes_succeeded += 1
                
                # Verify fix if verifier registered
                if error_type in self.verifiers:
                    verified = self.verifiers[error_type](context)
                    if not verified:
                        logger.warning(f"Fix not verified for {error_type}")
                        self.breaker.record_failure(error_type)
                        return False
                
                logger.info(f"Successfully fixed {error_type}")
                return True
            else:
                self.breaker.record_failure(error_type)
                logger.warning(f"Failed to fix {error_type}: {attempt.details}")
                return False
        
        finally:
            self.active_fixes -= 1
    
    def run_cycle(self) -> Dict[str, Any]:
        """
        Run one cycle of the autonomous loop.
        
        Returns:
            Statistics for this cycle
        """
        cycle_start = time.time()
        
        # Detect errors
        errors = self.detect_errors()
        self.total_errors_detected += len(errors)
        
        # Track cycle stats
        fixes_attempted = 0
        fixes_succeeded = 0
        fixes_blocked = 0
        
        # Attempt fixes (up to max concurrent)
        for error_message, context in errors:
            if self.active_fixes >= self.config.max_concurrent_fixes:
                logger.info("Max concurrent fixes reached, skipping remaining errors")
                break
            
            success = self.attempt_fix(error_message, context)
            fixes_attempted += 1
            if success:
                fixes_succeeded += 1
        
        cycle_time = (time.time() - cycle_start) * 1000
        
        return {
            "errors_detected": len(errors),
            "fixes_attempted": fixes_attempted,
            "fixes_succeeded": fixes_succeeded,
            "fixes_blocked": fixes_blocked,
            "cycle_time_ms": cycle_time,
        }
    
    def start(self):
        """Start the autonomous loop (non-blocking)."""
        if self.is_running:
            logger.warning("Autonomous loop already running")
            return
        
        self.is_running = True
        logger.info("Autonomous loop started")
    
    def stop(self):
        """Stop the autonomous loop."""
        if not self.is_running:
            logger.warning("Autonomous loop not running")
            return
        
        self.is_running = False
        logger.info("Autonomous loop stopped")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get autonomous loop statistics."""
        healing_stats = self.healer.get_healing_stats()
        breaker_summary = self.breaker.get_summary()
        
        return {
            "is_running": self.is_running,
            "total_errors_detected": self.total_errors_detected,
            "total_fixes_attempted": self.total_fixes_attempted,
            "total_fixes_succeeded": self.total_fixes_succeeded,
            "total_fixes_blocked": self.total_fixes_blocked,
            "success_rate": (
                self.total_fixes_succeeded / self.total_fixes_attempted * 100
                if self.total_fixes_attempted > 0 else 0.0
            ),
            "active_fixes": self.active_fixes,
            "healing_stats": healing_stats,
            "circuit_breaker": breaker_summary,
        }
    
    def enable_error_type(self, error_type: str):
        """Enable autonomous fixing for specific error type."""
        self.config.enable_per_error_type[error_type] = True
        logger.info(f"Enabled auto-fix for {error_type}")
    
    def disable_error_type(self, error_type: str):
        """Disable autonomous fixing for specific error type."""
        self.config.enable_per_error_type[error_type] = False
        logger.info(f"Disabled auto-fix for {error_type}")
