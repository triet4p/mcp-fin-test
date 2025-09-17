"""
Yahoo Finance real-time stock price fetcher.

This module provides functionality to fetch real-time stock price data from Yahoo Finance
using the yfinance library. It handles error cases and returns structured data.
"""
import yfinance as yf
from datetime import datetime, timezone

from app.schemas import StockRealtimePrice

def fetch_stock_realtime_price(ticker: str) -> StockRealtimePrice:
    """
    Fetch real-time stock price data from Yahoo Finance API.
    
    This function retrieves current price information for a specified stock ticker
    from Yahoo Finance's API using the yfinance library.
    
    Usage scenarios:
    - When users ask about "current price", "today's price", "current value"
    - When users want to know intraday movements like "opening price", "highest", "lowest"
    - Examples: "What's FPT's price today?", "What's VNM going for?", "Check Apple's price"
    
    Limitations:
    - This tool does NOT fetch historical data (e.g., last week's price)
    - This tool does NOT fetch news or financial reports
    
    Args:
        ticker (str): Stock ticker symbol to fetch data for
        
    Returns:
        StockRealtimePrice: Contains real-time price data or error information
    """
    current_ts = int(datetime.now(timezone.utc).timestamp())
    try:
        # fast_info is a good choice for performance
        info = yf.Ticker(ticker).fast_info
        
        # Check if price data is available
        if not info or info.last_price is None:
            return StockRealtimePrice(
                ticker=ticker,
                ts=current_ts,
                error=f"No real-time trading data found for ticker '{ticker}'."
            )

        return StockRealtimePrice(
            ticker=ticker,
            ts=current_ts,
            open=info.open,
            day_high=info.day_high,
            day_low=info.day_low,
            last_price=info.last_price,
            last_volume=info.last_volume
        )
    except Exception as e:
        # Catch other errors (e.g., network, non-existent ticker)
        return StockRealtimePrice(
            ticker=ticker,
            ts=current_ts,
            error=f"An error occurred while querying data for ticker {ticker}: {e}"
        )