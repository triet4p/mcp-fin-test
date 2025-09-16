from typing import Literal
import requests
from langchain_core.tools import tool

from app.core.config import ITAPIA_API_BASE_URL

from .schemas import AdvisorResponse, QuantitivePreferencesConfigRequest

@tool
def get_itapia_quick_advisor(quantitive_config: QuantitivePreferencesConfigRequest,
                              ticker: str,
                              limit: int) -> AdvisorResponse:
    """
    Gọi tới ứng dụng ITAPIA để lấy một advisor dựa trên báo cáo phân tích toàn cảnh của chính ITAPIA và áp dụng các luật có sẵn trong ITAPIA
    
    **Các tham số điều chỉnh**:
    - ticker: Mã cổ phiếu
    - limit: Số lượng rule được áp dụng để bỏ phiếu cho 1 quyết định.
    - quantitive_config: Đây là config cá nhân hóa bên phía người dùng. Nó được sử dụng để tìm kiếm các action khác nhau với cùng 1 report, khi khẩu vị người dùng khác nhau. Nó bao gồm:
        - weights: Trọng số của các metrics để tính toán điểm số. Ví dụ `cagr` có trọng số cao thì sẽ ưu tiên tìm các rules thuộc cagr. Có thể set trọng số trên nhiều metric. Lúc đó nó sẽ cố gắng tìm các rule thỏa mãn nhiều mục tiêu.
        - constraints: Các ràng buộc cứng, mỗi cái là một cặp (min, max), biểu thị ví dụ constraints['cagr'] = (0.01, None) thì chỉ lấy các rule có 0.01 < rule < inf.
        - modifiers: Bộ điều chỉnh action cuối cùng. Nó dùng các field của nó để tác động vào các mức như Position Size Percent hay Take profite, Stop Loss rate của action.
    
    **Nên dùng khi**:
    - Người dùng muốn có 1 lời khuyên về việc đầu tư.
    - Người dùng muốn xem là với các thông tin hiện tại, liệu khi thay đổi các khẩu vị, tính cách (như tính chấp nhận rủi ro, ...) thì action và recommend được khuyên sẽ thay đổi thế nào.
      Nghĩa là họ muốn thử nghiệm nhiều trường hợp.
    
    **Chú ý**:
    - Bạn nên cho weights khác 0 trong ít nhất 5 metrics và gán constraints (min hoặc max khác none) cho ít nhất 4 metrics. Constraints ko nên quá hard, nếu ko sẽ có ít rule được áp dụng. 
      Tôi sẽ cung cấp 1 metrics hiện tại được coi là rất tốt để bạn tham khảo và ko đặt quá nhiều kì vọng:
      {"cagr": 0.008, "num_trades": 10, "sharpe_ratio": 0.99083288151707, "win_rate_pct": 0.5294783194452999, "profit_factor": 1.3026362902976416, "sortino_ratio": 0.27143086787988063, "max_drawdown_pct": 0.15714378223655628, "total_return_pct": 0.04950513606408939, "annual_return_stability": 0.07358453383782033}
    - Advisor trả về sẽ ko chứa báo cáo phân tích
    - Tools này có 1 phần ban đầu sẽ gọi phân tích nhanh (quick analysis) tại chính ITAPIA, bạn ko phải gọi tools lấy report trước khi gọi tool này.
      Nhưng nếu bạn cần 1 báo cáo tách biệt với lời khuyên thì vẫn phải gọi cả 2 tool
    """
    try:
        url = f'{ITAPIA_API_BASE_URL}/advisor/quick/{ticker}/full'
        response = requests.post(url=url, params={
            'limit': limit
        }, json=quantitive_config.model_dump())
        
        response.raise_for_status()
        return AdvisorResponse.model_validate(response.json())
    except requests.exceptions.HTTPError as e:
        return {'error': f'An error occured: {str(e)}'}