"""
Tier-based Dynamic Routing for Token Efficiency.

This module implements intelligent skill loading based on task tier,
reducing token usage by 50%+ through selective skill loading.
"""

from dataclasses import dataclass
from enum import IntEnum
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


class TaskTier(IntEnum):
    """Task complexity tiers."""
    TIER_1 = 1  # Simple: Blog, CRUD, landing page
    TIER_2 = 2  # Essential: E-commerce, SaaS, payment
    TIER_3 = 3  # Advanced: Real-time, microservices
    TIER_4 = 4  # Critical: Medical, space, life-critical


@dataclass
class TierConfig:
    """Configuration for each tier."""
    tier: TaskTier
    max_skills: int
    skill_categories: List[str]
    load_master_inventory: bool
    description: str


class TierRouter:
    """
    Routes tasks to appropriate skill sets based on tier.
    
    Token Efficiency Strategy:
    - Tier 1: Load 3-5 essential skills only
    - Tier 2: Load 5-8 moderate skills
    - Tier 3: Load 8-12 advanced skills
    - Tier 4: Load 12-15 comprehensive skills
    """
    
    TIER_CONFIGS = {
        TaskTier.TIER_1: TierConfig(
            tier=TaskTier.TIER_1,
            max_skills=5,
            skill_categories=["frontend-basic", "backend-basic", "workflows-essential"],
            load_master_inventory=True,
            description="Simple tasks: Blog, CRUD, landing page"
        ),
        TaskTier.TIER_2: TierConfig(
            tier=TaskTier.TIER_2,
            max_skills=8,
            skill_categories=[
                "frontend-basic", "backend-basic", "security-owasp",
                "workflows-essential", "validation", "error-handling"
            ],
            load_master_inventory=True,
            description="Essential tasks: E-commerce, SaaS, payment (OWASP, GDPR)"
        ),
        TaskTier.TIER_3: TierConfig(
            tier=TaskTier.TIER_3,
            max_skills=12,
            skill_categories=[
                "frontend-advanced", "backend-advanced", "security-advanced",
                "devops", "workflows-advanced", "real-time", "microservices"
            ],
            load_master_inventory=False,
            description="Advanced tasks: Real-time, microservices, scalability"
        ),
        TaskTier.TIER_4: TierConfig(
            tier=TaskTier.TIER_4,
            max_skills=15,
            skill_categories=[
                "frontend-all", "backend-all", "security-critical",
                "devops-all", "workflows-all", "compliance", "testing-critical"
            ],
            load_master_inventory=False,
            description="Critical tasks: Medical, space, life-critical"
        )
    }
    
    def __init__(self):
        """Initialize TierRouter."""
        self._routing_stats = {tier: {"count": 0, "avg_skills": 0.0} for tier in TaskTier}
    
    def detect_tier(self, task_description: str, tags: Optional[List[str]] = None) -> TaskTier:
        """
        Detect task tier from description and tags.
        
        Args:
            task_description: Task description text
            tags: Optional list of tags
            
        Returns:
            Detected TaskTier
        """
        description_lower = task_description.lower()
        tags_lower = [t.lower() for t in (tags or [])]
        
        # Combine description and tags for checking
        combined_text = description_lower + " " + " ".join(tags_lower)
        
        # Tier 4 indicators (highest priority)
        tier4_keywords = [
            "medical", "healthcare", "life-critical", "space", "autonomous",
            "fda", "hipaa", "iec 62304", "safety-critical", "real-time critical"
        ]
        if any(kw in combined_text for kw in tier4_keywords):
            logger.info(f"[TIER ROUTER] Detected TIER 4: {task_description[:50]}...")
            return TaskTier.TIER_4
        
        # Tier 3 indicators
        tier3_keywords = [
            "real-time", "microservices", "scalability", "high-traffic",
            "distributed", "event-driven", "websocket", "streaming"
        ]
        if any(kw in combined_text for kw in tier3_keywords):
            logger.info(f"[TIER ROUTER] Detected TIER 3: {task_description[:50]}...")
            return TaskTier.TIER_3
        
        # Tier 2 indicators
        tier2_keywords = [
            "e-commerce", "payment", "saas", "authentication", "authorization",
            "owasp", "gdpr", "pci-dss", "security", "compliance"
        ]
        if any(kw in combined_text for kw in tier2_keywords):
            logger.info(f"[TIER ROUTER] Detected TIER 2: {task_description[:50]}...")
            return TaskTier.TIER_2
        
        # Default to Tier 1
        logger.info(f"[TIER ROUTER] Detected TIER 1 (default): {task_description[:50]}...")
        return TaskTier.TIER_1
    
    def get_skill_budget(self, tier: TaskTier) -> int:
        """
        Get maximum number of skills to load for tier.
        
        Args:
            tier: Task tier
            
        Returns:
            Maximum number of skills
        """
        config = self.TIER_CONFIGS[tier]
        return config.max_skills
    
    def get_skill_categories(self, tier: TaskTier) -> List[str]:
        """
        Get skill categories to load for tier.
        
        Args:
            tier: Task tier
            
        Returns:
            List of skill category names
        """
        config = self.TIER_CONFIGS[tier]
        return config.skill_categories
    
    def should_load_master_inventory(self, tier: TaskTier) -> bool:
        """
        Check if master inventory should be loaded for tier.
        
        Master inventories are compressed skill summaries that provide
        100+ skills in a single file, reducing token usage by 90%.
        
        Args:
            tier: Task tier
            
        Returns:
            True if master inventory should be loaded
        """
        config = self.TIER_CONFIGS[tier]
        return config.load_master_inventory
    
    def route_task(
        self,
        task_description: str,
        tags: Optional[List[str]] = None,
        explicit_tier: Optional[int] = None
    ) -> dict:
        """
        Route task to appropriate skill set.
        
        Args:
            task_description: Task description
            tags: Optional tags
            explicit_tier: Optional explicit tier (1-4)
            
        Returns:
            Routing decision dict with:
                - tier: TaskTier
                - max_skills: int
                - categories: List[str]
                - use_master_inventory: bool
                - description: str
        """
        # Use explicit tier if provided
        if explicit_tier is not None:
            tier = TaskTier(explicit_tier)
            logger.info(f"[TIER ROUTER] Using explicit tier: {tier}")
        else:
            tier = self.detect_tier(task_description, tags)
        
        config = self.TIER_CONFIGS[tier]
        
        # Update stats
        self._routing_stats[tier]["count"] += 1
        
        decision = {
            "tier": tier,
            "max_skills": config.max_skills,
            "categories": config.skill_categories,
            "use_master_inventory": config.load_master_inventory,
            "description": config.description
        }
        
        logger.info(
            f"[TIER ROUTER] Routing decision: "
            f"Tier={tier.value}, MaxSkills={config.max_skills}, "
            f"MasterInventory={config.load_master_inventory}"
        )
        
        return decision
    
    def get_routing_stats(self) -> dict:
        """
        Get routing statistics.
        
        Returns:
            Dict with routing stats per tier
        """
        return {
            f"tier_{tier.value}": {
                "count": stats["count"],
                "avg_skills": stats["avg_skills"],
                "description": self.TIER_CONFIGS[tier].description
            }
            for tier, stats in self._routing_stats.items()
        }
    
    def estimate_token_savings(self, tier: TaskTier, baseline_skills: int = 25) -> float:
        """
        Estimate token savings compared to loading all skills.
        
        Args:
            tier: Task tier
            baseline_skills: Baseline number of skills (default: 25)
            
        Returns:
            Token savings ratio (0.0-1.0)
        """
        config = self.TIER_CONFIGS[tier]
        
        if config.load_master_inventory:
            # Master inventory: 1 file = 100+ skills compressed
            # Token savings: ~90%
            savings = 0.90
        else:
            # Regular skills: proportional to skill count
            savings = 1.0 - (config.max_skills / baseline_skills)
        
        logger.debug(
            f"[TIER ROUTER] Token savings for Tier {tier.value}: "
            f"{savings:.1%} ({config.max_skills}/{baseline_skills} skills)"
        )
        
        return savings
