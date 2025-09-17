"""
Main application module for the MCP Financial Agent.

This module initializes the FastAPI application and sets up the API routes.
"""
from fastapi import FastAPI

from app.api import health, interact

from app.core.config import API_V1_BASE_ROUTE

app = FastAPI(
    title='MCP Financial Agent',
    description='An AI-powered financial agent built on the Model-Context-Protocol for stock analysis',
    version='0.0.1'
)

# Include the health check endpoint for monitoring application status
app.include_router(health.router, prefix=API_V1_BASE_ROUTE, tags=['HEALTH'])

# Include the main interaction endpoint for the financial agent
app.include_router(interact.router, prefix=API_V1_BASE_ROUTE, tags=['INTERACT'])
