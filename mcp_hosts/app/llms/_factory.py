"""
LLM factory module for the MCP Financial Agent.

This module provides a factory pattern implementation for creating
language model clients based on configuration. It supports multiple
LLM providers and handles caching configuration.
"""
from langchain_core.language_models.chat_models import BaseChatModel
from . import google, openai, openrouter, ollama
from langchain.globals import set_llm_cache
from langchain_community.cache import RedisCache
import app.core.config as cfg
import redis

# Set up LLM caching if enabled in configuration
if cfg.LLM_CACHE_ENABLED:
    try:
        print(f"INFO:     Enabling LLM Caching with Redis at {cfg.REDIS_URL}")
        redis_client = redis.from_url(cfg.REDIS_URL)
        set_llm_cache(RedisCache(redis_client))
    except Exception as e:
        print(f"WARNING:  Could not enable LLM Caching: {e}")

def get_llm_client() -> BaseChatModel:
    """
    Factory function to create and return an LLM client based on configuration.
    
    This function reads the LLM_PROVIDER environment variable to determine
    which language model provider to use, then initializes and returns
    the appropriate client.
    
    Supported providers:
    - google: Google Gemini models
    - openai: OpenAI GPT models
    - openrouter: Models via OpenRouter API
    - ollama: Local models via Ollama
    
    Returns:
        BaseChatModel: An instance of the configured language model client
        
    Raises:
        ValueError: If the provider is not supported
    """
    if cfg.LLM_PROVIDER == "google":
        module_to_load = google
    elif cfg.LLM_PROVIDER == "openai":
        module_to_load = openai
    elif cfg.LLM_PROVIDER == 'openrouter':
        module_to_load = openrouter
    elif cfg.LLM_PROVIDER == 'ollama':
        module_to_load = ollama
    else:
        raise ValueError(f"Unsupported LLM provider: {cfg.LLM_PROVIDER}")
    
    return module_to_load.get_model()
    
# Initialize the LLM client at module load time
llm_client = get_llm_client()