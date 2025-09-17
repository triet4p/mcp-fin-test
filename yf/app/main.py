from fastapi import FastAPI

from app.api import health, realtime

from app.core.config import API_V1_BASE_ROUTE

app = FastAPI(
    title='MCP Servers test for stock',
    description='Một MCP đơn giản để lấy giá realtime của stock',
    version='0.0.1'
)

# Include the health check endpoint for monitoring application status
app.include_router(health.router, prefix=API_V1_BASE_ROUTE, tags=['HEALTH'])

# Include the main interaction endpoint for the financial agent
app.include_router(realtime.router, prefix=API_V1_BASE_ROUTE, tags=['realtime price'])
