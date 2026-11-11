"""Core Vector Cache LRU Prefetcher implementation."""
import collections
import math
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Tuple

@dataclass
class CacheEntry:
    key_vector: List[float]
    result: Any
    timestamp: float

class VectorLRUPrefetcher:
    """Predictive semantic LRU cache that pre-warms expected neighboring vector lookups."""
    
    def __init__(self, capacity: int = 100, similarity_threshold: float = 0.92):
        self.capacity = capacity
        self.similarity_threshold = similarity_threshold
        self.cache: collections.OrderedDict[str, CacheEntry] = collections.OrderedDict()
        self.hits = 0
        self.misses = 0

    @staticmethod
    def cosine_similarity(v1: List[float], v2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        return dot / max(1e-9, (norm1 * norm2))

    def get(self, query_vector: List[float]) -> Optional[Any]:
        # Search existing entries by cosine similarity
        for key_str, entry in list(self.cache.items()):
            sim = self.cosine_similarity(query_vector, entry.key_vector)
            if sim >= self.similarity_threshold:
                self.hits += 1
                self.cache.move_to_end(key_str)
                return entry.result
        
        self.misses += 1
        return None

    def put(self, key_id: str, query_vector: List[float], result: Any) -> None:
        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)  # Evict LRU
        self.cache[key_id] = CacheEntry(query_vector, result, time.time())

    def prefetch(self, forecast_vector: List[float], fetch_fn: Callable[[List[float]], Any], key_id: str) -> None:
        # Background pre-warm
        res = fetch_fn(forecast_vector)
        self.put(key_id, forecast_vector, res)
