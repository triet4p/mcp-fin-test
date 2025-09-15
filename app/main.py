from fastapi import FastAPI

from app.api import health, interact

from app.core.config import API_V1_BASE_ROUTE

app = FastAPI(
    title='MCP Servers test for stock',
    description='Một MCP đơn giản để lấy giá realtime của stock',
    version='0.0.1'
)

app.include_router(health.router, prefix=API_V1_BASE_ROUTE, tags=['HEALTH'])
app.include_router(interact.router, prefix=API_V1_BASE_ROUTE, tags=['INTERACT'])
