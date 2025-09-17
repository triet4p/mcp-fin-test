"""
OpenAI LLM provider for the MCP Financial Agent.

This module provides the implementation for OpenAI's GPT models.
"""
from langchain_openai.chat_models import ChatOpenAI

import app.core.config as cfg

def get_model():
    """
    Create and return an OpenAI GPT language model client.
    
    Returns:
        ChatOpenAI: Configured OpenAI GPT model client
        
    Raises:
        ValueError: If OPENAI_API_KEY is not set
    """
    if not cfg.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set for the OpenAI provider.")
    return ChatOpenAI(
        model=cfg.CHAT_MODEL,
        api_key=cfg.OPENAI_API_KEY
    )