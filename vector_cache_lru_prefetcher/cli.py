"""CLI for vector-cache-lru-prefetcher."""
import sys
import argparse
from .cache import VectorLRUPrefetcher

def main():
    parser = argparse.ArgumentParser(description="Vector Cache LRU Prefetcher CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate vector cache hit and prefetch")
    args = parser.parse_args()

    if args.demo:
        cache = VectorLRUPrefetcher(capacity=10, similarity_threshold=0.90)
        v1 = [1.0, 0.0]
        cache.put("entry_1", v1, ["result_a", "result_b"])
        
        # Query with slightly perturbed vector (cosine ~ 0.999)
        v_near = [0.99, 0.05]
        hit = cache.get(v_near)
        print(f"Query near v1 -> Cache Hit: {hit is not None} (Hits={cache.hits}, Misses={cache.misses})")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
