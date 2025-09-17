"""
Pydantic schemas for the Yahoo Finance service.

This module defines the data models used for validating and serializing
real-time stock price data.
"""
from pydantic import BaseModel, Field
from typing import Optional

class StockRealtimePrice(BaseModel):
    """
    Schema for real-time stock price data.
    
    This schema includes both successful responses with price data
    and error responses when data cannot be retrieved.
    """
    ticker: str = Field(..., description="Stock ticker symbol")
    open: Optional[float] = Field(None, description='Today\'s opening price')
    day_high: Optional[float] = Field(None, description="Highest price of the day")
    day_low: Optional[float] = Field(None, description="Lowest price of the day")
    last_price: Optional[float] = Field(None, description="Price at the time of API call")
    last_volume: Optional[float] = Field(None, description="Trading volume at the time of API call")
    ts: int = Field(..., description="Timestamp when the response was generated")
    error: Optional[str] = Field(None, description="Error message if data could not be retrieved")
