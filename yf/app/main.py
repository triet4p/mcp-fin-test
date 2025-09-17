"""
Main application module for the Yahoo Finance service.

This module initializes the FastAPI application and sets up the API routes
for the Yahoo Finance real-time price service.
"""
from fastapi import FastAPI

from app.api import health, realtime

from app.core.config import API_V1_BASE_ROUTE

app = FastAPI(
    title='Yahoo Finance Real-time Price Service',
    description='MCP service for retrieving real-time stock prices from Yahoo Finance',
    version='0.0.1'
)

# Include the health check endpoint for monitoring application status
app.include_router(health.router, prefix=API_V1_BASE_ROUTE, tags=['HEALTH'])

# Include the real-time price endpoint for retrieving stock prices
app.include_router(realtime.router, prefix=API_V1_BASE_ROUTE, tags=['realtime price'])
