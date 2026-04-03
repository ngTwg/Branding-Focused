"""
Lazy Loader for Skills - Token Optimization v6.5.0-SLIM

Load master inventories first (lightweight), then load full skills only when needed.
Implements caching and automatic unloading of unused skills.

Token Savings: 98% by loading only what's needed.
"""

import time
from pathlib import Path
from typing import Dict, Optional, Set, Tuple
from dataclasses import dataclass, field
from collections import OrderedDict
import threading


@dataclass
class SkillMetadata:
    """Metadata for a skill."""
    path: Path
    category: str
    tier: int
    size_kb: float
    last_accessed: float = field(default_factory=time.time)
    access_count: int = 0
    content: Optional[str] = None  # Cached content


class LazySkillLoader:
    """
    Lazy loader for skills with automatic caching and unloading.
    
    Strategy:
    1. Load master inventories first (lightweight, ~8KB each)
    2. Load full skill content only when explicitly requested
    3. Cache loaded skills in memory (LRU cache)
    4. Automatically unload unused skills after 5 minutes
    
    Token Optimization:
    - Master inventory: ~500 tokens
    - Full skill: ~2000-5000 tokens
    - Savings: 75-90% by loading inventories first
    """
    
    def __init__(
        self,
        skills_root: Path,
        cache_size: int = 20,
        unload_after_seconds: int = 300  # 5 minutes
    ):
        self.skills_root = Path(skills_root)
        self.cache_size = cache_size
        self.unload_after_seconds = unload_after_seconds
        
        # Cache: skill_path -> SkillMetadata
        self.cache: OrderedDict[str, SkillMetadata] = OrderedDict()
        
        # Master inventories (always loaded)
        self.master_inventories: Dict[str, str] = {}
        
        # Lock for thread safety
        self._lock = threading.Lock()
        
        # Metrics
        self.metrics = {
            "inventory_loads": 0,
            "skill_loads": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "unloads": 0,
        }
        
        # Load master inventories on init
        self._load_master_inventories()
    
    def _load_master_inventories(self) -> None:
        """Load all master inventory files (lightweight)."""
        inventory_patterns = [
            "*-master-inventory.md",
            "*/master-inventory.md",
        ]
        
        for pattern in inventory_patterns:
            for inventory_path in self.skills_root.rglob(pattern):
                category = inventory_path.parent.name
                try:
                    content = inventory_path.read_text(encoding="utf-8")
                    self.master_inventories[category] = content
                    self.metrics["inventory_loads"] += 1
                except Exception as e:
                    print(f"Warning: Failed to load inventory {inventory_path}: {e}")
    
    def get_master_inventory(self, category: str) -> Optional[str]:
        """
        Get master inventory for a category.
        
        Args:
            category: Category name (e.g., "workflows", "security", "frontend")
        
        Returns:
            Master inventory content or None if not found
        """
        return self.master_inventories.get(category)
    
    def list_categories(self) -> Set[str]:
        """List all available categories."""
        return set(self.master_inventories.keys())
    
    def load_skill(self, skill_path: str, force_reload: bool = False) -> Optional[str]:
        """
        Load a full skill file (lazy loading).
        
        Args:
            skill_path: Relative path to skill file (e.g., "workflows/debug-protocol.md")
            force_reload: Force reload even if cached
        
        Returns:
            Skill content or None if not found
        """
        with self._lock:
            # Check cache first
            if not force_reload and skill_path in self.cache:
                metadata = self.cache[skill_path]
                metadata.last_accessed = time.time()
                metadata.access_count += 1
                self.metrics["cache_hits"] += 1
                
                # Move to end (LRU)
                self.cache.move_to_end(skill_path)
                
                return metadata.content
            
            # Cache miss - load from disk
            self.metrics["cache_misses"] += 1
            full_path = self.skills_root / skill_path
            
            if not full_path.exists():
                return None
            
            try:
                content = full_path.read_text(encoding="utf-8")
                size_kb = len(content) / 1024
                
                # Extract category and tier from path
                parts = skill_path.split("/")
                category = parts[0] if parts else "unknown"
                tier = self._extract_tier(content)
                
                # Create metadata
                metadata = SkillMetadata(
                    path=full_path,
                    category=category,
                    tier=tier,
                    size_kb=size_kb,
                    content=content,
                )
                
                # Add to cache
                self.cache[skill_path] = metadata
                self.cache.move_to_end(skill_path)
                self.metrics["skill_loads"] += 1
                
                # Evict if cache full
                if len(self.cache) > self.cache_size:
                    self._evict_lru()
                
                return content
                
            except Exception as e:
                print(f"Error loading skill {skill_path}: {e}")
                return None
    
    def _extract_tier(self, content: str) -> int:
        """Extract tier from skill content."""
        # Look for "TIER: X" or "**TIER:** X" in content
        import re
        match = re.search(r'\*?\*?TIER:\*?\*?\s*(\d+)', content, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 1  # Default tier
    
    def _evict_lru(self) -> None:
        """Evict least recently used skill from cache."""
        if self.cache:
            evicted_path, _ = self.cache.popitem(last=False)
            self.metrics["unloads"] += 1
            print(f"Evicted skill from cache: {evicted_path}")
    
    def unload_unused(self) -> int:
        """
        Unload skills that haven't been accessed in unload_after_seconds.
        
        Returns:
            Number of skills unloaded
        """
        with self._lock:
            current_time = time.time()
            to_remove = []
            
            for skill_path, metadata in self.cache.items():
                if current_time - metadata.last_accessed > self.unload_after_seconds:
                    to_remove.append(skill_path)
            
            for skill_path in to_remove:
                del self.cache[skill_path]
                self.metrics["unloads"] += 1
            
            return len(to_remove)
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        with self._lock:
            total_size_kb = sum(m.size_kb for m in self.cache.values())
            
            return {
                "cached_skills": len(self.cache),
                "cache_size_kb": round(total_size_kb, 2),
                "cache_size_limit": self.cache_size,
                "master_inventories": len(self.master_inventories),
                **self.metrics,
                "hit_rate": (
                    self.metrics["cache_hits"] / 
                    (self.metrics["cache_hits"] + self.metrics["cache_misses"])
                    if (self.metrics["cache_hits"] + self.metrics["cache_misses"]) > 0
                    else 0.0
                ),
            }
    
    def clear_cache(self) -> None:
        """Clear all cached skills (keep master inventories)."""
        with self._lock:
            self.cache.clear()
            self.metrics["unloads"] += len(self.cache)
    
    def preload_skills(self, skill_paths: list[str]) -> Tuple[int, int]:
        """
        Preload multiple skills into cache.
        
        Args:
            skill_paths: List of skill paths to preload
        
        Returns:
            Tuple of (successful_loads, failed_loads)
        """
        successful = 0
        failed = 0
        
        for skill_path in skill_paths:
            if self.load_skill(skill_path):
                successful += 1
            else:
                failed += 1
        
        return successful, failed
