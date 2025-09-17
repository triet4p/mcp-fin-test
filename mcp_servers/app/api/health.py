"""
Health check API endpoint for the MCP Servers.

This module provides a simple health check endpoint to monitor application status.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get('/health', status_code=200)
def health_check():
    """
    Health check endpoint.
    
    Returns a simple status response to indicate the application is running.
    
    Returns:
        dict: Contains the status of the application
    """
    return {'status': 'ok'}