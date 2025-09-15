from fastapi import APIRouter
from app.agent import get_agent_response
from app.schemas.interact import InteractionRequest, InteractionResponse

router = APIRouter()

@router.post('/interact', response_model=InteractionResponse)
def interact(request: InteractionRequest):
    result = get_agent_response(
        session_id=request.session_id,
        user_message=request.message
    )
    return InteractionResponse.model_validate(result)