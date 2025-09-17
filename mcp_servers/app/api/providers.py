"""
Providers API endpoint for the MCP Servers.

This module defines the endpoint for providing provider configurations to agent hosts.
"""
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from app.dependencies import get_providers as get_providers_dp

router = APIRouter()

@router.get("/providers", 
         summary="Get All Provider Configurations",
         response_model=List[Dict[str, str]])
def get_providers():
    """
    Provide a list of all available provider configurations.
    
    Agent hosts will call this endpoint when starting up to discover capabilities.
    
    Returns:
        List[Dict[str, str]]: List of provider configurations
        
    Raises:
        HTTPException: If provider configurations are unavailable or invalid
    """
    providers = get_providers_dp()
    
    if not providers:
        raise HTTPException(
            status_code=503, 
            detail="Provider configurations are currently unavailable or invalid."
        )
        
    return providers