"""
BudgetStrategy — Graceful degradation under token budget pressure.

Implements three-zone strategy (GREEN/YELLOW/RED) with automatic adaptation:
- GREEN: Full features, high quality
- YELLOW: Reduced retrieval, prefer SLM
- RED: Minimal mode, disable repair

Validates Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8
"""

from __future__ import annotations
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


# ── Budget Zones ──────────────────────────────────────────────────────────────

class BudgetZone(Enum):
    """
    Budget zones for graceful degradation.
    
    GREEN: Abundant budget (>50% remaining)
    YELLOW: Moderate budget (20-50% remaining)
    RED: Critical budget (<20% remaining)
    """
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
    
    def __str__(self) -> str:
        return self.value.upper()


# ── Strategy Configuration ────────────────────────────────────────────────────

@dataclass
class StrategyConfig:
    """
    Configuration for a specific budget zone.
    
    Attributes:
        top_k: Number of skills to retrieve
        use_expansion: Whether to use contextual summary expansion
        prompt_mode: Prompt verbosity ("full" | "short" | "minimal")
        prefer_slm: Whether to prefer SLM routing
        enable_repair: Whether repair loop is enabled
    """
    top_k: int
    use_expansion: bool
    prompt_mode: str  # "full" | "short" | "minimal"
    prefer_slm: bool
    enable_repair: bool
    
    def __str__(self) -> str:
        return (
            f"StrategyConfig(top_k={self.top_k}, "
            f"expansion={self.use_expansion}, "
            f"prompt={self.prompt_mode}, "
            f"slm={self.prefer_slm}, "
            f"repair={self.enable_repair})"
        )


@dataclass
class ZoneStats:
    """
    Statistics for a budget zone.
    
    Attributes:
        success_count: Number of successful tasks
        failure_count: Number of failed tasks
        total_tasks: Total tasks executed in this zone
    """
    success_count: int = 0
    failure_count: int = 0
    
    @property
    def total_tasks(self) -> int:
        return self.success_count + self.failure_count
    
    @property
    def success_rate(self) -> float:
        if self.total_tasks == 0:
            return 0.0
        return self.success_count / self.total_tasks


# ── Budget Strategy ───────────────────────────────────────────────────────────

class BudgetStrategy:
    """
    Manages graceful degradation strategy based on remaining token budget.
    
    Features:
    - Three-zone system (GREEN/YELLOW/RED)
    - Automatic strategy adaptation
    - Zone transition logging
    - Success rate tracking per zone
    
    Validates Requirements:
    - 4.1: Three-zone system
    - 4.2: Strategy configuration per zone
    - 4.3: Automatic zone detection
    - 4.4: Zone transition logging
    - 4.5: Success rate tracking
    - 4.6: Graceful degradation
    - 4.7: SLM routing preference
    - 4.8: Repair loop control
    """
    
    def __init__(
        self,
        yellow_threshold: float = 0.5,
        red_threshold: float = 0.2
    ):
        """
        Initialize BudgetStrategy.
        
        Args:
            yellow_threshold: Budget ratio threshold for YELLOW zone (default: 0.5 = 50%)
            red_threshold: Budget ratio threshold for RED zone (default: 0.2 = 20%)
        """
        if not 0.0 < red_threshold < yellow_threshold <= 1.0:
            raise ValueError(
                f"Invalid thresholds: red={red_threshold}, yellow={yellow_threshold}. "
                f"Must satisfy: 0 < red < yellow <= 1"
            )
        
        self.yellow_threshold = yellow_threshold
        self.red_threshold = red_threshold
        
        # Zone configurations
        self._zone_configs = {
            BudgetZone.GREEN: StrategyConfig(
                top_k=5,
                use_expansion=True,
                prompt_mode="full",
                prefer_slm=False,
                enable_repair=True
            ),
            BudgetZone.YELLOW: StrategyConfig(
                top_k=3,
                use_expansion=False,
                prompt_mode="short",
                prefer_slm=True,
                enable_repair=True
            ),
            BudgetZone.RED: StrategyConfig(
                top_k=1,
                use_expansion=False,
                prompt_mode="minimal",
                prefer_slm=True,
                enable_repair=False
            )
        }
        
        # Current state
        self._current_zone: BudgetZone = BudgetZone.GREEN
        
        # Statistics
        self._zone_stats: dict[BudgetZone, ZoneStats] = {
            BudgetZone.GREEN: ZoneStats(),
            BudgetZone.YELLOW: ZoneStats(),
            BudgetZone.RED: ZoneStats()
        }
        
        logger.info(
            f"BudgetStrategy initialized: "
            f"yellow_threshold={yellow_threshold:.1%}, "
            f"red_threshold={red_threshold:.1%}"
        )
    
    def get_current_zone(self, remaining_ratio: float) -> BudgetZone:
        """
        Determine current budget zone based on remaining ratio.
        
        Args:
            remaining_ratio: Ratio of remaining budget (0.0-1.0)
        
        Returns:
            Current BudgetZone
            
        Validates: Requirements 4.1, 4.3
        """
        if remaining_ratio > self.yellow_threshold:
            return BudgetZone.GREEN
        elif remaining_ratio > self.red_threshold:
            return BudgetZone.YELLOW
        else:
            return BudgetZone.RED
    
    def get_strategy(self, zone: BudgetZone) -> StrategyConfig:
        """
        Get strategy configuration for a zone.
        
        Args:
            zone: Budget zone
        
        Returns:
            StrategyConfig for the zone
            
        Validates: Requirements 4.2
        """
        config = self._zone_configs[zone]
        
        # Log zone transition if changed
        if zone != self._current_zone:
            self.log_zone_transition(self._current_zone, zone, None)
            self._current_zone = zone
        
        return config
    
    def log_zone_transition(
        self,
        old_zone: BudgetZone,
        new_zone: BudgetZone,
        remaining_ratio: Optional[float]
    ) -> None:
        """
        Log budget zone transition.
        
        Args:
            old_zone: Previous zone
            new_zone: New zone
            remaining_ratio: Current remaining budget ratio (optional)
            
        Validates: Requirements 4.4
        """
        config = self._zone_configs[new_zone]
        
        ratio_str = f"{remaining_ratio:.1%}" if remaining_ratio is not None else "N/A"
        
        logger.warning(
            f"[BUDGET] Zone transition: {old_zone} → {new_zone} "
            f"(remaining: {ratio_str})"
        )
        logger.info(
            f"[BUDGET] Strategy: top_k={config.top_k}, "
            f"prompt_mode={config.prompt_mode}, "
            f"prefer_slm={config.prefer_slm}, "
            f"repair={config.enable_repair}"
        )
    
    def record_task_result(self, zone: BudgetZone, success: bool) -> None:
        """
        Record task execution result for a zone.
        
        Args:
            zone: Budget zone where task was executed
            success: Whether task succeeded
            
        Validates: Requirements 4.5
        """
        stats = self._zone_stats[zone]
        
        if success:
            stats.success_count += 1
        else:
            stats.failure_count += 1
        
        logger.debug(
            f"[BUDGET] Task result recorded: zone={zone}, "
            f"success={success}, "
            f"zone_success_rate={stats.success_rate:.2%}"
        )
    
    def get_zone_statistics(self) -> dict[str, float]:
        """
        Get success rate statistics for all zones.
        
        Returns:
            Dictionary with zone statistics
            
        Validates: Requirements 4.5
        """
        return {
            "green_zone_success_rate": self._zone_stats[BudgetZone.GREEN].success_rate,
            "yellow_zone_success_rate": self._zone_stats[BudgetZone.YELLOW].success_rate,
            "red_zone_success_rate": self._zone_stats[BudgetZone.RED].success_rate,
            "green_zone_tasks": self._zone_stats[BudgetZone.GREEN].total_tasks,
            "yellow_zone_tasks": self._zone_stats[BudgetZone.YELLOW].total_tasks,
            "red_zone_tasks": self._zone_stats[BudgetZone.RED].total_tasks,
        }
    
    def get_zone_time_ratio(self) -> dict[str, float]:
        """
        Get ratio of time spent in each zone.
        
        Returns:
            Dictionary with zone time ratios
        """
        total_tasks = sum(stats.total_tasks for stats in self._zone_stats.values())
        
        if total_tasks == 0:
            return {
                "green_zone_ratio": 0.0,
                "yellow_zone_ratio": 0.0,
                "red_zone_ratio": 0.0
            }
        
        return {
            "green_zone_ratio": self._zone_stats[BudgetZone.GREEN].total_tasks / total_tasks,
            "yellow_zone_ratio": self._zone_stats[BudgetZone.YELLOW].total_tasks / total_tasks,
            "red_zone_ratio": self._zone_stats[BudgetZone.RED].total_tasks / total_tasks,
        }
