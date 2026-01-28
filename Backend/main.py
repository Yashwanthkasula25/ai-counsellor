# backend/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from schemas import ChatRequest, ChatResponse # 👈 Import new schemas
from agent import get_ai_response        # 👈 Import AI logic

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "AI Counsellor API is running!"}

@app.get("/universities")
def get_universities(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM universities"))
    # Convert rows to dicts
    return [{"id": row.id, "name": row.name, "country": row.country} for row in result.fetchall()]

# 👇 NEW CHAT ENDPOINT 👇
@app.post("/chat", response_model=ChatResponse)
def chat_with_counsellor(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Pass the message to our AI Agent
        result = get_ai_response(request.message, db)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))