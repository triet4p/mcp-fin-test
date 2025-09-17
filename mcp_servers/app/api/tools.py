"""
Tools API endpoint for the MCP Servers.

This module defines the endpoint for providing tool specifications to agent hosts.
"""
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from app.dependencies import get_tools as get_tools_dp

router = APIRouter()

@router.get("/tools", 
         summary="Get All Tool Specifications",
         response_model=List[Dict[str, Any]])
def get_tools():
    """
    Provide a list of all available tool specifications.
    
    Agent hosts will call this endpoint when starting up to discover capabilities.
    
    Returns:
        List[Dict[str, Any]]: List of tool specifications
        
    Raises:
        HTTPException: If tool configurations are unavailable or invalid
    """
    tools = get_tools_dp()
    
    if not tools:
        raise HTTPException(
            status_code=503, 
            detail="Tool configurations are currently unavailable or invalid."
        )
        
    return tools