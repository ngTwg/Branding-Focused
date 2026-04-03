#!/usr/bin/env python3
"""
Skill Caching System
LRU cache for frequently accessed skills to reduce I/O by 50%+

Features:
- LRU cache with 20 slots
- Preload essential skills on startup
- Cache hit/miss statistics
- Memory-efficient (only caches file content, not parsed data)
"""

from functools import lru_cache
from pathlib import Path
from typing import Optional
import time


# Configuration
SKILLS_ROOT = Path("C:/Users/<YOUR_USERNAME>/.gemini/antigravity/skills")
CACHE_SIZE = 20

# Essential skills to preload (most frequently accessed)
ESSENTIAL_SKILLS = [
    "workflows/debug-protocol.md",
    "workflows/anti-hallucination-v2.md",
    "workflows/naming-conventions.md",
    "workflows/error-handling-patterns.md",
    "workflows/edge-case-catalog.md",
    "security/security-middleware-stack.md",
    "frontend/state-classification.md",
    "backend/api-design-standards.md",
    "backend/database-standards.md",
    "workflows/refactoring-triggers.md",
]


@lru_cache(maxsize=CACHE_SIZE)
def get_skill_content(skill_path: str) -> str:
    """
    Get skill file content with LRU caching
    
    Args:
        skill_path: Absolute path to skill file
    
    Returns:
        File content as string
    
    Raises:
        FileNotFoundError: If skill file doesn't exist
    """
    path = Path(skill_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Skill not found: {skill_path}")
    
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
        return content
    except Exception as e:
        raise IOError(f"Error reading skill {skill_path}: {e}")


def get_skill(skill_name: str) -> str:
    """
    Get skill content by relative name
    
    Args:
        skill_name: Relative path from skills root (e.g., "workflows/debug-protocol.md")
    
    Returns:
        File content as string
    """
    full_path = SKILLS_ROOT / skill_name
    return get_skill_content(str(full_path))


def preload_essentials() -> dict:
    """
    Preload essential skills into cache
    
    Returns:
        Dict with preload results
    """
    print("🔄 Preloading essential skills...")
    
    results = {
        "loaded": 0,
        "failed": 0,
        "skills": []
    }
    
    start_time = time.time()
    
    for skill in ESSENTIAL_SKILLS:
        full_path = SKILLS_ROOT / skill
        
        if not full_path.exists():
            print(f"  ⚠️ Not found: {skill}")
            results["failed"] += 1
            continue
        
        try:
            # Load into cache
            get_skill_content(str(full_path))
            print(f"  ✅ Cached: {skill}")
            results["loaded"] += 1
            results["skills"].append(skill)
        except Exception as e:
            print(f"  ❌ Error loading {skill}: {e}")
            results["failed"] += 1
    
    elapsed = time.time() - start_time
    results["time_elapsed"] = elapsed
    
    print()
    print(f"✅ Preload complete in {elapsed:.2f}s")
    print(f"   Loaded: {results['loaded']}/{len(ESSENTIAL_SKILLS)}")
    
    return results


def cache_stats() -> dict:
    """
    Get cache statistics
    
    Returns:
        Dict with hits, misses, maxsize, currsize
    """
    info = get_skill_content.cache_info()
    
    total = info.hits + info.misses
    hit_rate = (info.hits / total * 100) if total > 0 else 0
    
    return {
        "hits": info.hits,
        "misses": info.misses,
        "maxsize": info.maxsize,
        "currsize": info.currsize,
        "hit_rate": hit_rate,
        "total_requests": total
    }


def print_stats():
    """Print cache statistics in human-readable format"""
    stats = cache_stats()
    
    print("📊 Cache Statistics:")
    print(f"   Hits: {stats['hits']}")
    print(f"   Misses: {stats['misses']}")
    print(f"   Hit Rate: {stats['hit_rate']:.1f}%")
    print(f"   Cache Size: {stats['currsize']}/{stats['maxsize']}")
    print(f"   Total Requests: {stats['total_requests']}")
    
    # I/O reduction estimate
    if stats['total_requests'] > 0:
        io_saved = stats['hits']
        io_reduction = (io_saved / stats['total_requests']) * 100
        print(f"   I/O Reduction: ~{io_reduction:.1f}% ({io_saved} disk reads avoided)")


def clear_cache():
    """Clear the cache"""
    get_skill_content.cache_clear()
    print("🧹 Cache cleared")


def warm_cache(skill_list: list) -> dict:
    """
    Warm cache with specific skills
    
    Args:
        skill_list: List of skill paths relative to SKILLS_ROOT
    
    Returns:
        Dict with results
    """
    print(f"🔥 Warming cache with {len(skill_list)} skills...")
    
    results = {
        "loaded": 0,
        "failed": 0,
        "skills": []
    }
    
    for skill in skill_list:
        full_path = SKILLS_ROOT / skill
        
        if not full_path.exists():
            results["failed"] += 1
            continue
        
        try:
            get_skill_content(str(full_path))
            results["loaded"] += 1
            results["skills"].append(skill)
        except Exception:
            results["failed"] += 1
    
    print(f"✅ Warmed {results['loaded']}/{len(skill_list)} skills")
    
    return results


def get_master_inventory(category: str) -> str:
    """
    Get master inventory for a category
    
    Args:
        category: Category name (frontend, backend, security, etc.)
    
    Returns:
        Master inventory content
    """
    inventory_map = {
        "frontend": "frontend/frontend-master-inventory.md",
        "backend": "backend/backend-master-inventory.md",
        "security": "security/security-master-inventory.md",
        "workflows": "workflows/workflows-master-inventory.md",
        "deep-tech": "deep-tech/deep-tech-master-inventory.md",
        "ai-agents": "deep-tech/ai-agents-master-inventory.md",
        "cognition": "deep-tech/autonomous-cognition-inventory.md",
        "data": "data-engineering/data-engineering-master-inventory.md",
        "specialized": "specialized/specialized-master-inventory.md",
        "enterprise": "specialized/enterprise-ops-master-inventory.md",
    }
    
    skill_path = inventory_map.get(category)
    if not skill_path:
        raise ValueError(f"Unknown category: {category}")
    
    return get_skill(skill_path)


def main():
    """CLI entry point"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "preload":
            preload_essentials()
            print_stats()
        
        elif command == "stats":
            print_stats()
        
        elif command == "clear":
            clear_cache()
        
        elif command == "get":
            if len(sys.argv) < 3:
                print("Usage: python skill_cache.py get <skill_path>")
                sys.exit(1)
            
            skill_path = sys.argv[2]
            try:
                content = get_skill(skill_path)
                print(f"✅ Loaded {skill_path} ({len(content)} chars)")
                print_stats()
            except Exception as e:
                print(f"❌ Error: {e}")
                sys.exit(1)
        
        elif command == "inventory":
            if len(sys.argv) < 3:
                print("Usage: python skill_cache.py inventory <category>")
                print("Categories: frontend, backend, security, workflows, deep-tech, etc.")
                sys.exit(1)
            
            category = sys.argv[2]
            try:
                content = get_master_inventory(category)
                print(f"✅ Loaded {category} inventory ({len(content)} chars)")
                print_stats()
            except Exception as e:
                print(f"❌ Error: {e}")
                sys.exit(1)
        
        else:
            print(f"Unknown command: {command}")
            print("Available commands: preload, stats, clear, get, inventory")
            sys.exit(1)
    
    else:
        # Default: preload and show stats
        print("🚀 Skill Cache System")
        print(f"   Cache size: {CACHE_SIZE} slots")
        print(f"   Skills root: {SKILLS_ROOT}")
        print()
        
        preload_essentials()
        print()
        print_stats()


if __name__ == "__main__":
    main()
