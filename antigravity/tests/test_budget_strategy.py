"""
Unit and Property Tests for BudgetStrategy

Tests graceful degradation under budget pressure: zone detection,
strategy adaptation, transition logging, and success rate tracking.

Requirements: 4.1-4.8 from antigravity-resilience-upgrade spec.
"""

import pytest
from hypothesis import given, strategies as st, settings, assume

from antigravity.core.budget_strategy import (
    BudgetStrategy,
    BudgetZone,
    StrategyConfig,
    ZoneStats
)


# ── Unit Tests: Zone Detection ────────────────────────────────────────────────

def test_zone_detection_green():
    """
    Test zone detection for GREEN zone (>50% remaining).
    
    Requirements: 4.1, 4.3
    """
    strategy = BudgetStrategy(yellow_threshold=0.5, red_threshold=0.2)
    
    # Test various ratios in GREEN zone
    assert strategy.get_current_zone(1.0) == BudgetZone.GREEN
    assert strategy.get_current_zone(0.8) == BudgetZone.GREEN
    assert strategy.get_current_zone(0.51) == BudgetZone.GREEN


def test_zone_detection_yellow():
    """
    Test zone detection for YELLOW zone (20-50% remaining).
    
    Requirements: 4.1, 4.3
    """
    strategy = BudgetStrategy(yellow_threshold=0.5, red_threshold=0.2)
    
    # Test various ratios in YELLOW zone
    assert strategy.get_current_zone(0.5) == BudgetZone.YELLOW
    assert strategy.get_current_zone(0.4) == BudgetZone.YELLOW
    assert strategy.get_current_zone(0.21) == BudgetZone.YELLOW


def test_zone_detection_red():
    """
    Test zone detection for RED zone (<20% remaining).
    
    Requirements: 4.1, 4.3
    """
    strategy = BudgetStrategy(yellow_threshold=0.5, red_threshold=0.2)
    
    # Test various ratios in RED zone
    assert strategy.get_current_zone(0.2) == BudgetZone.RED
    assert strategy.get_current_zone(0.1) == BudgetZone.RED
    assert strategy.get_current_zone(0.01) == BudgetZone.RED
    assert strategy.get_current_zone(0.0) == BudgetZone.RED


def test_custom_thresholds():
    """Test zone detection with custom thresholds."""
    strategy = BudgetStrategy(yellow_threshold=0.7, red_threshold=0.3)
    
    assert strategy.get_current_zone(0.8) == BudgetZone.GREEN
    assert strategy.get_current_zone(0.5) == BudgetZone.YELLOW
    assert strategy.get_current_zone(0.2) == BudgetZone.RED


def test_invalid_thresholds():
    """Test that invalid thresholds raise ValueError."""
    # red >= yellow
    with pytest.raises(ValueError, match="Invalid thresholds"):
        BudgetStrategy(yellow_threshold=0.3, red_threshold=0.5)
    
    # yellow > 1.0
    with pytest.raises(ValueError, match="Invalid thresholds"):
        BudgetStrategy(yellow_threshold=1.5, red_threshold=0.2)
    
    # red <= 0
    with pytest.raises(ValueError, match="Invalid thresholds"):
        BudgetStrategy(yellow_threshold=0.5, red_threshold=0.0)


# ── Unit Tests: Strategy Configs ──────────────────────────────────────────────

def test_green_zone_config():
    """
    Test GREEN zone strategy configuration.
    
    Requirements: 4.2
    """
    strategy = BudgetStrategy()
    config = strategy.get_strategy(BudgetZone.GREEN)
    
    assert config.top_k == 5
    assert config.use_expansion is True
    assert config.prompt_mode == "full"
    assert config.prefer_slm is False
    assert config.enable_repair is True


def test_yellow_zone_config():
    """
    Test YELLOW zone strategy configuration.
    
    Requirements: 4.2, 4.7
    """
    strategy = BudgetStrategy()
    config = strategy.get_strategy(BudgetZone.YELLOW)
    
    assert config.top_k == 3
    assert config.use_expansion is False
    assert config.prompt_mode == "short"
    assert config.prefer_slm is True  # SLM preferred
    assert config.enable_repair is True


def test_red_zone_config():
    """
    Test RED zone strategy configuration.
    
    Requirements: 4.2, 4.7, 4.8
    """
    strategy = BudgetStrategy()
    config = strategy.get_strategy(BudgetZone.RED)
    
    assert config.top_k == 1
    assert config.use_expansion is False
    assert config.prompt_mode == "minimal"
    assert config.prefer_slm is True  # SLM preferred
    assert config.enable_repair is False  # Repair disabled


# ── Unit Tests: Zone Transitions ──────────────────────────────────────────────

def test_zone_transition_logging(caplog):
    """
    Test zone transition logging.
    
    Requirements: 4.4
    """
    strategy = BudgetStrategy()
    
    # Initial zone is GREEN
    assert strategy._current_zone == BudgetZone.GREEN
    
    # Transition to YELLOW
    with caplog.at_level("WARNING"):
        config = strategy.get_strategy(BudgetZone.YELLOW)
    
    assert strategy._current_zone == BudgetZone.YELLOW
    assert "Zone transition: GREEN → YELLOW" in caplog.text
    
    # Transition to RED
    caplog.clear()
    with caplog.at_level("WARNING"):
        config = strategy.get_strategy(BudgetZone.RED)
    
    assert strategy._current_zone == BudgetZone.RED
    assert "Zone transition: YELLOW → RED" in caplog.text


def test_no_transition_same_zone(caplog):
    """Test that staying in same zone doesn't log transition."""
    strategy = BudgetStrategy()
    
    # Get GREEN config twice
    with caplog.at_level("WARNING"):
        strategy.get_strategy(BudgetZone.GREEN)
        caplog.clear()
        strategy.get_strategy(BudgetZone.GREEN)
    
    # Should not log transition
    assert "Zone transition" not in caplog.text


# ── Unit Tests: Success Rate Tracking ─────────────────────────────────────────

def test_record_task_result():
    """
    Test recording task results.
    
    Requirements: 4.5
    """
    strategy = BudgetStrategy()
    
    # Record successes in GREEN zone
    strategy.record_task_result(BudgetZone.GREEN, success=True)
    strategy.record_task_result(BudgetZone.GREEN, success=True)
    strategy.record_task_result(BudgetZone.GREEN, success=False)
    
    stats = strategy._zone_stats[BudgetZone.GREEN]
    assert stats.success_count == 2
    assert stats.failure_count == 1
    assert stats.total_tasks == 3
    assert stats.success_rate == pytest.approx(0.666, abs=0.01)


def test_zone_statistics():
    """
    Test get_zone_statistics() returns correct data.
    
    Requirements: 4.5
    """
    strategy = BudgetStrategy()
    
    # Record results in different zones
    strategy.record_task_result(BudgetZone.GREEN, success=True)
    strategy.record_task_result(BudgetZone.GREEN, success=True)
    
    strategy.record_task_result(BudgetZone.YELLOW, success=True)
    strategy.record_task_result(BudgetZone.YELLOW, success=False)
    
    strategy.record_task_result(BudgetZone.RED, success=False)
    
    stats = strategy.get_zone_statistics()
    
    assert stats["green_zone_success_rate"] == 1.0
    assert stats["yellow_zone_success_rate"] == 0.5
    assert stats["red_zone_success_rate"] == 0.0
    assert stats["green_zone_tasks"] == 2
    assert stats["yellow_zone_tasks"] == 2
    assert stats["red_zone_tasks"] == 1


def test_zone_time_ratio():
    """Test get_zone_time_ratio() computes correct ratios."""
    strategy = BudgetStrategy()
    
    # Execute 10 tasks: 5 GREEN, 3 YELLOW, 2 RED
    for _ in range(5):
        strategy.record_task_result(BudgetZone.GREEN, success=True)
    for _ in range(3):
        strategy.record_task_result(BudgetZone.YELLOW, success=True)
    for _ in range(2):
        strategy.record_task_result(BudgetZone.RED, success=True)
    
    ratios = strategy.get_zone_time_ratio()
    
    assert ratios["green_zone_ratio"] == 0.5  # 5/10
    assert ratios["yellow_zone_ratio"] == 0.3  # 3/10
    assert ratios["red_zone_ratio"] == 0.2  # 2/10


def test_zone_time_ratio_no_tasks():
    """Test zone time ratio with no tasks."""
    strategy = BudgetStrategy()
    
    ratios = strategy.get_zone_time_ratio()
    
    assert ratios["green_zone_ratio"] == 0.0
    assert ratios["yellow_zone_ratio"] == 0.0
    assert ratios["red_zone_ratio"] == 0.0


# ── Integration Test: Full Degradation Flow ───────────────────────────────────

def test_full_degradation_flow():
    """
    Integration test: simulate budget depletion from GREEN → YELLOW → RED.
    
    Validates: Requirements 4.1-4.8
    """
    strategy = BudgetStrategy(yellow_threshold=0.5, red_threshold=0.2)
    
    # Phase 1: GREEN zone (100% → 60%)
    zone = strategy.get_current_zone(0.8)
    assert zone == BudgetZone.GREEN
    
    config = strategy.get_strategy(zone)
    assert config.top_k == 5
    assert config.enable_repair is True
    
    # Execute tasks in GREEN
    for _ in range(5):
        strategy.record_task_result(zone, success=True)
    
    # Phase 2: YELLOW zone (50% → 30%)
    zone = strategy.get_current_zone(0.4)
    assert zone == BudgetZone.YELLOW
    
    config = strategy.get_strategy(zone)
    assert config.top_k == 3  # Reduced
    assert config.prefer_slm is True  # SLM preferred
    assert config.enable_repair is True  # Still enabled
    
    # Execute tasks in YELLOW
    for _ in range(3):
        strategy.record_task_result(zone, success=True)
    
    # Phase 3: RED zone (15%)
    zone = strategy.get_current_zone(0.15)
    assert zone == BudgetZone.RED
    
    config = strategy.get_strategy(zone)
    assert config.top_k == 1  # Minimal
    assert config.prompt_mode == "minimal"
    assert config.enable_repair is False  # Disabled!
    
    # Execute tasks in RED
    for _ in range(2):
        strategy.record_task_result(zone, success=True)
    
    # Verify statistics
    stats = strategy.get_zone_statistics()
    assert stats["green_zone_tasks"] == 5
    assert stats["yellow_zone_tasks"] == 3
    assert stats["red_zone_tasks"] == 2
    
    ratios = strategy.get_zone_time_ratio()
    assert ratios["green_zone_ratio"] == 0.5  # 5/10
    assert ratios["yellow_zone_ratio"] == 0.3  # 3/10
    assert ratios["red_zone_ratio"] == 0.2  # 2/10


# ── Property Tests: Zone Monotonicity ─────────────────────────────────────────

@given(remaining_ratio=st.floats(min_value=0.0, max_value=1.0))
@settings(max_examples=100)
def test_zone_monotonicity(remaining_ratio):
    """
    Property test: zones never "upgrade" as budget depletes.
    
    GREEN → YELLOW → RED order maintained.
    
    Requirements: 4.1, 4.3
    """
    strategy = BudgetStrategy(yellow_threshold=0.5, red_threshold=0.2)
    
    zone = strategy.get_current_zone(remaining_ratio)
    
    # Verify zone assignment
    if remaining_ratio > 0.5:
        assert zone == BudgetZone.GREEN
    elif remaining_ratio > 0.2:
        assert zone == BudgetZone.YELLOW
    else:
        assert zone == BudgetZone.RED


@given(
    ratio1=st.floats(min_value=0.0, max_value=1.0),
    ratio2=st.floats(min_value=0.0, max_value=1.0)
)
@settings(max_examples=100)
def test_zone_ordering(ratio1, ratio2):
    """
    Property test: higher budget ratio → same or better zone.
    
    Requirements: 4.1, 4.3
    """
    assume(ratio1 != ratio2)  # Skip if equal
    
    strategy = BudgetStrategy(yellow_threshold=0.5, red_threshold=0.2)
    
    zone1 = strategy.get_current_zone(ratio1)
    zone2 = strategy.get_current_zone(ratio2)
    
    # Define zone ordering: GREEN > YELLOW > RED
    zone_order = {BudgetZone.GREEN: 3, BudgetZone.YELLOW: 2, BudgetZone.RED: 1}
    
    if ratio1 > ratio2:
        # Higher ratio should have same or better zone
        assert zone_order[zone1] >= zone_order[zone2]


@given(success_rate=st.floats(min_value=0.0, max_value=1.0))
@settings(max_examples=50)
def test_success_rate_bounds(success_rate):
    """
    Property test: success rate always in [0, 1].
    
    Requirements: 4.5
    """
    strategy = BudgetStrategy()
    
    # Simulate tasks with given success rate
    num_tasks = 100
    num_successes = int(num_tasks * success_rate)
    
    for _ in range(num_successes):
        strategy.record_task_result(BudgetZone.GREEN, success=True)
    for _ in range(num_tasks - num_successes):
        strategy.record_task_result(BudgetZone.GREEN, success=False)
    
    stats = strategy.get_zone_statistics()
    computed_rate = stats["green_zone_success_rate"]
    
    # Success rate should be in [0, 1]
    assert 0.0 <= computed_rate <= 1.0
    
    # Should match input (within floating point tolerance)
    assert computed_rate == pytest.approx(success_rate, abs=0.01)
