from pydantic import BaseModel, Field
from typing import Optional

# Schema cho output của tool, bao gồm cả trường hợp lỗi
class StockRealtimePrice(BaseModel):
    ticker: str = Field(..., description="Mã symbol của ticker")
    open: Optional[float] = Field(None, description='Giá mở cửa hôm nay')
    day_high: Optional[float] = Field(None, description="Giá cao nhất trong ngày")
    day_low: Optional[float] = Field(None, description="Giá thấp nhất trong ngày")
    last_price: Optional[float] = Field(None, description="Giá tại thời điểm gọi API")
    last_volume: Optional[float] = Field(None, description="Khối lượng giao dịch tại thời điểm gọi API")
    ts: int = Field(..., description="Timestamp lúc mà trả kết quả")
    error: Optional[str] = Field(None, description="Thông báo lỗi nếu không lấy được dữ liệu")

# Schema cho input của tool
class StockTickerInput(BaseModel):
    ticker: str = Field(description="Mã cổ phiếu cần tra cứu, ví dụ: 'FPT', 'AAPL'")
    
