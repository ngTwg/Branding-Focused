"""
LRU Cache for Atomic Skills

Provides an LRU (Least Recently Used) cache system for atomic skills to optimize
memory usage and loading performance. Thread-safe implementation with metrics tracking.

Design:
- LRU Cache with configurable size (default: 20 slots)
- Cache key: skill file path
- Eviction policy: Least Recently Used
- Metrics: hit rate, miss rate, eviction count
- Thread-safe using threading.Lock
"""

import threading
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class CacheMetrics:
    """Metrics for cache performance tracking."""
    
    hits: int = 0
    misses: int = 0
    evictions: int = 0
    total_requests: int = 0
    
    @property
    def hit_rate(self) -> float:
        """Calculate cache hit rate (0.0 to 1.0)."""
        if self.total_requests == 0:
            return 0.0
        return self.hits / self.total_requests
    
    @property
    def miss_rate(self) -> float:
        """Calculate cache miss rate (0.0 to 1.0)."""
        if self.total_requests == 0:
            return 0.0
        return self.misses / self.total_requests
    
    def to_dict(self) -> dict:
        """Convert metrics to dictionary format."""
        return {
            "hits": self.hits,
            "misses": self.misses,
            "evictions": self.evictions,
            "total_requests": self.total_requests,
            "hit_rate": self.hit_rate,
            "miss_rate": self.miss_rate
        }


@dataclass
class CacheEntry:
    """Entry in the skill cache."""
    
    content: str
    path: str
    cached_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0


class SkillCache:
    """
    LRU Cache for atomic skills with thread-safe operations.
    
    Features:
    - LRU eviction policy
    - Thread-safe operations
    - Metrics tracking (hit rate, miss rate, evictions)
    - Configurable cache size
    
    Example:
        cache = SkillCache(max_size=20)
        
        # Cache a skill
        cache.put("/path/to/skill.md", "skill content...")
        
        # Retrieve from cache
        content = cache.get("/path/to/skill.md")
        
        # Get metrics
        metrics = cache.get_metrics()
        print(f"Hit rate: {metrics['hit_rate']:.2%}")
    """
    
    def __init__(self, max_size: int = 20):
        """
        Initialize the skill cache.
        
        Args:
            max_size: Maximum number of skills to cache (default: 20)
        """
        if max_size <= 0:
            raise ValueError("max_size must be positive")
        
        self._max_size = max_size
        self._cache: OrderedDict[str, CacheEntry] = OrderedDict()
        self._lock = threading.Lock()
        self._metrics = CacheMetrics()
    
    def get(self, skill_path: str) -> Optional[str]:
        """
        Get cached skill content.
        
        Args:
            skill_path: Path to the skill file (cache key)
        
        Returns:
            Cached skill content if found, None otherwise
        """
        with self._lock:
            self._metrics.total_requests += 1
            
            if skill_path in self._cache:
                # Cache hit - move to end (most recently used)
                entry = self._cache.pop(skill_path)
                entry.last_accessed = datetime.now()
                entry.access_count += 1
                self._cache[skill_path] = entry
                
                self._metrics.hits += 1
                return entry.content
            else:
                # Cache miss
                self._metrics.misses += 1
                return None
    
    def put(self, skill_path: str, content: str) -> None:
        """
        Cache skill content.
        
        Args:
            skill_path: Path to the skill file (cache key)
            content: Skill content to cache
        """
        with self._lock:
            # If already exists, update and move to end
            if skill_path in self._cache:
                self._cache.pop(skill_path)
            
            # Check if cache is full
            elif len(self._cache) >= self._max_size:
                self.evict()
            
            # Add new entry
            entry = CacheEntry(
                content=content,
                path=skill_path,
                cached_at=datetime.now(),
                last_accessed=datetime.now(),
                access_count=0
            )
            self._cache[skill_path] = entry
    
    def evict(self) -> Optional[str]:
        """
        Remove least recently used item from cache.
        
        Returns:
            Path of evicted skill, or None if cache is empty
        """
        # Note: This method assumes lock is already held by caller
        if not self._cache:
            return None
        
        # Remove first item (least recently used)
        evicted_path, _ = self._cache.popitem(last=False)
        self._metrics.evictions += 1
        return evicted_path
    
    def get_metrics(self) -> dict:
        """
        Get cache performance metrics.
        
        Returns:
            Dictionary containing:
            - hits: Number of cache hits
            - misses: Number of cache misses
            - evictions: Number of evictions
            - total_requests: Total cache requests
            - hit_rate: Cache hit rate (0.0 to 1.0)
            - miss_rate: Cache miss rate (0.0 to 1.0)
            - current_size: Current number of cached items
            - max_size: Maximum cache size
        """
        with self._lock:
            metrics = self._metrics.to_dict()
            metrics["current_size"] = len(self._cache)
            metrics["max_size"] = self._max_size
            return metrics
    
    def clear(self) -> None:
        """Clear all cached skills."""
        with self._lock:
            self._cache.clear()
    
    def contains(self, skill_path: str) -> bool:
        """
        Check if skill is in cache.
        
        Args:
            skill_path: Path to the skill file
        
        Returns:
            True if skill is cached, False otherwise
        """
        with self._lock:
            return skill_path in self._cache
    
    def size(self) -> int:
        """
        Get current cache size.
        
        Returns:
            Number of items currently in cache
        """
        with self._lock:
            return len(self._cache)
    
    def get_entry_info(self, skill_path: str) -> Optional[dict]:
        """
        Get information about a cached entry.
        
        Args:
            skill_path: Path to the skill file
        
        Returns:
            Dictionary with entry info, or None if not cached
        """
        with self._lock:
            if skill_path not in self._cache:
                return None
            
            entry = self._cache[skill_path]
            return {
                "path": entry.path,
                "cached_at": entry.cached_at.isoformat(),
                "last_accessed": entry.last_accessed.isoformat(),
                "access_count": entry.access_count,
                "content_length": len(entry.content)
            }
    
    def get_all_paths(self) -> list[str]:
        """
        Get list of all cached skill paths.
        
        Returns:
            List of cached skill paths (ordered by LRU)
        """
        with self._lock:
            return list(self._cache.keys())
