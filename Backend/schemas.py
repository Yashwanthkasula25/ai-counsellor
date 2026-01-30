from pydantic import BaseModel
from typing import Optional, Any

# Frontend sends this to Backend
class ChatRequest(BaseModel):
    user_id: int = 1  # Default to 1 if not sent
    message: str

# Backend sends this to Frontend
class ChatResponse(BaseModel):
    response: str
    action_taken: Optional[dict] = None