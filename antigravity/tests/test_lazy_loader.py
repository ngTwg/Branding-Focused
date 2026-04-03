"""
Tests for LazySkillLoader - Token Optimization v6.5.0-SLIM
"""

import pytest
import time
from pathlib import Path
from antigravity.core.lazy_loader import LazySkillLoader, SkillMetadata


@pytest.fixture
def skills_root(tmp_path):
    """Create temporary skills directory structure."""
    # Create master inventories
    workflows_dir = tmp_path / "workflows"
    workflows_dir.mkdir()
    
    (workflows_dir / "workflows-master-inventory.md").write_text(
        "# Workflows Master Inventory\n**TIER:** 1-4\nQuick reference..."
    )
    
    security_dir = tmp_path / "security"
    security_dir.mkdir()
    
    (security_dir / "security-master-inventory.md").write_text(
        "# Security Master Inventory\n**TIER:** 2-4\nSecurity skills..."
    )
    
    # Create individual skills
    (workflows_dir / "debug-protocol.md").write_text(
        "# Debug Protocol\n**TIER:** 1-4\nSystematic debugging..."
    )
    
    (security_dir / "attack-vectors.md").write_text(
        "# Attack Vectors\n**TIER:** 2-4\nOWASP Top 10..."
    )
    
    return tmp_path


def test_lazy_loader_init(skills_root):
    """Test lazy loader initialization."""
    loader = LazySkillLoader(skills_root)
    
    assert len(loader.master_inventories) == 2
    assert "workflows" in loader.master_inventories
    assert "security" in loader.master_inventories
    assert loader.metrics["inventory_loads"] == 2


def test_get_master_inventory(skills_root):
    """Test getting master inventory."""
    loader = LazySkillLoader(skills_root)
    
    workflows_inv = loader.get_master_inventory("workflows")
    assert workflows_inv is not None
    assert "Workflows Master Inventory" in workflows_inv
    
    security_inv = loader.get_master_inventory("security")
    assert security_inv is not None
    assert "Security Master Inventory" in security_inv
    
    # Non-existent category
    assert loader.get_master_inventory("nonexistent") is None


def test_list_categories(skills_root):
    """Test listing categories."""
    loader = LazySkillLoader(skills_root)
    
    categories = loader.list_categories()
    assert len(categories) == 2
    assert "workflows" in categories
    assert "security" in categories


def test_load_skill_lazy(skills_root):
    """Test lazy loading of skills."""
    loader = LazySkillLoader(skills_root)
    
    # Load skill for first time (cache miss)
    content = loader.load_skill("workflows/debug-protocol.md")
    assert content is not None
    assert "Debug Protocol" in content
    assert loader.metrics["cache_misses"] == 1
    assert loader.metrics["skill_loads"] == 1
    assert len(loader.cache) == 1
    
    # Load same skill again (cache hit)
    content2 = loader.load_skill("workflows/debug-protocol.md")
    assert content2 == content
    assert loader.metrics["cache_hits"] == 1
    assert loader.metrics["skill_loads"] == 1  # No new load


def test_load_nonexistent_skill(skills_root):
    """Test loading non-existent skill."""
    loader = LazySkillLoader(skills_root)
    
    content = loader.load_skill("workflows/nonexistent.md")
    assert content is None
    assert loader.metrics["cache_misses"] == 1
    assert loader.metrics["skill_loads"] == 0


def test_cache_lru_eviction(skills_root):
    """Test LRU cache eviction."""
    loader = LazySkillLoader(skills_root, cache_size=1)
    
    # Load first skill
    loader.load_skill("workflows/debug-protocol.md")
    assert len(loader.cache) == 1
    
    # Load second skill (should evict first)
    loader.load_skill("security/attack-vectors.md")
    assert len(loader.cache) == 1
    assert "security/attack-vectors.md" in loader.cache
    assert "workflows/debug-protocol.md" not in loader.cache
    assert loader.metrics["unloads"] == 1


def test_unload_unused(skills_root):
    """Test unloading unused skills."""
    loader = LazySkillLoader(skills_root, unload_after_seconds=1)
    
    # Load skills
    loader.load_skill("workflows/debug-protocol.md")
    loader.load_skill("security/attack-vectors.md")
    assert len(loader.cache) == 2
    
    # Wait for unload timeout
    time.sleep(1.1)
    
    # Unload unused
    unloaded = loader.unload_unused()
    assert unloaded == 2
    assert len(loader.cache) == 0


def test_cache_stats(skills_root):
    """Test cache statistics."""
    loader = LazySkillLoader(skills_root)
    
    # Initial stats
    stats = loader.get_cache_stats()
    assert stats["cached_skills"] == 0
    assert stats["master_inventories"] == 2
    assert stats["hit_rate"] == 0.0
    
    # Load some skills
    loader.load_skill("workflows/debug-protocol.md")
    loader.load_skill("workflows/debug-protocol.md")  # Cache hit
    
    stats = loader.get_cache_stats()
    assert stats["cached_skills"] == 1
    assert stats["cache_hits"] == 1
    assert stats["cache_misses"] == 1
    assert stats["hit_rate"] == 0.5


def test_clear_cache(skills_root):
    """Test clearing cache."""
    loader = LazySkillLoader(skills_root)
    
    # Load skills
    loader.load_skill("workflows/debug-protocol.md")
    loader.load_skill("security/attack-vectors.md")
    assert len(loader.cache) == 2
    
    # Clear cache
    loader.clear_cache()
    assert len(loader.cache) == 0
    
    # Master inventories should still be available
    assert len(loader.master_inventories) == 2


def test_preload_skills(skills_root):
    """Test preloading multiple skills."""
    loader = LazySkillLoader(skills_root)
    
    skills_to_preload = [
        "workflows/debug-protocol.md",
        "security/attack-vectors.md",
        "workflows/nonexistent.md",  # Should fail
    ]
    
    successful, failed = loader.preload_skills(skills_to_preload)
    assert successful == 2
    assert failed == 1
    assert len(loader.cache) == 2


def test_force_reload(skills_root):
    """Test force reloading a skill."""
    loader = LazySkillLoader(skills_root)
    
    # Load skill
    content1 = loader.load_skill("workflows/debug-protocol.md")
    assert loader.metrics["skill_loads"] == 1
    
    # Force reload
    content2 = loader.load_skill("workflows/debug-protocol.md", force_reload=True)
    assert content2 == content1
    assert loader.metrics["skill_loads"] == 2  # Reloaded


def test_tier_extraction(skills_root):
    """Test tier extraction from skill content."""
    loader = LazySkillLoader(skills_root)
    
    # Load skill and check tier
    loader.load_skill("workflows/debug-protocol.md")
    metadata = loader.cache["workflows/debug-protocol.md"]
    assert metadata.tier >= 1
    assert metadata.tier <= 4


def test_access_tracking(skills_root):
    """Test access count and last accessed tracking."""
    loader = LazySkillLoader(skills_root)
    
    # Load skill multiple times
    loader.load_skill("workflows/debug-protocol.md")  # First load (cache miss)
    time.sleep(0.1)
    loader.load_skill("workflows/debug-protocol.md")  # Cache hit
    time.sleep(0.1)
    loader.load_skill("workflows/debug-protocol.md")  # Cache hit
    
    metadata = loader.cache["workflows/debug-protocol.md"]
    # First load doesn't increment access_count, only cache hits do
    assert metadata.access_count == 2
    assert metadata.last_accessed > time.time() - 1


def test_token_optimization_metrics(skills_root):
    """Test token optimization metrics."""
    # Create larger test files for realistic comparison
    workflows_dir = skills_root / "workflows"
    
    # Create larger master inventory
    (workflows_dir / "workflows-master-inventory.md").write_text(
        "# Workflows Master Inventory\n**TIER:** 1-4\n" + 
        "Quick reference index with 50+ skills compressed...\n" * 10
    )
    
    # Create larger skill file
    (workflows_dir / "debug-protocol.md").write_text(
        "# Debug Protocol\n**TIER:** 1-4\n" +
        "Systematic debugging process with detailed steps...\n" * 20
    )
    
    loader = LazySkillLoader(skills_root)
    
    # Load master inventory (lightweight)
    inv = loader.get_master_inventory("workflows")
    inv_tokens = len(inv.split())  # Rough token count
    
    # Load full skill (heavier)
    skill = loader.load_skill("workflows/debug-protocol.md")
    skill_tokens = len(skill.split())
    
    # Master inventory should be much smaller
    assert inv_tokens < skill_tokens
    
    # Token savings by loading inventory first
    savings_percent = (1 - inv_tokens / skill_tokens) * 100
    assert savings_percent > 30  # At least 30% savings (realistic threshold)
