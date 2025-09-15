from .stock import get_stock_realtime_price
from .itapia import get_itapia_quick_analysis

def get_all_tools():
    """
    Returns a list of all available tools for the financial agent.
    
    The agent can use these tools to gather information and perform actions
    based on user requests. Each tool is a function decorated with @tool
    that has a description explaining when and how to use it.
    
    Returns:
        list: A list of tool functions available to the agent
    """
    return [get_stock_realtime_price, get_itapia_quick_analysis]