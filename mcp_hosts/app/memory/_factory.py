from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory
import app.core.config as cfg 
from .in_memory import get_or_create as get_or_create_in_memory_chat_history

def get_chat_message_history(session_id: str) -> ChatMessageHistory:
    """
    Factory function to get or create a chat message history instance.
    
    This function determines which type of memory backend to use based on
    the MEMORY_TYPE configuration and returns an appropriate chat history
    instance for the given session ID.
    
    Args:
        session_id (str): Unique identifier for the conversation session
        
    Returns:
        ChatMessageHistory: An instance of a chat message history handler
        
    Raises:
        TypeError: If the configured memory type is not supported
    """
    memory_type = cfg.MEMORY_TYPE
    if memory_type == 'redis':
        return RedisChatMessageHistory(session_id, url=cfg.REDIS_URL)
    elif memory_type == "in-memory":
        return get_or_create_in_memory_chat_history(session_id)
    else:
        raise TypeError(f'Not supported memory type {memory_type}')