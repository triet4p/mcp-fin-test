from . import gptcache, redis, in_memory
import app.core.config as cfg

def get_agent_cache():
    if not cfg.LLM_CACHE_ENABLED:
        return None
    if cfg.LLM_CACHE_TYPE == 'gptcache':
        module_to_load = gptcache
    elif cfg.LLM_CACHE_TYPE == 'redis':
        module_to_load = redis
    elif cfg.LLM_CACHE_TYPE == 'in-memory':
        module_to_load = in_memory
    else:
        raise TypeError(f'Not supported agent cache with cache type {cfg.LLM_CACHE_TYPE}')
    return module_to_load.get_cache()