"""
Tests for TierRouter (Token Efficiency Optimization).
"""

import pytest
from antigravity.core.tier_router import TierRouter, TaskTier


class TestTierDetection:
    """Test tier detection from task descriptions."""
    
    def test_detect_tier_1_simple_crud(self):
        """Test Tier 1 detection for simple CRUD app."""
        router = TierRouter()
        tier = router.detect_tier("Create a simple blog with posts and comments")
        assert tier == TaskTier.TIER_1
    
    def test_detect_tier_1_landing_page(self):
        """Test Tier 1 detection for landing page."""
        router = TierRouter()
        tier = router.detect_tier("Build a landing page for my product")
        assert tier == TaskTier.TIER_1
    
    def test_detect_tier_2_ecommerce(self):
        """Test Tier 2 detection for e-commerce."""
        router = TierRouter()
        tier = router.detect_tier("Build an e-commerce site with payment processing")
        assert tier == TaskTier.TIER_2
    
    def test_detect_tier_2_saas(self):
        """Test Tier 2 detection for SaaS."""
        router = TierRouter()
        tier = router.detect_tier("Create a SaaS application with authentication")
        assert tier == TaskTier.TIER_2
    
    def test_detect_tier_2_security(self):
        """Test Tier 2 detection for security requirements."""
        router = TierRouter()
        tier = router.detect_tier("Implement OWASP security best practices")
        assert tier == TaskTier.TIER_2
    
    def test_detect_tier_3_realtime(self):
        """Test Tier 3 detection for real-time features."""
        router = TierRouter()
        tier = router.detect_tier("Build a real-time chat application with WebSocket")
        assert tier == TaskTier.TIER_3
    
    def test_detect_tier_3_microservices(self):
        """Test Tier 3 detection for microservices."""
        router = TierRouter()
        tier = router.detect_tier("Design a microservices architecture with event-driven communication")
        assert tier == TaskTier.TIER_3
    
    def test_detect_tier_4_medical(self):
        """Test Tier 4 detection for medical devices."""
        router = TierRouter()
        tier = router.detect_tier("Create firmware for medical device with FDA approval")
        assert tier == TaskTier.TIER_4
    
    def test_detect_tier_4_life_critical(self):
        """Test Tier 4 detection for life-critical systems."""
        router = TierRouter()
        tier = router.detect_tier("Implement safety-critical control system for autonomous vehicle")
        assert tier == TaskTier.TIER_4
    
    def test_detect_tier_with_tags(self):
        """Test tier detection with tags."""
        router = TierRouter()
        tier = router.detect_tier(
            "Build an application",
            tags=["medical", "healthcare", "HIPAA"]
        )
        assert tier == TaskTier.TIER_4


class TestSkillBudget:
    """Test skill budget allocation per tier."""
    
    def test_tier_1_budget(self):
        """Test Tier 1 skill budget (3-5 skills)."""
        router = TierRouter()
        budget = router.get_skill_budget(TaskTier.TIER_1)
        assert budget == 5
        assert 3 <= budget <= 5
    
    def test_tier_2_budget(self):
        """Test Tier 2 skill budget (5-8 skills)."""
        router = TierRouter()
        budget = router.get_skill_budget(TaskTier.TIER_2)
        assert budget == 8
        assert 5 <= budget <= 8
    
    def test_tier_3_budget(self):
        """Test Tier 3 skill budget (8-12 skills)."""
        router = TierRouter()
        budget = router.get_skill_budget(TaskTier.TIER_3)
        assert budget == 12
        assert 8 <= budget <= 12
    
    def test_tier_4_budget(self):
        """Test Tier 4 skill budget (12-15 skills)."""
        router = TierRouter()
        budget = router.get_skill_budget(TaskTier.TIER_4)
        assert budget == 15
        assert 12 <= budget <= 15
    
    def test_budget_monotonic_increase(self):
        """Test that budget increases with tier."""
        router = TierRouter()
        budgets = [router.get_skill_budget(tier) for tier in TaskTier]
        assert budgets == sorted(budgets), "Budget should increase with tier"


class TestSkillCategories:
    """Test skill category selection per tier."""
    
    def test_tier_1_categories(self):
        """Test Tier 1 categories (essential only)."""
        router = TierRouter()
        categories = router.get_skill_categories(TaskTier.TIER_1)
        assert "frontend-basic" in categories
        assert "backend-basic" in categories
        assert "workflows-essential" in categories
        assert len(categories) <= 5
    
    def test_tier_2_categories(self):
        """Test Tier 2 categories (+ security)."""
        router = TierRouter()
        categories = router.get_skill_categories(TaskTier.TIER_2)
        assert "security-owasp" in categories
        assert "validation" in categories
        assert "error-handling" in categories
    
    def test_tier_3_categories(self):
        """Test Tier 3 categories (+ advanced)."""
        router = TierRouter()
        categories = router.get_skill_categories(TaskTier.TIER_3)
        assert "frontend-advanced" in categories
        assert "backend-advanced" in categories
        assert "real-time" in categories or "microservices" in categories
    
    def test_tier_4_categories(self):
        """Test Tier 4 categories (comprehensive)."""
        router = TierRouter()
        categories = router.get_skill_categories(TaskTier.TIER_4)
        assert "security-critical" in categories
        assert "compliance" in categories
        assert "testing-critical" in categories


class TestMasterInventory:
    """Test master inventory loading strategy."""
    
    def test_tier_1_uses_master_inventory(self):
        """Test Tier 1 uses master inventory (90% token savings)."""
        router = TierRouter()
        assert router.should_load_master_inventory(TaskTier.TIER_1) is True
    
    def test_tier_2_uses_master_inventory(self):
        """Test Tier 2 uses master inventory."""
        router = TierRouter()
        assert router.should_load_master_inventory(TaskTier.TIER_2) is True
    
    def test_tier_3_no_master_inventory(self):
        """Test Tier 3 loads full skills (more specific)."""
        router = TierRouter()
        assert router.should_load_master_inventory(TaskTier.TIER_3) is False
    
    def test_tier_4_no_master_inventory(self):
        """Test Tier 4 loads full skills (critical)."""
        router = TierRouter()
        assert router.should_load_master_inventory(TaskTier.TIER_4) is False


class TestRouteTask:
    """Test complete task routing."""
    
    def test_route_simple_task(self):
        """Test routing simple task."""
        router = TierRouter()
        decision = router.route_task("Create a blog")
        
        assert decision["tier"] == TaskTier.TIER_1
        assert decision["max_skills"] == 5
        assert decision["use_master_inventory"] is True
        assert "frontend-basic" in decision["categories"]
    
    def test_route_ecommerce_task(self):
        """Test routing e-commerce task."""
        router = TierRouter()
        decision = router.route_task("Build e-commerce with payment")
        
        assert decision["tier"] == TaskTier.TIER_2
        assert decision["max_skills"] == 8
        assert decision["use_master_inventory"] is True
        assert "security-owasp" in decision["categories"]
    
    def test_route_realtime_task(self):
        """Test routing real-time task."""
        router = TierRouter()
        decision = router.route_task("Build real-time chat with WebSocket")
        
        assert decision["tier"] == TaskTier.TIER_3
        assert decision["max_skills"] == 12
        assert decision["use_master_inventory"] is False
    
    def test_route_medical_task(self):
        """Test routing medical task."""
        router = TierRouter()
        decision = router.route_task("Create medical device firmware with FDA approval")
        
        assert decision["tier"] == TaskTier.TIER_4
        assert decision["max_skills"] == 15
        assert decision["use_master_inventory"] is False
        assert "security-critical" in decision["categories"]
    
    def test_route_with_explicit_tier(self):
        """Test routing with explicit tier override."""
        router = TierRouter()
        decision = router.route_task(
            "Simple blog",
            explicit_tier=4  # Override to Tier 4
        )
        
        assert decision["tier"] == TaskTier.TIER_4
        assert decision["max_skills"] == 15


class TestTokenSavings:
    """Test token savings estimation."""
    
    def test_tier_1_token_savings(self):
        """Test Tier 1 token savings (90% via master inventory)."""
        router = TierRouter()
        savings = router.estimate_token_savings(TaskTier.TIER_1, baseline_skills=25)
        assert savings == 0.90  # Master inventory
    
    def test_tier_2_token_savings(self):
        """Test Tier 2 token savings (90% via master inventory)."""
        router = TierRouter()
        savings = router.estimate_token_savings(TaskTier.TIER_2, baseline_skills=25)
        assert savings == 0.90  # Master inventory
    
    def test_tier_3_token_savings(self):
        """Test Tier 3 token savings (proportional)."""
        router = TierRouter()
        savings = router.estimate_token_savings(TaskTier.TIER_3, baseline_skills=25)
        expected = 1.0 - (12 / 25)  # 12 skills vs 25 baseline
        assert savings == pytest.approx(expected, abs=0.01)
    
    def test_tier_4_token_savings(self):
        """Test Tier 4 token savings (minimal)."""
        router = TierRouter()
        savings = router.estimate_token_savings(TaskTier.TIER_4, baseline_skills=25)
        expected = 1.0 - (15 / 25)  # 15 skills vs 25 baseline
        assert savings == pytest.approx(expected, abs=0.01)
    
    def test_overall_token_savings(self):
        """Test overall token savings across tiers."""
        router = TierRouter()
        
        # Simulate 100 tasks: 40% Tier 1, 30% Tier 2, 20% Tier 3, 10% Tier 4
        tier_distribution = {
            TaskTier.TIER_1: 40,
            TaskTier.TIER_2: 30,
            TaskTier.TIER_3: 20,
            TaskTier.TIER_4: 10
        }
        
        total_savings = 0.0
        for tier, count in tier_distribution.items():
            savings = router.estimate_token_savings(tier)
            total_savings += savings * count
        
        avg_savings = total_savings / 100
        assert avg_savings > 0.50, "Should achieve >50% token savings overall"


class TestRoutingStats:
    """Test routing statistics tracking."""
    
    def test_routing_stats_initialization(self):
        """Test routing stats initialized correctly."""
        router = TierRouter()
        stats = router.get_routing_stats()
        
        assert "tier_1" in stats
        assert "tier_2" in stats
        assert "tier_3" in stats
        assert "tier_4" in stats
        
        for tier_stats in stats.values():
            assert tier_stats["count"] == 0
            assert "description" in tier_stats
    
    def test_routing_stats_tracking(self):
        """Test routing stats track task counts."""
        router = TierRouter()
        
        # Route 10 tasks
        router.route_task("Create blog")  # Tier 1
        router.route_task("Create blog")  # Tier 1
        router.route_task("Build e-commerce")  # Tier 2
        router.route_task("Build real-time chat")  # Tier 3
        
        stats = router.get_routing_stats()
        assert stats["tier_1"]["count"] == 2
        assert stats["tier_2"]["count"] == 1
        assert stats["tier_3"]["count"] == 1
        assert stats["tier_4"]["count"] == 0


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_empty_task_description(self):
        """Test routing with empty description (default to Tier 1)."""
        router = TierRouter()
        tier = router.detect_tier("")
        assert tier == TaskTier.TIER_1
    
    def test_ambiguous_task_description(self):
        """Test routing with ambiguous description."""
        router = TierRouter()
        tier = router.detect_tier("Build an application")
        assert tier == TaskTier.TIER_1  # Default
    
    def test_multiple_tier_keywords(self):
        """Test routing with multiple tier keywords (highest wins)."""
        router = TierRouter()
        tier = router.detect_tier("Build e-commerce medical device")
        assert tier == TaskTier.TIER_4  # Medical (Tier 4) > e-commerce (Tier 2)
    
    def test_explicit_tier_override(self):
        """Test explicit tier overrides detection."""
        router = TierRouter()
        decision = router.route_task(
            "Simple blog",  # Would be Tier 1
            explicit_tier=3  # Override to Tier 3
        )
        assert decision["tier"] == TaskTier.TIER_3
