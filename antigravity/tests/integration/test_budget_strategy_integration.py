"""
Integration Tests for BudgetStrategy with Orchestrator

Tests budget-aware routing, planning, and repair across different zones.

Requirements: 4.1-4.8 from antigravity-resilience-upgrade spec.
"""

import os
from unittest.mock import Mock, patch, MagicMock

import pytest

from antigravity.core.budget_strategy import BudgetStrategy, BudgetZone
from antigravity.core.budget_guard import BudgetGuard


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def budget_guard():
    """Create BudgetGuard with known limits."""
    return BudgetGuard(
        max_steps=50,
        max_tokens=10000,
        max_repair_attempts=5
    )


@pytest.fixture
def budget_strategy():
    """Create BudgetStrategy with default thresholds."""
    return BudgetStrategy(
        yellow_threshold=0.5,
        red_threshold=0.2
    )


# ── Integration Tests ──────────────────────────────────────────────────────────

def test_zone_detection_with_budget_guard(budget_guard, budget_strategy):
    """
    Test zone detection integrates correctly with BudgetGuard.
    
    Requirements: 4.1, 4.2
    """
    # Start in GREEN zone (100% remaining)
    assert budget_guard.remaining_ratio == 1.0
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    assert zone == BudgetZone.GREEN
    
    # Consume tokens to reach YELLOW zone (45% remaining)
    budget_guard.record_call(5500)  # 5500/10000 = 55% used, 45% remaining
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    assert zone == BudgetZone.YELLOW
    
    # Consume more to reach RED zone (15% remaining)
    budget_guard.record_call(3000)  # 8500/10000 = 85% used, 15% remaining
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    assert zone == BudgetZone.RED


def test_strategy_adaptation_across_zones(budget_guard, budget_strategy):
    """
    Test strategy config changes as budget depletes.
    
    Requirements: 4.3, 4.4
    """
    # GREEN zone: full features
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    config = budget_strategy.get_strategy(zone)
    
    assert config.top_k == 5
    assert config.use_expansion is True
    assert config.prompt_mode == "full"
    assert config.prefer_slm is False
    assert config.enable_repair is True
    
    # YELLOW zone: reduced features
    budget_guard.record_call(5500)
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    config = budget_strategy.get_strategy(zone)
    
    assert config.top_k == 3
    assert config.use_expansion is False
    assert config.prompt_mode == "short"
    assert config.prefer_slm is True
    assert config.enable_repair is True
    
    # RED zone: minimal features
    budget_guard.record_call(3000)
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    config = budget_strategy.get_strategy(zone)
    
    assert config.top_k == 1
    assert config.use_expansion is False
    assert config.prompt_mode == "minimal"
    assert config.prefer_slm is True
    assert config.enable_repair is False  # Repair disabled in RED


def test_task_result_tracking(budget_strategy):
    """
    Test task result recording and statistics.
    
    Requirements: 4.7, 4.8
    """
    # Record 10 tasks in GREEN zone: 8 success, 2 failure
    for _ in range(8):
        budget_strategy.record_task_result(BudgetZone.GREEN, success=True)
    for _ in range(2):
        budget_strategy.record_task_result(BudgetZone.GREEN, success=False)
    
    # Record 10 tasks in YELLOW zone: 6 success, 4 failure
    for _ in range(6):
        budget_strategy.record_task_result(BudgetZone.YELLOW, success=True)
    for _ in range(4):
        budget_strategy.record_task_result(BudgetZone.YELLOW, success=False)
    
    # Record 10 tasks in RED zone: 4 success, 6 failure
    for _ in range(4):
        budget_strategy.record_task_result(BudgetZone.RED, success=True)
    for _ in range(6):
        budget_strategy.record_task_result(BudgetZone.RED, success=False)
    
    # Get statistics
    stats = budget_strategy.get_zone_statistics()
    
    # Verify success rates
    assert stats["green_zone_success_rate"] == 0.8  # 8/10
    assert stats["yellow_zone_success_rate"] == 0.6  # 6/10
    assert stats["red_zone_success_rate"] == pytest.approx(0.4, abs=0.01)  # 4/10
    
    # Verify task counts
    assert stats["green_zone_tasks"] == 10
    assert stats["yellow_zone_tasks"] == 10
    assert stats["red_zone_tasks"] == 10


def test_zone_time_tracking(budget_strategy):
    """
    Test zone time ratio tracking.
    
    Requirements: 4.8
    """
    # Simulate 100 tasks across zones
    for _ in range(50):
        budget_strategy.record_task_result(BudgetZone.GREEN, success=True)
    for _ in range(30):
        budget_strategy.record_task_result(BudgetZone.YELLOW, success=True)
    for _ in range(20):
        budget_strategy.record_task_result(BudgetZone.RED, success=True)
    
    # Get zone time ratios
    ratios = budget_strategy.get_zone_time_ratio()
    
    assert ratios["green_zone_ratio"] == 0.5  # 50/100
    assert ratios["yellow_zone_ratio"] == 0.3  # 30/100
    assert ratios["red_zone_ratio"] == 0.2  # 20/100


def test_full_degradation_flow_integration(budget_guard, budget_strategy):
    """
    Integration test: Full budget degradation flow.
    
    Simulates realistic task execution with budget depletion.
    
    Requirements: 4.1-4.8
    """
    task_results = []
    
    # Execute 30 tasks with increasing token consumption
    for i in range(30):
        # Get current zone
        remaining_ratio = budget_guard.remaining_ratio
        zone = budget_strategy.get_current_zone(remaining_ratio)
        config = budget_strategy.get_strategy(zone)
        
        # Simulate task execution with zone-appropriate token usage
        if zone == BudgetZone.GREEN:
            tokens_used = 400  # Full prompts
        elif zone == BudgetZone.YELLOW:
            tokens_used = 250  # Short prompts
        else:  # RED
            tokens_used = 150  # Minimal prompts
        
        # Record token usage
        try:
            budget_guard.check_pre_call(tokens_used // 2, tokens_used // 2)
            budget_guard.record_call(tokens_used)
            budget_guard.record_step()
            
            # Simulate success (90% in GREEN, 70% in YELLOW, 50% in RED)
            import random
            if zone == BudgetZone.GREEN:
                success = random.random() < 0.9
            elif zone == BudgetZone.YELLOW:
                success = random.random() < 0.7
            else:
                success = random.random() < 0.5
            
            budget_strategy.record_task_result(zone, success)
            
            task_results.append({
                "task_id": i,
                "zone": zone,
                "tokens_used": tokens_used,
                "success": success,
                "remaining_ratio": remaining_ratio
            })
        except Exception as e:
            # Budget exceeded
            task_results.append({
                "task_id": i,
                "zone": zone,
                "error": str(e),
                "remaining_ratio": remaining_ratio
            })
            break
    
    # Verify zone transitions occurred
    zones_visited = set(r["zone"] for r in task_results if "zone" in r)
    assert BudgetZone.GREEN in zones_visited
    assert BudgetZone.YELLOW in zones_visited or BudgetZone.RED in zones_visited
    
    # Verify token usage decreased in lower zones
    green_tasks = [r for r in task_results if r.get("zone") == BudgetZone.GREEN]
    yellow_tasks = [r for r in task_results if r.get("zone") == BudgetZone.YELLOW]
    
    if green_tasks and yellow_tasks:
        avg_green_tokens = sum(r["tokens_used"] for r in green_tasks) / len(green_tasks)
        avg_yellow_tokens = sum(r["tokens_used"] for r in yellow_tasks) / len(yellow_tasks)
        assert avg_yellow_tokens < avg_green_tokens
    
    # Verify statistics collected
    stats = budget_strategy.get_zone_statistics()
    assert stats["green_zone_tasks"] > 0


def test_repair_disabled_in_red_zone(budget_guard, budget_strategy):
    """
    Test repair is disabled when in RED zone.
    
    Requirements: 4.6
    """
    # Deplete budget to RED zone
    budget_guard.record_call(8500)  # 85% used, 15% remaining
    
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    assert zone == BudgetZone.RED
    
    config = budget_strategy.get_strategy(zone)
    assert config.enable_repair is False


def test_slm_preference_in_yellow_red_zones(budget_guard, budget_strategy):
    """
    Test SLM routing is preferred in YELLOW and RED zones.
    
    Requirements: 4.2, 4.3
    """
    # GREEN zone: no SLM preference
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    config = budget_strategy.get_strategy(zone)
    assert config.prefer_slm is False
    
    # YELLOW zone: prefer SLM
    budget_guard.record_call(5500)
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    config = budget_strategy.get_strategy(zone)
    assert config.prefer_slm is True
    
    # RED zone: prefer SLM
    budget_guard.record_call(3000)
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    config = budget_strategy.get_strategy(zone)
    assert config.prefer_slm is True


def test_prompt_mode_adaptation(budget_guard, budget_strategy):
    """
    Test prompt mode adapts to budget zone.
    
    Requirements: 4.4
    """
    # GREEN: full prompts
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    config = budget_strategy.get_strategy(zone)
    assert config.prompt_mode == "full"
    
    # YELLOW: short prompts
    budget_guard.record_call(5500)
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    config = budget_strategy.get_strategy(zone)
    assert config.prompt_mode == "short"
    
    # RED: minimal prompts
    budget_guard.record_call(3000)
    zone = budget_strategy.get_current_zone(budget_guard.remaining_ratio)
    config = budget_strategy.get_strategy(zone)
    assert config.prompt_mode == "minimal"
