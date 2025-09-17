"""
Interaction API endpoint for the MCP Financial Agent.

This module defines the FastAPI router and endpoint for user-agent interactions.
"""
from fastapi import APIRouter
from app.agent import get_agent_response
from app.schemas.interact import InteractionRequest, InteractionResponse

router = APIRouter()

@router.post('/interact', response_model=InteractionResponse)
def interact(request: InteractionRequest):
    """
    Main endpoint for interacting with the financial agent.
    
    This endpoint receives user messages and processes them through the agent,
    which may use various tools to gather information and formulate responses.
    
    Example request:
    ```
    {
        "session_id": "session_123",
        "message": "What is the current price of AAPL?"
    }
    ```
    
    Args:
        request (InteractionRequest): Contains the session ID and user message
        
    Returns:
        InteractionResponse: Contains the agent's response to the user message
    """
    result = get_agent_response(
        session_id=request.session_id,
        user_message=request.message
    )
    return InteractionResponse.model_validate(result)