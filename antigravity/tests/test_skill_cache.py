"""
Unit tests for SkillCache

Tests cover:
- Basic cache operations (get, put, clear)
- LRU eviction policy
- Thread safety
- Metrics tracking
- Edge cases
"""

import threading
import time
import unittest
from datetime import datetime

from antigravity.core.skill_cache import SkillCache, CacheMetrics, CacheEntry


class TestCacheMetrics(unittest.TestCase):
    """Test CacheMetrics dataclass."""
    
    def test_initial_metrics(self):
        """Test initial metrics are zero."""
        metrics = CacheMetrics()
        self.assertEqual(metrics.hits, 0)
        self.assertEqual(metrics.misses, 0)
        self.assertEqual(metrics.evictions, 0)
        self.assertEqual(metrics.total_requests, 0)
    
    def test_hit_rate_zero_requests(self):
        """Test hit rate is 0.0 when no requests."""
        metrics = CacheMetrics()
        self.assertEqual(metrics.hit_rate, 0.0)
    
    def test_hit_rate_calculation(self):
        """Test hit rate calculation."""
        metrics = CacheMetrics(hits=7, misses=3, total_requests=10)
        self.assertEqual(metrics.hit_rate, 0.7)
    
    def test_miss_rate_calculation(self):
        """Test miss rate calculation."""
        metrics = CacheMetrics(hits=7, misses=3, total_requests=10)
        self.assertEqual(metrics.miss_rate, 0.3)
    
    def test_to_dict(self):
        """Test metrics conversion to dictionary."""
        metrics = CacheMetrics(hits=5, misses=5, evictions=2, total_requests=10)
        result = metrics.to_dict()
        
        self.assertEqual(result["hits"], 5)
        self.assertEqual(result["misses"], 5)
        self.assertEqual(result["evictions"], 2)
        self.assertEqual(result["total_requests"], 10)
        self.assertEqual(result["hit_rate"], 0.5)
        self.assertEqual(result["miss_rate"], 0.5)


class TestCacheEntry(unittest.TestCase):
    """Test CacheEntry dataclass."""
    
    def test_entry_creation(self):
        """Test cache entry creation."""
        entry = CacheEntry(content="test content", path="/test/path.md")
        
        self.assertEqual(entry.content, "test content")
        self.assertEqual(entry.path, "/test/path.md")
        self.assertEqual(entry.access_count, 0)
        self.assertIsInstance(entry.cached_at, datetime)
        self.assertIsInstance(entry.last_accessed, datetime)


class TestSkillCacheBasics(unittest.TestCase):
    """Test basic cache operations."""
    
    def setUp(self):
        """Create a fresh cache for each test."""
        self.cache = SkillCache(max_size=3)
    
    def test_initialization(self):
        """Test cache initialization."""
        cache = SkillCache(max_size=20)
        self.assertEqual(cache._max_size, 20)
        self.assertEqual(cache.size(), 0)
    
    def test_initialization_invalid_size(self):
        """Test initialization with invalid size raises error."""
        with self.assertRaises(ValueError):
            SkillCache(max_size=0)
        
        with self.assertRaises(ValueError):
            SkillCache(max_size=-1)
    
    def test_put_and_get(self):
        """Test basic put and get operations."""
        self.cache.put("/skill1.md", "content1")
        result = self.cache.get("/skill1.md")
        
        self.assertEqual(result, "content1")
    
    def test_get_nonexistent(self):
        """Test getting non-existent skill returns None."""
        result = self.cache.get("/nonexistent.md")
        self.assertIsNone(result)
    
    def test_put_updates_existing(self):
        """Test putting same path updates content."""
        self.cache.put("/skill1.md", "content1")
        self.cache.put("/skill1.md", "content2")
        
        result = self.cache.get("/skill1.md")
        self.assertEqual(result, "content2")
        self.assertEqual(self.cache.size(), 1)
    
    def test_clear(self):
        """Test clearing cache."""
        self.cache.put("/skill1.md", "content1")
        self.cache.put("/skill2.md", "content2")
        
        self.assertEqual(self.cache.size(), 2)
        
        self.cache.clear()
        
        self.assertEqual(self.cache.size(), 0)
        self.assertIsNone(self.cache.get("/skill1.md"))
    
    def test_contains(self):
        """Test contains method."""
        self.cache.put("/skill1.md", "content1")
        
        self.assertTrue(self.cache.contains("/skill1.md"))
        self.assertFalse(self.cache.contains("/skill2.md"))
    
    def test_size(self):
        """Test size method."""
        self.assertEqual(self.cache.size(), 0)
        
        self.cache.put("/skill1.md", "content1")
        self.assertEqual(self.cache.size(), 1)
        
        self.cache.put("/skill2.md", "content2")
        self.assertEqual(self.cache.size(), 2)


class TestLRUEviction(unittest.TestCase):
    """Test LRU eviction policy."""
    
    def setUp(self):
        """Create a cache with size 3 for testing."""
        self.cache = SkillCache(max_size=3)
    
    def test_eviction_when_full(self):
        """Test LRU eviction when cache is full."""
        # Fill cache
        self.cache.put("/skill1.md", "content1")
        self.cache.put("/skill2.md", "content2")
        self.cache.put("/skill3.md", "content3")
        
        # Add one more - should evict skill1 (least recently used)
        self.cache.put("/skill4.md", "content4")
        
        self.assertEqual(self.cache.size(), 3)
        self.assertIsNone(self.cache.get("/skill1.md"))
        self.assertIsNotNone(self.cache.get("/skill2.md"))
        self.assertIsNotNone(self.cache.get("/skill3.md"))
        self.assertIsNotNone(self.cache.get("/skill4.md"))
    
    def test_lru_order_with_access(self):
        """Test LRU order is updated on access."""
        # Fill cache
        self.cache.put("/skill1.md", "content1")
        self.cache.put("/skill2.md", "content2")
        self.cache.put("/skill3.md", "content3")
        
        # Access skill1 - makes it most recently used
        self.cache.get("/skill1.md")
        
        # Add skill4 - should evict skill2 (now least recently used)
        self.cache.put("/skill4.md", "content4")
        
        self.assertIsNotNone(self.cache.get("/skill1.md"))
        self.assertIsNone(self.cache.get("/skill2.md"))
        self.assertIsNotNone(self.cache.get("/skill3.md"))
        self.assertIsNotNone(self.cache.get("/skill4.md"))
    
    def test_eviction_order(self):
        """Test multiple evictions maintain LRU order."""
        self.cache.put("/skill1.md", "content1")
        self.cache.put("/skill2.md", "content2")
        self.cache.put("/skill3.md", "content3")
        
        # skill1, skill2, skill3 in cache
        
        self.cache.put("/skill4.md", "content4")
        # skill2, skill3, skill4 in cache (skill1 evicted)
        
        self.cache.put("/skill5.md", "content5")
        # skill3, skill4, skill5 in cache (skill2 evicted)
        
        self.assertIsNone(self.cache.get("/skill1.md"))
        self.assertIsNone(self.cache.get("/skill2.md"))
        self.assertIsNotNone(self.cache.get("/skill3.md"))
        self.assertIsNotNone(self.cache.get("/skill4.md"))
        self.assertIsNotNone(self.cache.get("/skill5.md"))
    
    def test_evict_empty_cache(self):
        """Test evicting from empty cache returns None."""
        with self.cache._lock:
            result = self.cache.evict()
        self.assertIsNone(result)


class TestCacheMetricsTracking(unittest.TestCase):
    """Test metrics tracking."""
    
    def setUp(self):
        """Create a fresh cache for each test."""
        self.cache = SkillCache(max_size=3)
    
    def test_hit_tracking(self):
        """Test cache hits are tracked."""
        self.cache.put("/skill1.md", "content1")
        
        self.cache.get("/skill1.md")
        self.cache.get("/skill1.md")
        
        metrics = self.cache.get_metrics()
        self.assertEqual(metrics["hits"], 2)
        self.assertEqual(metrics["total_requests"], 2)
    
    def test_miss_tracking(self):
        """Test cache misses are tracked."""
        self.cache.get("/nonexistent1.md")
        self.cache.get("/nonexistent2.md")
        
        metrics = self.cache.get_metrics()
        self.assertEqual(metrics["misses"], 2)
        self.assertEqual(metrics["total_requests"], 2)
    
    def test_eviction_tracking(self):
        """Test evictions are tracked."""
        # Fill cache
        self.cache.put("/skill1.md", "content1")
        self.cache.put("/skill2.md", "content2")
        self.cache.put("/skill3.md", "content3")
        
        # Trigger eviction
        self.cache.put("/skill4.md", "content4")
        
        metrics = self.cache.get_metrics()
        self.assertEqual(metrics["evictions"], 1)
    
    def test_hit_rate_calculation(self):
        """Test hit rate is calculated correctly."""
        self.cache.put("/skill1.md", "content1")
        
        # 3 hits, 2 misses
        self.cache.get("/skill1.md")
        self.cache.get("/skill1.md")
        self.cache.get("/skill1.md")
        self.cache.get("/nonexistent1.md")
        self.cache.get("/nonexistent2.md")
        
        metrics = self.cache.get_metrics()
        self.assertEqual(metrics["hit_rate"], 0.6)
        self.assertEqual(metrics["miss_rate"], 0.4)
    
    def test_metrics_include_size(self):
        """Test metrics include current and max size."""
        self.cache.put("/skill1.md", "content1")
        self.cache.put("/skill2.md", "content2")
        
        metrics = self.cache.get_metrics()
        self.assertEqual(metrics["current_size"], 2)
        self.assertEqual(metrics["max_size"], 3)


class TestThreadSafety(unittest.TestCase):
    """Test thread-safe operations."""
    
    def test_concurrent_puts(self):
        """Test concurrent put operations are thread-safe."""
        cache = SkillCache(max_size=100)
        
        def put_skills(start_idx):
            for i in range(start_idx, start_idx + 10):
                cache.put(f"/skill{i}.md", f"content{i}")
        
        threads = []
        for i in range(10):
            thread = threading.Thread(target=put_skills, args=(i * 10,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Should have 100 items (cache size limit)
        self.assertEqual(cache.size(), 100)
    
    def test_concurrent_gets(self):
        """Test concurrent get operations are thread-safe."""
        cache = SkillCache(max_size=10)
        
        # Pre-populate cache
        for i in range(10):
            cache.put(f"/skill{i}.md", f"content{i}")
        
        results = []
        
        def get_skills():
            for i in range(10):
                result = cache.get(f"/skill{i}.md")
                results.append(result)
        
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=get_skills)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # All gets should succeed
        self.assertEqual(len(results), 50)
        self.assertTrue(all(r is not None for r in results))
    
    def test_concurrent_mixed_operations(self):
        """Test concurrent mixed operations are thread-safe."""
        cache = SkillCache(max_size=20)
        
        def writer():
            for i in range(20):
                cache.put(f"/skill{i}.md", f"content{i}")
                time.sleep(0.001)
        
        def reader():
            for i in range(20):
                cache.get(f"/skill{i}.md")
                time.sleep(0.001)
        
        threads = []
        for _ in range(3):
            threads.append(threading.Thread(target=writer))
            threads.append(threading.Thread(target=reader))
        
        for thread in threads:
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Cache should be in valid state
        self.assertLessEqual(cache.size(), 20)


class TestEntryInfo(unittest.TestCase):
    """Test entry information retrieval."""
    
    def setUp(self):
        """Create a fresh cache for each test."""
        self.cache = SkillCache(max_size=5)
    
    def test_get_entry_info(self):
        """Test getting entry information."""
        self.cache.put("/skill1.md", "test content")
        
        info = self.cache.get_entry_info("/skill1.md")
        
        self.assertIsNotNone(info)
        self.assertEqual(info["path"], "/skill1.md")
        self.assertEqual(info["access_count"], 0)
        self.assertEqual(info["content_length"], len("test content"))
        self.assertIn("cached_at", info)
        self.assertIn("last_accessed", info)
    
    def test_get_entry_info_nonexistent(self):
        """Test getting info for non-existent entry returns None."""
        info = self.cache.get_entry_info("/nonexistent.md")
        self.assertIsNone(info)
    
    def test_access_count_increments(self):
        """Test access count increments on get."""
        self.cache.put("/skill1.md", "content")
        
        self.cache.get("/skill1.md")
        self.cache.get("/skill1.md")
        self.cache.get("/skill1.md")
        
        info = self.cache.get_entry_info("/skill1.md")
        self.assertEqual(info["access_count"], 3)
    
    def test_get_all_paths(self):
        """Test getting all cached paths."""
        self.cache.put("/skill1.md", "content1")
        self.cache.put("/skill2.md", "content2")
        self.cache.put("/skill3.md", "content3")
        
        paths = self.cache.get_all_paths()
        
        self.assertEqual(len(paths), 3)
        self.assertIn("/skill1.md", paths)
        self.assertIn("/skill2.md", paths)
        self.assertIn("/skill3.md", paths)
    
    def test_get_all_paths_empty(self):
        """Test getting paths from empty cache."""
        paths = self.cache.get_all_paths()
        self.assertEqual(paths, [])


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""
    
    def test_cache_size_one(self):
        """Test cache with size 1."""
        cache = SkillCache(max_size=1)
        
        cache.put("/skill1.md", "content1")
        self.assertEqual(cache.size(), 1)
        
        cache.put("/skill2.md", "content2")
        self.assertEqual(cache.size(), 1)
        self.assertIsNone(cache.get("/skill1.md"))
        self.assertIsNotNone(cache.get("/skill2.md"))
    
    def test_empty_content(self):
        """Test caching empty content."""
        cache = SkillCache(max_size=5)
        cache.put("/empty.md", "")
        
        result = cache.get("/empty.md")
        self.assertEqual(result, "")
    
    def test_large_content(self):
        """Test caching large content."""
        cache = SkillCache(max_size=5)
        large_content = "x" * 1000000  # 1MB
        
        cache.put("/large.md", large_content)
        result = cache.get("/large.md")
        
        self.assertEqual(result, large_content)
    
    def test_special_characters_in_path(self):
        """Test paths with special characters."""
        cache = SkillCache(max_size=5)
        
        paths = [
            "/path/with spaces.md",
            "/path/with-dashes.md",
            "/path/with_underscores.md",
            "/path/with.dots.md"
        ]
        
        for path in paths:
            cache.put(path, f"content for {path}")
        
        for path in paths:
            result = cache.get(path)
            self.assertEqual(result, f"content for {path}")


if __name__ == "__main__":
    unittest.main()
