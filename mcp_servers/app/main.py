"""
Main application module for the MCP Servers.

This module initializes the FastAPI application and sets up the API routes
for tools and providers endpoints.
"""
from fastapi import FastAPI

from app.api import health, tools, providers

from app.core.config import API_V1_BASE_ROUTE

app = FastAPI(
    title='MCP Servers for Financial Tools',
    description='MCP Servers that provides tool specifications and provider configurations for financial data',
    version='0.0.1'
)

# Include the health check endpoint for monitoring application status
app.include_router(health.router, prefix=API_V1_BASE_ROUTE, tags=['HEALTH'])

# Include the tools endpoint for providing tool specifications
app.include_router(tools.router, prefix=API_V1_BASE_ROUTE, tags=['tools'])

# Include the providers endpoint for providing provider configurations
app.include_router(providers.router, prefix=API_V1_BASE_ROUTE, tags=['providers'])
