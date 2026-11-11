"""Unit tests for vector-cache-lru-prefetcher."""
import unittest
from vector_cache_lru_prefetcher.cache import VectorLRUPrefetcher

class TestVectorLRUPrefetcher(unittest.TestCase):
    def setUp(self):
        self.cache = VectorLRUPrefetcher(capacity=2, similarity_threshold=0.90)

    def test_semantic_hit(self):
        self.cache.put("k1", [1.0, 0.0], "doc_data")
        val = self.cache.get([0.98, 0.02])
        self.assertEqual(val, "doc_data")
        self.assertEqual(self.cache.hits, 1)

    def test_lru_eviction(self):
        self.cache.put("k1", [1.0, 0.0], "v1")
        self.cache.put("k2", [0.0, 1.0], "v2")
        self.cache.put("k3", [0.5, 0.5], "v3")  # Evicts k1
        self.assertEqual(len(self.cache.cache), 2)
