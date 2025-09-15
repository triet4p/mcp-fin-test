from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory
import app.core.config as cfg 
from .in_memory import get_or_create as get_or_create_in_memory_chat_history

def get_chat_message_history(session_id: str) -> ChatMessageHistory:
    memory_type = cfg.MEMORY_TYPE
    if memory_type == 'redis':
        return RedisChatMessageHistory(session_id, url=cfg.REDIS_URL)
    elif memory_type == "in-memory":
        return get_or_create_in_memory_chat_history(session_id)
    else:
        raise TypeError(f'Not supported memory type {memory_type}')