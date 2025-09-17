from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from app.dependencies import get_tools as get_tools_dp

router = APIRouter()

@router.get("/tools", 
         summary="Get All Tool Specifications",
         response_model=List[Dict[str, Any]])
def get_tools():
    """
    Cung cấp danh sách tất cả các 'Tool Specification' có sẵn.
    Agent Host sẽ gọi endpoint này khi khởi động để khám phá các năng lực.
    """
    tools = get_tools_dp()
    
    if not tools:
        raise HTTPException(
            status_code=503, 
            detail="Tool configurations are currently unavailable or invalid."
        )
        
    return tools