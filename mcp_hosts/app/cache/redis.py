from langchain_core.caches import BaseCache
from langchain_community.cache import RedisCache
import redis
import app.core.config as cfg

def get_cache() -> BaseCache:
    try:
        print(f"INFO:     Enabling LLM Caching with Redis at {cfg.REDIS_URL}")
        redis_client = redis.from_url(cfg.REDIS_URL)
        return RedisCache(redis_client)
    except Exception as e:
        print(f"WARNING:  Could not enable LLM Caching: {e}")