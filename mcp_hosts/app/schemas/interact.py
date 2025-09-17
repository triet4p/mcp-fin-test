"""
Pydantic schemas for the interaction API endpoint.

This module defines the request and response schemas for the main interaction endpoint.
"""
from pydantic import BaseModel

class InteractionRequest(BaseModel):
    """
    Schema for interaction requests to the financial agent.
    
    Attributes:
        session_id (str): Unique identifier for the conversation session
        message (str): The user's input message to the agent
    """
    session_id: str
    message: str

class InteractionResponse(BaseModel):
    """
    Schema for interaction responses from the financial agent.
    
    Attributes:
        response (str): The agent's response to the user message
    """
    response: str