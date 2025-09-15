from typing import Dict
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory as InMemoryChatMessageHistory

_INMEMORY_DICT: Dict[str, InMemoryChatMessageHistory] = {}

def get_or_create(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in _INMEMORY_DICT:
        _INMEMORY_DICT[session_id] = InMemoryChatMessageHistory()
    return _INMEMORY_DICT[session_id]