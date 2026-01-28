# backend/schemas.py
from pydantic import BaseModel
from typing import Optional, Any

# What the frontend sends to us
class ChatRequest(BaseModel):
    user_id: int = 1  # Default to 1 for now
    message: str

# What we send back to the frontend
class ChatResponse(BaseModel):
    response: str
    action_taken: Optional[dict] = None  # If AI shortlists a uni, this has data