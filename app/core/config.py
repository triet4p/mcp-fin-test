import os
from dotenv import load_dotenv

load_dotenv()

# Biến môi trường để quyết định dùng LLM nào
LLM_PROVIDER = os.getenv("LLM_PROVIDER").lower() # Mặc định là google

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

CHAT_MODEL = 'gemini-2.5-flash'

API_V1_BASE_ROUTE = os.getenv('API_V1_BASE_ROUTE')

ITAPIA_API_BASE_URL = os.getenv('ITAPIA_API_BASE_URL')

# Memory config
MEMORY_TYPE=os.getenv('MEMORY_TYPE', 'in-memory')

# Redis
REDIS_HOST=os.getenv('REDIS_HOST')
REDIS_PORT=os.getenv('REDIS_PORT')
REDIS_DB=os.getenv("REDIS_DB")
REDIS_URL=f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

PROMPT_FILE='prompts.yaml'
SYSTEM_PROMPT_ID='financial_agent_system_prompt_v1'