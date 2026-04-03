"""
Self-Healing System - v6.5.0-SLIM

Monitors error logs in real-time and triggers automatic fix attempts.
Integrates with FailureMemory and HealthMonitor for intelligent recovery.

Features:
- Real-time error log monitoring
- Pattern detection for recurring errors
- Automatic fix attempt triggering
- Healing action logging
- Integration with Circuit Breaker pattern
"""

import re
import time
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ErrorType(Enum):
    """Types of errors that can be auto-healed."""
    SYNTAX_ERROR = "syntax_error"
    IMPORT_ERROR = "import_error"
    TYPE_ERROR = "type_error"
    ATTRIBUTE_ERROR = "attribute_error"
    NAME_ERROR = "name_error"
    INDEX_ERROR = "index_error"
    KEY_ERROR = "key_error"
    FILE_NOT_FOUND = "file_not_found"
    PERMISSION_ERROR = "permission_error"
    UNKNOWN = "unknown"


class HealingStatus(Enum):
    """Status of a healing attempt."""
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    IN_PROGRESS = "in_progress"


@dataclass
class ErrorPattern:
    """Pattern for detecting specific error types."""
    error_type: ErrorType
    regex_pattern: str
    fix_strategy: str
    priority: int = 1  # 1=highest, 5=lowest
    
    def matches(self, error_message: str) -> bool:
        """Check if error message matches this pattern."""
        return bool(re.search(self.regex_pattern, error_message, re.IGNORECASE))


@dataclass
class HealingAttempt:
    """Record of a healing attempt."""
    timestamp: datetime
    error_type: ErrorType
    error_message: str
    fix_strategy: str
    status: HealingStatus
    details: str = ""
    execution_time_ms: float = 0.0


class SelfHealer:
    """
    Self-healing system for automatic error recovery.
    
    Monitors errors, detects patterns, and triggers fixes automatically.
    """
    
    def __init__(
        self,
        log_dir: Path,
        enable_auto_fix: bool = True,
        max_attempts_per_error: int = 3,
    ):
        self.log_dir = Path(log_dir)
        self.enable_auto_fix = enable_auto_fix
        self.max_attempts_per_error = max_attempts_per_error
        
        # Error patterns for detection
        self.error_patterns: List[ErrorPattern] = self._init_error_patterns()
        
        # Healing history
        self.healing_history: List[HealingAttempt] = []
        
        # Error attempt counters
        self.error_attempts: Dict[str, int] = {}
        
        # Fix strategies (callable functions)
        self.fix_strategies: Dict[str, Callable] = {}
        
        # Ensure log directory exists
        self.log_dir.mkdir(parents=True, exist_ok=True)
    
    def _init_error_patterns(self) -> List[ErrorPattern]:
        """Initialize error detection patterns."""
        return [
            # Syntax errors
            ErrorPattern(
                ErrorType.SYNTAX_ERROR,
                r"SyntaxError|invalid syntax|unexpected EOF",
                "fix_syntax_error",
                priority=1,
            ),
            # Import errors
            ErrorPattern(
                ErrorType.IMPORT_ERROR,
                r"ImportError|ModuleNotFoundError|No module named",
                "fix_import_error",
                priority=1,
            ),
            # Type errors
            ErrorPattern(
                ErrorType.TYPE_ERROR,
                r"TypeError|unsupported operand type|not callable",
                "fix_type_error",
                priority=2,
            ),
            # Attribute errors
            ErrorPattern(
                ErrorType.ATTRIBUTE_ERROR,
                r"AttributeError|has no attribute",
                "fix_attribute_error",
                priority=2,
            ),
            # Name errors
            ErrorPattern(
                ErrorType.NAME_ERROR,
                r"NameError|name .* is not defined",
                "fix_name_error",
                priority=2,
            ),
            # Index errors
            ErrorPattern(
                ErrorType.INDEX_ERROR,
                r"IndexError|list index out of range",
                "fix_index_error",
                priority=3,
            ),
            # Key errors
            ErrorPattern(
                ErrorType.KEY_ERROR,
                r"KeyError",
                "fix_key_error",
                priority=3,
            ),
            # File not found
            ErrorPattern(
                ErrorType.FILE_NOT_FOUND,
                r"FileNotFoundError|No such file or directory",
                "fix_file_not_found",
                priority=2,
            ),
            # Permission errors
            ErrorPattern(
                ErrorType.PERMISSION_ERROR,
                r"PermissionError|Permission denied",
                "fix_permission_error",
                priority=4,
            ),
        ]
    
    def register_fix_strategy(
        self,
        strategy_name: str,
        fix_function: Callable[[str, str], bool],
    ):
        """
        Register a fix strategy function.
        
        Args:
            strategy_name: Name of the strategy (e.g., "fix_syntax_error")
            fix_function: Function that takes (error_message, context) and returns success bool
        """
        self.fix_strategies[strategy_name] = fix_function
    
    def detect_error_type(self, error_message: str) -> Optional[ErrorPattern]:
        """
        Detect error type from error message.
        
        Returns the highest priority matching pattern.
        """
        matches = [
            pattern for pattern in self.error_patterns
            if pattern.matches(error_message)
        ]
        
        if not matches:
            return None
        
        # Return highest priority match
        return min(matches, key=lambda p: p.priority)
    
    def should_attempt_fix(self, error_signature: str) -> bool:
        """
        Check if we should attempt to fix this error.
        
        Returns False if:
        - Auto-fix is disabled
        - Max attempts reached for this error
        """
        if not self.enable_auto_fix:
            return False
        
        attempts = self.error_attempts.get(error_signature, 0)
        return attempts < self.max_attempts_per_error
    
    def attempt_heal(
        self,
        error_message: str,
        context: str = "",
    ) -> HealingAttempt:
        """
        Attempt to heal an error.
        
        Args:
            error_message: The error message to heal
            context: Additional context (file path, code snippet, etc.)
        
        Returns:
            HealingAttempt record
        """
        start_time = time.time()
        
        # Detect error type
        pattern = self.detect_error_type(error_message)
        
        if not pattern:
            # Unknown error type
            attempt = HealingAttempt(
                timestamp=datetime.now(),
                error_type=ErrorType.UNKNOWN,
                error_message=error_message,
                fix_strategy="none",
                status=HealingStatus.SKIPPED,
                details="Unknown error type - no pattern matched",
            )
            self.healing_history.append(attempt)
            return attempt
        
        # Create error signature for tracking
        error_signature = f"{pattern.error_type.value}:{error_message[:100]}"
        
        # Check if we should attempt fix
        if not self.should_attempt_fix(error_signature):
            attempt = HealingAttempt(
                timestamp=datetime.now(),
                error_type=pattern.error_type,
                error_message=error_message,
                fix_strategy=pattern.fix_strategy,
                status=HealingStatus.SKIPPED,
                details=f"Max attempts ({self.max_attempts_per_error}) reached",
            )
            self.healing_history.append(attempt)
            return attempt
        
        # Increment attempt counter
        self.error_attempts[error_signature] = self.error_attempts.get(error_signature, 0) + 1
        
        # Get fix strategy
        fix_function = self.fix_strategies.get(pattern.fix_strategy)
        
        if not fix_function:
            attempt = HealingAttempt(
                timestamp=datetime.now(),
                error_type=pattern.error_type,
                error_message=error_message,
                fix_strategy=pattern.fix_strategy,
                status=HealingStatus.FAILED,
                details=f"Fix strategy '{pattern.fix_strategy}' not registered",
            )
            self.healing_history.append(attempt)
            return attempt
        
        # Attempt fix
        try:
            success = fix_function(error_message, context)
            status = HealingStatus.SUCCESS if success else HealingStatus.FAILED
            details = "Fix applied successfully" if success else "Fix failed"
        except Exception as e:
            success = False
            status = HealingStatus.FAILED
            details = f"Fix raised exception: {str(e)}"
        
        execution_time = (time.time() - start_time) * 1000
        
        attempt = HealingAttempt(
            timestamp=datetime.now(),
            error_type=pattern.error_type,
            error_message=error_message,
            fix_strategy=pattern.fix_strategy,
            status=status,
            details=details,
            execution_time_ms=execution_time,
        )
        
        self.healing_history.append(attempt)
        self._log_healing_attempt(attempt)
        
        return attempt
    
    def _log_healing_attempt(self, attempt: HealingAttempt):
        """Log healing attempt to file."""
        log_file = self.log_dir / "healing_log.txt"
        
        log_entry = (
            f"[{attempt.timestamp.isoformat()}] "
            f"{attempt.error_type.value} | "
            f"{attempt.status.value} | "
            f"{attempt.fix_strategy} | "
            f"{attempt.execution_time_ms:.2f}ms | "
            f"{attempt.details}\n"
        )
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
    
    def get_healing_stats(self) -> Dict[str, Any]:
        """Get healing statistics."""
        if not self.healing_history:
            return {
                "total_attempts": 0,
                "success_rate": 0.0,
                "by_error_type": {},
                "by_status": {},
            }
        
        total = len(self.healing_history)
        successes = sum(1 for a in self.healing_history if a.status == HealingStatus.SUCCESS)
        success_rate = (successes / total * 100) if total > 0 else 0.0
        
        # Group by error type
        by_error_type = {}
        for attempt in self.healing_history:
            error_type = attempt.error_type.value
            if error_type not in by_error_type:
                by_error_type[error_type] = {"total": 0, "success": 0}
            by_error_type[error_type]["total"] += 1
            if attempt.status == HealingStatus.SUCCESS:
                by_error_type[error_type]["success"] += 1
        
        # Group by status
        by_status = {}
        for attempt in self.healing_history:
            status = attempt.status.value
            by_status[status] = by_status.get(status, 0) + 1
        
        return {
            "total_attempts": total,
            "success_rate": success_rate,
            "by_error_type": by_error_type,
            "by_status": by_status,
        }
    
    def reset_error_attempts(self, error_signature: Optional[str] = None):
        """
        Reset error attempt counters.
        
        Args:
            error_signature: Specific error to reset, or None to reset all
        """
        if error_signature:
            self.error_attempts.pop(error_signature, None)
        else:
            self.error_attempts.clear()
