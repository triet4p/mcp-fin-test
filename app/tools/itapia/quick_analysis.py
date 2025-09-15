from typing import Literal
import requests
from langchain_core.tools import tool

from app.core.config import ITAPIA_API_BASE_URL

from .schemas import QuickCheckReportResponse

@tool
def get_itapia_quick_analysis(ticker: str,
                              daily_analysis_type: Literal['short', 'medium', 'long'] = 'medium',
                              required_type: Literal['daily', 'intraday', 'all'] = 'all') -> QuickCheckReportResponse:
    """
    Gọi tới ứng dụng ITAPIA để lấy một báo cáo phân tích nhanh toàn cảnh. Báo cáo thường được dùng để có cái nhìn đa chiều về:
    - Technical Analysis: Góc nhìn kỹ thuật, bao gồm các chỉ số (indicators) được tính thêm như RSI, SMA, etc. Nó cũng bao gồm các pattern phân tích
        được, bao gồm cả các chart patterns và candlestick patterns.
    - News analysis: Góc nhìn tin tức. Nó sẽ phân tích các tin tức (Sentiment, NER, Impact, ...) và trả về các kết quả về độ quan trọng.
    - Forecasting: Góc nhìn tương lai. Sử dụng một mô hình ML đơn giản để có các forecast về tương lai, bao gồm:
        - Triple Barrier: Dự đoán có chạm ngưỡng Take Profit (TP), Stop Loss (SL) hay ko bị gì sau 1 duration days. -1, 0, 1 lần lượt nghĩa là
            chạm SL, ko chạm gì, chạm TP
        - N-days distribution (5-day và 20-day): Dự đoán phân phối giá trong n ngày tới. Hiện cung cấp 5 ngày cho ngắn hạn và 20 ngày cho trung/dài hạn.
    
    **Các tham số điều chỉnh**:
    - ticker: Mã cổ phiếu
    - daily_analysis_type ('short', 'medium', 'long'): Kiểu phân tích hướng tới.
    - required_type ('daily', 'intraday', 'all'): Loại báo cáo muốn trả về
    
    **Nên dùng khi**:
    - Người dùng muốn có 1 góc nhìn đa chiều về cả lịch sử, hiện tại và tương lai, trên nhiều khía cạnh như chỉ báo, dự đoán, tin tức.
    - Người dùng muốn có 1 vài chỉ số, dự đoán nào đó có trong liệt kê trên.
    
    **Chú ý**:
    - ITAPIA có thể chưa cập nhật giá realtime mới nhất. Hãy sử dụng tool khác để lấy giá realtime khi cần thiết.
    """
    try:
        url = f'{ITAPIA_API_BASE_URL}/analysis/quick/{ticker}/full'
        response = requests.get(url=url, params={
            'daily_analysis_type': daily_analysis_type if daily_analysis_type in ['short', 'medium', 'long'] else 'medium',
            'required_type': required_type if required_type in ['daily', 'intraday', 'all'] else 'all'
        })
        
        response.raise_for_status()
        return QuickCheckReportResponse.model_validate(response.json())
    except requests.exceptions.HTTPError as e:
        return {'error': f'An error occured: {str(e)}'}