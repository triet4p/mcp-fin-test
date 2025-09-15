import yfinance as yf
from langchain_core.tools import tool
from datetime import datetime, timezone

from .schemas import StockRealtimePrice, StockTickerInput

@tool(args_schema=StockTickerInput)
def get_stock_realtime_price(ticker: str) -> StockRealtimePrice:
    """
    Lấy dữ liệu giá cổ phiếu theo thời gian thực (real-time) từ API của Yahoo Finance

    **Khi nào sử dụng:**
    - Khi người dùng hỏi về "giá hiện tại", "giá hôm nay", "giá bây giờ".
    - Khi người dùng muốn biết biến động trong ngày như giá "mở cửa", "cao nhất", "thấp nhất".
    - Ví dụ: "giá FPT hôm nay?", "VNM đang là bao nhiêu?", "xem giá Apple".

    **Giới hạn:**
    - Công cụ này KHÔNG lấy dữ liệu lịch sử (ví dụ: giá của tuần trước).
    - Công cụ này KHÔNG lấy tin tức hoặc báo cáo tài chính.
    """
    current_ts = int(datetime.now(timezone.utc).timestamp())
    try:
        # fast_info là lựa chọn tốt cho hiệu năng
        info = yf.Ticker(ticker).fast_info
        
        # Kiểm tra xem có dữ liệu giá không
        if not info or info.last_price is None:
            return StockRealtimePrice(
                ticker=ticker,
                ts=current_ts,
                error=f"Không tìm thấy dữ liệu giao dịch real-time cho mã '{ticker}'."
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
        # Bắt các lỗi khác (ví dụ: mạng, ticker không tồn tại)
        return StockRealtimePrice(
            ticker=ticker,
            ts=current_ts,
            error=f"Đã xảy ra lỗi khi truy vấn dữ liệu cho mã {ticker}: {e}"
        )