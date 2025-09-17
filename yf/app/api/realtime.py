"""
Real-time price API endpoint for the Yahoo Finance service.

This module defines the endpoint for retrieving real-time stock prices from Yahoo Finance.
"""
from fastapi import APIRouter
from app.schemas import StockRealtimePrice
from app.tools.fetch_realtime_stock import fetch_stock_realtime_price

router = APIRouter()

@router.get('/market/tickers/{ticker}/price/realtime', 
            response_model=StockRealtimePrice)
def get_stock_realtime_price(ticker: str) -> StockRealtimePrice:
    """
    Get real-time stock price data from Yahoo Finance.
    
    This endpoint retrieves current price information for a specified stock ticker
    from Yahoo Finance's API.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., AAPL, MSFT, FPT)
        
    Returns:
        StockRealtimePrice: Real-time price data or error information
    """
    return fetch_stock_realtime_price(ticker)