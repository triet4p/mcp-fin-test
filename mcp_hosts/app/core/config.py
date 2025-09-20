"""
Configuration module for the MCP Financial Agent.

This module loads environment variables and sets up configuration constants
used throughout the application. It handles LLM provider settings, API keys,
memory configuration, and other application-level settings.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# LLM provider configuration - determines which language model to use
# Valid options: 'google', 'openai', 'openrouter', 'ollama'
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google").lower()

# API keys for different LLM providers
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", 'https://openrouter.ai/api/v1')
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

# Default chat model to use
CHAT_MODEL = os.getenv('CHAT_MODEL')
if CHAT_MODEL is None:
    if LLM_PROVIDER == "google" and GOOGLE_API_KEY:
        CHAT_MODEL = 'gemini-2.5-flash'
    elif LLM_PROVIDER == "openai" and OPENAI_API_KEY:
        CHAT_MODEL = 'gpt-4o-mini'  # Fixed: was incorrectly checking GOOGLE_API_KEY again

# API base route configuration
API_V1_BASE_ROUTE = os.getenv('API_V1_BASE_ROUTE', '/api/v1')

# Memory configuration - determines which memory backend to use
# Valid options: 'in-memory', 'redis'
MEMORY_TYPE = os.getenv('MEMORY_TYPE', 'in-memory')

# Redis configuration for persistent memory storage
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')
REDIS_DB = os.getenv("REDIS_DB", '0')
REDIS_TTL = int(os.getenv('REDIS_TTL', '3600'))
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

# Chroma host
CHROMA_HOST = os.getenv('CHROMA_HOST', 'localhost')
CHROMA_PORT = os.getenv('CHROMA_PORT', '8000')


# Prompt configuration
PROMPT_FILE = 'prompts.yaml'
SYSTEM_PROMPT_ID = 'financial_agent_system_prompt_v1'

# LLM caching configuration
LLM_CACHE_ENABLED = True if os.getenv('LLM_CACHE_ENABLED', 'false').lower() in ['true', '1'] else False
LLM_CACHE_TYPE = os.getenv('LLM_CACHE_TYPE', 'gptcache')

# Embedding
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'intfloat/multilingual-e5-small')

# MCP Servers registry URL for tool discovery
MCP_SERVERS_REGISTRY_URL = os.getenv("MCP_SERVERS_REGISTRY_URL")