from langchain_community.cache import InMemoryCache
from langchain_core.caches import BaseCache

def get_cache() -> BaseCache:
    return InMemoryCache()