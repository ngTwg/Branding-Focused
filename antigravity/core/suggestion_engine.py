"""
Suggestion Engine for Antigravity v6.2 - Task 22.

This module provides a rule-based suggestion system with priority scoring
for actionable recommendations to improve system performance.

Phase 6: Self-Evaluation - Task 22 (Actionable Suggestions)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class SuggestionPriority(Enum):
    """Priority levels for suggestions."""
    CRITICAL = 1  # Immediate action required
    HIGH = 2      # Important, should address soon
    MEDIUM = 3    # Moderate importance
    LOW = 4       # Nice to have


@dataclass
class Suggestion:
    """
    A single actionable suggestion with priority.
    
    Attributes:
        message: The suggestion text
        priority: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
        reason: Explanation of why this suggestion was triggered
        metric_value: The metric value that triggered this suggestion (optional)
    """
    message: str
    priority: SuggestionPriority
    reason: str
    metric_value: float | None = None
    
    def __str__(self) -> str:
        """Format suggestion for display."""
        if self.metric_value is not None:
            return f"[{self.priority.name}] {self.message} ({self.reason}: {self.metric_value:.1%})"
        return f"[{self.priority.name}] {self.message} ({self.reason})"


class MetricsProvider(Protocol):
    """Protocol for objects that provide metrics for suggestion evaluation."""
    
    def get_stale_ratio(self) -> float:
        """Get the ratio of stale embeddings (0.0-1.0)."""
        ...
    
    def get_rollback_rate(self) -> float:
        """Get the rollback rate (0.0-1.0)."""
        ...
    
    def get_red_zone_ratio(self) -> float:
        """Get the ratio of time spent in red budget zone (0.0-1.0)."""
        ...
    
    def get_slm_usage_ratio(self) -> float:
        """Get the ratio of SLM usage vs total (0.0-1.0)."""
        ...
    
    def get_token_efficiency_ratio(self) -> float:
        """Get current token usage vs baseline (1.0 = baseline, >1.0 = worse)."""
        ...
    
    def get_success_rate(self) -> float:
        """Get the success rate (0.0-1.0)."""
        ...


class SuggestionEngine:
    """
    Rule-based suggestion system with priority scoring.
    
    The SuggestionEngine evaluates system metrics against predefined rules
    and generates prioritized, actionable suggestions for improvement.
    
    Rules (Task 22.2):
        1. High stale_ratio (>20%) → "Re-index skills" (HIGH)
        2. High rollback_rate (>15%) → "Review error detection" (HIGH)
        3. Frequent Red zone (>30%) → "Increase budget" (MEDIUM)
        4. Low SLM usage (<20%) → "Check SLM router" (LOW)
        5. High token per task (>baseline*1.5) → "Optimize prompts" (MEDIUM)
        6. Low success rate (<70%) → "Review skill retrieval" (CRITICAL)
    
    Usage:
        engine = SuggestionEngine()
        suggestions = engine.get_top_suggestions(
            metrics_provider=my_metrics,
            max_count=3
        )
    """
    
    def __init__(self):
        """Initialize the SuggestionEngine."""
        # Rule thresholds (configurable)
        self.stale_ratio_threshold = 0.20  # 20%
        self.rollback_rate_threshold = 0.15  # 15%
        self.red_zone_threshold = 0.30  # 30%
        self.slm_usage_threshold = 0.20  # 20%
        self.token_efficiency_threshold = 1.5  # 150% of baseline
        self.success_rate_threshold = 0.70  # 70%
    
    def evaluate_rule_1_stale_index(self, metrics: MetricsProvider) -> Suggestion | None:
        """
        Rule 1: High stale_ratio (>20%) → "Re-index skills" (HIGH)
        
        Args:
            metrics: Metrics provider with get_stale_ratio() method
        
        Returns:
            Suggestion if rule triggered, None otherwise
        """
        try:
            stale_ratio = metrics.get_stale_ratio()
            if stale_ratio > self.stale_ratio_threshold:
                return Suggestion(
                    message="Re-index skills to maintain retrieval quality",
                    priority=SuggestionPriority.HIGH,
                    reason=f"Stale ratio: {stale_ratio:.1%}",
                    metric_value=stale_ratio
                )
        except (AttributeError, NotImplementedError):
            # Metrics provider doesn't support this metric
            pass
        return None
    
    def evaluate_rule_2_high_rollback(self, metrics: MetricsProvider) -> Suggestion | None:
        """
        Rule 2: High rollback_rate (>15%) → "Review error detection" (HIGH)
        
        Args:
            metrics: Metrics provider with get_rollback_rate() method
        
        Returns:
            Suggestion if rule triggered, None otherwise
        """
        try:
            rollback_rate = metrics.get_rollback_rate()
            if rollback_rate > self.rollback_rate_threshold:
                return Suggestion(
                    message="Review error detection logic in ASTAnalyzer",
                    priority=SuggestionPriority.HIGH,
                    reason=f"Rollback rate: {rollback_rate:.1%}",
                    metric_value=rollback_rate
                )
        except (AttributeError, NotImplementedError):
            pass
        return None
    
    def evaluate_rule_3_red_zone(self, metrics: MetricsProvider) -> Suggestion | None:
        """
        Rule 3: Frequent Red zone (>30%) → "Increase budget" (MEDIUM)
        
        Args:
            metrics: Metrics provider with get_red_zone_ratio() method
        
        Returns:
            Suggestion if rule triggered, None otherwise
        """
        try:
            red_zone_ratio = metrics.get_red_zone_ratio()
            if red_zone_ratio > self.red_zone_threshold:
                return Suggestion(
                    message="Increase budget limits or optimize token usage",
                    priority=SuggestionPriority.MEDIUM,
                    reason=f"Red zone time: {red_zone_ratio:.1%}",
                    metric_value=red_zone_ratio
                )
        except (AttributeError, NotImplementedError):
            pass
        return None
    
    def evaluate_rule_4_low_slm(self, metrics: MetricsProvider) -> Suggestion | None:
        """
        Rule 4: Low SLM usage (<20%) → "Check SLM router" (LOW)
        
        Args:
            metrics: Metrics provider with get_slm_usage_ratio() method
        
        Returns:
            Suggestion if rule triggered, None otherwise
        """
        try:
            slm_ratio = metrics.get_slm_usage_ratio()
            if slm_ratio < self.slm_usage_threshold:
                return Suggestion(
                    message="Check SLM router configuration and thresholds",
                    priority=SuggestionPriority.LOW,
                    reason=f"SLM usage: {slm_ratio:.1%}",
                    metric_value=slm_ratio
                )
        except (AttributeError, NotImplementedError):
            pass
        return None
    
    def evaluate_rule_5_high_tokens(self, metrics: MetricsProvider) -> Suggestion | None:
        """
        Rule 5: High token per task (>baseline*1.5) → "Optimize prompts" (MEDIUM)
        
        Args:
            metrics: Metrics provider with get_token_efficiency_ratio() method
        
        Returns:
            Suggestion if rule triggered, None otherwise
        """
        try:
            token_ratio = metrics.get_token_efficiency_ratio()
            if token_ratio > self.token_efficiency_threshold:
                return Suggestion(
                    message="Optimize prompt length and retrieval top_k",
                    priority=SuggestionPriority.MEDIUM,
                    reason=f"Token usage: {token_ratio:.1f}x baseline",
                    metric_value=token_ratio
                )
        except (AttributeError, NotImplementedError):
            pass
        return None
    
    def evaluate_rule_6_low_success(self, metrics: MetricsProvider) -> Suggestion | None:
        """
        Rule 6: Low success rate (<70%) → "Review skill retrieval" (CRITICAL)
        
        Args:
            metrics: Metrics provider with get_success_rate() method
        
        Returns:
            Suggestion if rule triggered, None otherwise
        """
        try:
            success_rate = metrics.get_success_rate()
            if success_rate < self.success_rate_threshold:
                return Suggestion(
                    message="Review skill retrieval quality and repair logic",
                    priority=SuggestionPriority.CRITICAL,
                    reason=f"Success rate: {success_rate:.1%}",
                    metric_value=success_rate
                )
        except (AttributeError, NotImplementedError):
            pass
        return None
    
    def evaluate_all_rules(self, metrics: MetricsProvider) -> list[Suggestion]:
        """
        Evaluate all suggestion rules against provided metrics.
        
        Args:
            metrics: Metrics provider implementing MetricsProvider protocol
        
        Returns:
            List of triggered suggestions (may be empty)
        """
        suggestions = []
        
        # Evaluate each rule
        rules = [
            self.evaluate_rule_1_stale_index,
            self.evaluate_rule_2_high_rollback,
            self.evaluate_rule_3_red_zone,
            self.evaluate_rule_4_low_slm,
            self.evaluate_rule_5_high_tokens,
            self.evaluate_rule_6_low_success,
        ]
        
        for rule in rules:
            suggestion = rule(metrics)
            if suggestion is not None:
                suggestions.append(suggestion)
        
        return suggestions
    
    def get_top_suggestions(
        self,
        metrics: MetricsProvider,
        max_count: int = 3
    ) -> list[str]:
        """
        Get top-N suggestions sorted by priority (Task 22.3).
        
        This method:
        1. Evaluates all rules against provided metrics
        2. Sorts suggestions by priority (CRITICAL > HIGH > MEDIUM > LOW)
        3. Returns top-N suggestion messages
        
        Args:
            metrics: Metrics provider implementing MetricsProvider protocol
            max_count: Maximum number of suggestions to return (default: 3)
        
        Returns:
            List of suggestion message strings, sorted by priority (most critical first)
        
        Example:
            >>> engine = SuggestionEngine()
            >>> suggestions = engine.get_top_suggestions(my_metrics, max_count=3)
            >>> for suggestion in suggestions:
            ...     print(suggestion)
            [CRITICAL] Review skill retrieval quality and repair logic (Success rate: 65.0%)
            [HIGH] Re-index skills to maintain retrieval quality (Stale ratio: 25.0%)
            [HIGH] Review error detection logic in ASTAnalyzer (Rollback rate: 18.0%)
        """
        # Evaluate all rules
        suggestions = self.evaluate_all_rules(metrics)
        
        # Sort by priority (CRITICAL=1, HIGH=2, MEDIUM=3, LOW=4)
        # Lower priority value = higher importance
        suggestions.sort(key=lambda s: s.priority.value)
        
        # Take top-N and convert to strings
        top_suggestions = suggestions[:max_count]
        
        return [str(s) for s in top_suggestions]
