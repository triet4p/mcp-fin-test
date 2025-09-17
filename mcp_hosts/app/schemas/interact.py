from pydantic import BaseModel

class InteractionRequest(BaseModel):
    session_id: str
    message: str

class InteractionResponse(BaseModel):
    response: str