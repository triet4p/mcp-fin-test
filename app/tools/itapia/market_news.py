from typing import Literal
import requests
from langchain_core.tools import tool

from app.core.config import ITAPIA_API_BASE_URL

from .schemas import RelevantNewsResponse, UniversalNewsResponse

@tool
def get_itapia_relevant_news(ticker: str, limit: int = 10) -> RelevantNewsResponse:
    """
    Gọi tới ứng dụng ITAPIA để lấy các tin tức liên quan trực tiếp tới một mã cổ phiếu
    
    **Các tham số điều chỉnh**:
    - ticker: Mã cổ phiếu
    - limit: Số lượng tin tức nhiều nhất được lấy (các tin tức được xếp theo thứ tự thời gian từ gần đây tới xa hơn). Mặc định là 10.
    
    **Nên dùng khi**:
    - Người dùng muốn có chính xác các tin tức xảy ra trong các ngày gần đây liên quan tới cổ phiếu mà họ muốn tìm hiểu
    
    **Chú ý**:
    - Khi API này ko trả về nhiều tin tức liên quan, có thể gọi tới API trả về các tin tức toàn cục (liên quan tới thế giới, ngành, ...)
    """
    try:
        url = f'{ITAPIA_API_BASE_URL}/market/tickers/{ticker}/news'
        response = requests.get(url=url, params={
            'skip': 0,
            'limit': limit,
        })
        
        response.raise_for_status()
        return RelevantNewsResponse.model_validate(response.json())
    except requests.exceptions.HTTPError as e:
        return {'error': f'An error occured: {str(e)}'}
    
@tool
def get_itapia_universal_news(search_terms: str, limit: int = 10) -> UniversalNewsResponse:
    """
    Gọi tới ứng dụng ITAPIA để lấy các tin tức toàn cục (liên quan tới thế giới, quốc gia, các ngành,...)
    
    **Các tham số điều chỉnh**:
    - search_terms: Từ khóa để search. Có thể search nhiều từ khóa cùng lúc, cách nhau bởi dấu cách. Lúc đó
        nó sẽ trả về các tin tức mà cả 2 từ khóa đó xuất hiện.
        Ví dụ `search_terms=US%20forecast` thì sẽ tìm các bài mà cả US và forecast đều xuất hiện
        
        *Các từ khóa* thường xuất hiện:
        US, Federal, policy, forecast, S&P, report, reserve, world, nation, business
        các nhóm ngành như technology, utility (util), finance, politics, energy, economy,... 
        
        
    - limit: Số lượng tin tức nhiều nhất được lấy (các tin tức được xếp theo thứ tự thời gian từ gần đây tới xa hơn). Mặc định là 10.
    
    **Nên dùng khi**:
    - Người dùng muốn có thêm các tin tức liên quan gián tiếp tới cổ phiếu mà họ muốn tìm hiểu, qua các từ khóa
    
    **Chú ý**:
    - API này là một bổ sung khá mạnh cho API lấy relevant news
    """
    try:
        url = f'{ITAPIA_API_BASE_URL}/market/news/universal'
        response = requests.get(url=url, params={
            'search_terms': search_terms,
            'skip': 0,
            'limit': limit,
        })
        
        response.raise_for_status()
        return UniversalNewsResponse.model_validate(response.json())
    except requests.exceptions.HTTPError as e:
        return {'error': f'An error occured: {str(e)}'}
    
