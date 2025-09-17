import os
from dotenv import load_dotenv

load_dotenv()

# LLM provider configuration - determines which language model to use
# Valid options: 'google', 'openai'
LLM_PROVIDER = os.getenv("LLM_PROVIDER").lower() # Default is google

# API keys for different LLM providers
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", 'https://openrouter.ai/api/v1')

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

# Default chat model to use
CHAT_MODEL = os.getenv('CHAT_MODEL')
if CHAT_MODEL is None:
    if GOOGLE_API_KEY:
        CHAT_MODEL = 'gemini-2.5-flash'
    elif GOOGLE_API_KEY:
        CHAT_MODEL = 'gpt-5'

# API base route configuration
API_V1_BASE_ROUTE = os.getenv('API_V1_BASE_ROUTE')

# External ITAPIA service configuration
ITAPIA_API_BASE_URL = os.getenv('ITAPIA_API_BASE_URL')

# Memory configuration - determines which memory backend to use
# Valid options: 'in-memory', 'redis'
MEMORY_TYPE=os.getenv('MEMORY_TYPE', 'in-memory')

# Redis configuration for persistent memory storage
REDIS_HOST=os.getenv('REDIS_HOST')
REDIS_PORT=os.getenv('REDIS_PORT')
REDIS_DB=os.getenv("REDIS_DB")
REDIS_URL=f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

# Prompt configuration
PROMPT_FILE='prompts.yaml'
SYSTEM_PROMPT_ID='financial_agent_system_prompt_v1'

LLM_CACHE_ENABLED=True if os.getenv('LLM_CACHE_ENABLED', 'false') in ['true', 'True', '1'] else False

MCP_SERVERS_REGISTRY_URL=os.getenv("MCP_SERVERS_REGISTRY_URL")