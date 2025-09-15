from .stock import get_stock_realtime_price
from .itapia import get_itapia_quick_analysis

def get_all_tools():
    return [get_stock_realtime_price, get_itapia_quick_analysis]