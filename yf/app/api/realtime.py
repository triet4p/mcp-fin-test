from fastapi import APIRouter
from app.schemas import StockRealtimePrice
from app.tools.fetch_realtime_stock import fetch_stock_realtime_price

router = APIRouter()

@router.get('/market/tickers/{ticker}/price/realtime', 
            response_model=StockRealtimePrice)
def get_stock_realtie_price(ticker: str) -> StockRealtimePrice:
    return fetch_stock_realtime_price(ticker)