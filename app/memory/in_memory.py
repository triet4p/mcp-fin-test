from typing import Dict
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory as InMemoryChatMessageHistory

# In-memory storage for chat histories, keyed by session ID
_INMEMORY_DICT: Dict[str, InMemoryChatMessageHistory] = {}

def get_or_create(session_id: str) -> InMemoryChatMessageHistory:
    """
    Get an existing chat history for a session or create a new one if it doesn't exist.
    
    This function maintains an in-memory dictionary of chat histories to ensure
    that each session gets its own persistent history throughout the application's
    lifetime.
    
    Args:
        session_id (str): Unique identifier for the conversation session
        
    Returns:
        InMemoryChatMessageHistory: The chat history for the specified session
    """
    if session_id not in _INMEMORY_DICT:
        _INMEMORY_DICT[session_id] = InMemoryChatMessageHistory()
    return _INMEMORY_DICT[session_id]