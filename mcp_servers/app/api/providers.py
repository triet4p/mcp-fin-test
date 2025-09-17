from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from app.dependencies import get_providers as get_providers_dp

router = APIRouter()

@router.get("/providers", 
         summary="Get All Provider Configurations",
         response_model=List[Dict[str, str]])
def get_providers():
    """
    Cung cấp danh sách tất cả các 'Tool Specification' có sẵn.
    Agent Host sẽ gọi endpoint này khi khởi động để khám phá các năng lực.
    """
    providers = get_providers_dp()
    
    if not providers:
        raise HTTPException(
            status_code=503, 
            detail="Tool configurations are currently unavailable or invalid."
        )
        
    return providers