"""
Unit tests for SuggestionEngine (Task 22).

Tests cover:
- Individual rule evaluation
- Priority sorting
- Top-N suggestion selection
- Integration with HealthMonitor

Requirements: 6.3 (Task 22.1-22.4)
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from antigravity.core.suggestion_engine import (
    SuggestionEngine,
    SuggestionPriority,
    Suggestion
)


class MockMetricsProvider:
    """Mock metrics provider for testing."""
    
    def __init__(
        self,
        stale_ratio=0.0,
        rollback_rate=0.0,
        red_zone_ratio=0.0,
        slm_usage_ratio=1.0,
        token_efficiency_ratio=1.0,
        success_rate=1.0
    ):
        self._stale_ratio = stale_ratio
        self._rollback_rate = rollback_rate
        self._red_zone_ratio = red_zone_ratio
        self._slm_usage_ratio = slm_usage_ratio
        self._token_efficiency_ratio = token_efficiency_ratio
        self._success_rate = success_rate
    
    def get_stale_ratio(self) -> float:
        return self._stale_ratio
    
    def get_rollback_rate(self) -> float:
        return self._rollback_rate
    
    def get_red_zone_ratio(self) -> float:
        return self._red_zone_ratio
    
    def get_slm_usage_ratio(self) -> float:
        return self._slm_usage_ratio
    
    def get_token_efficiency_ratio(self) -> float:
        return self._token_efficiency_ratio
    
    def get_success_rate(self) -> float:
        return self._success_rate


class TestSuggestionEngineRules:
    """Test individual suggestion rules (Task 22.2)."""
    
    def test_rule_1_high_stale_ratio(self):
        """Test Rule 1: High stale_ratio (>20%) → Re-index skills (HIGH)."""
        engine = SuggestionEngine()
        metrics = MockMetricsProvider(stale_ratio=0.25)  # 25%
        
        suggestion = engine.evaluate_rule_1_stale_index(metrics)
        
        assert suggestion is not None
        assert suggestion.priority == SuggestionPriority.HIGH
        assert "Re-index skills" in suggestion.message
        assert suggestion.metric_value == 0.25
    
    def test_rule_1_normal_stale_ratio(self):
        """Test Rule 1 doesn't trigger with normal stale ratio."""
        engine = SuggestionEngine()
        metrics = MockMetricsProvider(stale_ratio=0.10)  # 10%
        
        suggestion = engine.evaluate_rule_1_stale_index(metrics)
        
        assert suggestion is None
    
    def test_rule_2_high_rollback_rate(self):
        """Test Rule 2: High rollback_rate (>15%) → Review error detection (HIGH)."""
        engine = SuggestionEngine()
        metrics = MockMetricsProvider(rollback_rate=0.18)  # 18%
        
        suggestion = engine.evaluate_rule_2_high_rollback(metrics)
        
        assert suggestion is not None
        assert suggestion.priority == SuggestionPriority.HIGH
        assert "Review error detection" in suggestion.message
        assert suggestion.metric_value == 0.18
    
    def test_rule_3_frequent_red_zone(self):
        """Test Rule 3: Frequent Red zone (>30%) → Increase budget (MEDIUM)."""
        engine = SuggestionEngine()
        metrics = MockMetricsProvider(red_zone_ratio=0.35)  # 35%
        
        suggestion = engine.evaluate_rule_3_red_zone(metrics)
        
        assert suggestion is not None
        assert suggestion.priority == SuggestionPriority.MEDIUM
        assert "Increase budget" in suggestion.message
        assert suggestion.metric_value == 0.35
    
    def test_rule_4_low_slm_usage(self):
        """Test Rule 4: Low SLM usage (<20%) → Check SLM router (LOW)."""
        engine = SuggestionEngine()
        metrics = MockMetricsProvider(slm_usage_ratio=0.15)  # 15%
        
        suggestion = engine.evaluate_rule_4_low_slm(metrics)
        
        assert suggestion is not None
        assert suggestion.priority == SuggestionPriority.LOW
        assert "Check SLM router" in suggestion.message
        assert suggestion.metric_value == 0.15
    
    def test_rule_5_high_token_usage(self):
        """Test Rule 5: High token per task (>baseline*1.5) → Optimize prompts (MEDIUM)."""
        engine = SuggestionEngine()
        metrics = MockMetricsProvider(token_efficiency_ratio=1.6)  # 160% of baseline
        
        suggestion = engine.evaluate_rule_5_high_tokens(metrics)
        
        assert suggestion is not None
        assert suggestion.priority == SuggestionPriority.MEDIUM
        assert "Optimize prompt" in suggestion.message
        assert suggestion.metric_value == 1.6
    
    def test_rule_6_low_success_rate(self):
        """Test Rule 6: Low success rate (<70%) → Review skill retrieval (CRITICAL)."""
        engine = SuggestionEngine()
        metrics = MockMetricsProvider(success_rate=0.65)  # 65%
        
        suggestion = engine.evaluate_rule_6_low_success(metrics)
        
        assert suggestion is not None
        assert suggestion.priority == SuggestionPriority.CRITICAL
        assert "Review skill retrieval" in suggestion.message
        assert suggestion.metric_value == 0.65


class TestSuggestionEnginePrioritization:
    """Test priority sorting and top-N selection (Task 22.3)."""
    
    def test_priority_sorting(self):
        """Test suggestions are sorted by priority (CRITICAL > HIGH > MEDIUM > LOW)."""
        engine = SuggestionEngine()
        
        # Trigger multiple rules with different priorities
        metrics = MockMetricsProvider(
            stale_ratio=0.25,        # HIGH
            rollback_rate=0.18,      # HIGH
            red_zone_ratio=0.35,     # MEDIUM
            slm_usage_ratio=0.15,    # LOW
            token_efficiency_ratio=1.6,  # MEDIUM
            success_rate=0.65        # CRITICAL
        )
        
        suggestions = engine.evaluate_all_rules(metrics)
        
        # Should have 6 suggestions (all rules triggered)
        assert len(suggestions) == 6
        
        # Sort by priority
        suggestions.sort(key=lambda s: s.priority.value)
        
        # First should be CRITICAL
        assert suggestions[0].priority == SuggestionPriority.CRITICAL
        
        # Next two should be HIGH
        assert suggestions[1].priority == SuggestionPriority.HIGH
        assert suggestions[2].priority == SuggestionPriority.HIGH
        
        # Next two should be MEDIUM
        assert suggestions[3].priority == SuggestionPriority.MEDIUM
        assert suggestions[4].priority == SuggestionPriority.MEDIUM
        
        # Last should be LOW
        assert suggestions[5].priority == SuggestionPriority.LOW
    
    def test_get_top_suggestions_default(self):
        """Test get_top_suggestions returns top 3 by default."""
        engine = SuggestionEngine()
        
        # Trigger multiple rules
        metrics = MockMetricsProvider(
            stale_ratio=0.25,        # HIGH
            rollback_rate=0.18,      # HIGH
            red_zone_ratio=0.35,     # MEDIUM
            slm_usage_ratio=0.15,    # LOW
            success_rate=0.65        # CRITICAL
        )
        
        suggestions = engine.get_top_suggestions(metrics)
        
        # Should return top 3
        assert len(suggestions) == 3
        
        # First should be CRITICAL
        assert "[CRITICAL]" in suggestions[0]
        assert "Review skill retrieval" in suggestions[0]
        
        # Next two should be HIGH
        assert "[HIGH]" in suggestions[1]
        assert "[HIGH]" in suggestions[2]
    
    def test_get_top_suggestions_custom_count(self):
        """Test get_top_suggestions with custom max_count."""
        engine = SuggestionEngine()
        
        # Trigger multiple rules
        metrics = MockMetricsProvider(
            stale_ratio=0.25,
            rollback_rate=0.18,
            success_rate=0.65
        )
        
        suggestions = engine.get_top_suggestions(metrics, max_count=2)
        
        # Should return top 2
        assert len(suggestions) == 2
        
        # First should be CRITICAL
        assert "[CRITICAL]" in suggestions[0]
        
        # Second should be HIGH
        assert "[HIGH]" in suggestions[1]
    
    def test_get_top_suggestions_no_issues(self):
        """Test get_top_suggestions returns empty list when no issues."""
        engine = SuggestionEngine()
        
        # All metrics normal
        metrics = MockMetricsProvider(
            stale_ratio=0.10,
            rollback_rate=0.05,
            red_zone_ratio=0.10,
            slm_usage_ratio=0.50,
            token_efficiency_ratio=1.0,
            success_rate=0.90
        )
        
        suggestions = engine.get_top_suggestions(metrics)
        
        # Should return empty list
        assert len(suggestions) == 0


class TestSuggestionEngineIntegration:
    """Test integration with HealthMonitor (Task 22.4)."""
    
    def test_health_monitor_uses_suggestion_engine(self):
        """Test HealthMonitor.suggest_actions() uses SuggestionEngine."""
        from antigravity.core.health_monitor import HealthMonitor
        
        monitor = HealthMonitor(window_size=10)
        
        # Record tasks with high rollback rate
        for i in range(10):
            monitor.record_task(
                success=(i < 8),  # 80% success
                patches_count=2,
                rollback=(i >= 8),  # 20% rollback
                tokens_used=2500,
                no_op_patch=False
            )
        
        # Get suggestions
        suggestions = monitor.suggest_actions()
        
        # Should have suggestions (rollback rate is 20% > 15%)
        assert len(suggestions) > 0
        
        # Should be formatted with priority tags
        assert any("[HIGH]" in s or "[CRITICAL]" in s or "[MEDIUM]" in s for s in suggestions)
    
    def test_health_monitor_suggestion_format(self):
        """Test suggestions are properly formatted."""
        from antigravity.core.health_monitor import HealthMonitor
        
        monitor = HealthMonitor(window_size=10)
        
        # Record tasks with low success rate (triggers CRITICAL)
        for i in range(10):
            monitor.record_task(
                success=(i < 6),  # 60% success (< 70% threshold)
                patches_count=1,
                rollback=False,
                tokens_used=2000,
                no_op_patch=False
            )
        
        # Get suggestions
        suggestions = monitor.suggest_actions()
        
        # Should have at least one suggestion
        assert len(suggestions) > 0
        
        # First suggestion should be CRITICAL (low success rate)
        assert "[CRITICAL]" in suggestions[0]
        assert "Review skill retrieval" in suggestions[0]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
