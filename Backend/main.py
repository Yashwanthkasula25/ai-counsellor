from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db, engine, Base
from models import User
from schemas import ChatRequest, ChatResponse
from agent import get_ai_response
from models import UserShortlist

# Create Tables automatically (optional, but good for safety)
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Allow Frontend to talk to Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AI Counsellor API is running!"}

# --- STAGE MANAGEMENT ENDPOINTS ---

@app.get("/user/{user_id}/stage")
def get_user_stage(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        # Create a default user if none exists (Auto-fix for testing)
        new_user = User(id=user_id, email=f"test{user_id}@example.com", current_stage="ONBOARDING")
        db.add(new_user)
        db.commit()
        return {"stage": "ONBOARDING"}
    
    return {"stage": user.current_stage}

@app.post("/user/{user_id}/advance_stage")
def advance_user_stage(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.current_stage == "ONBOARDING":
        user.current_stage = "SHORTLISTING"
    elif user.current_stage == "SHORTLISTING":
        user.current_stage = "APPLICATION"
        
    db.commit()
    return {"status": "success", "new_stage": user.current_stage}

# --- CHAT ENDPOINT (The Critical Fix) ---

@app.post("/chat", response_model=ChatResponse)
def chat_with_counsellor(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # 👇 CRITICAL FIX: Passing 3 arguments now!
        result = get_ai_response(request.user_id, request.message, db)
        return result
    except Exception as e:
        # Print the error to the terminal so we can see it!
        print(f"❌ SERVER ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{user_id}/shortlist")
def get_user_shortlist(user_id: int, db: Session = Depends(get_db)):
    items = db.query(UserShortlist).filter(UserShortlist.user_id == user_id).all()
    return [
        {
            "id": item.id,
            "university": item.university.name,
            "category": item.category,
            "is_locked": item.is_locked
        }
        for item in items
    ]

# 2. LOCK A UNIVERSITY (Triggers Stage 3)
@app.post("/user/{user_id}/lock/{shortlist_id}")
def lock_university(user_id: int, shortlist_id: int, db: Session = Depends(get_db)):
    # 1. Lock the specific university
    item = db.query(UserShortlist).filter(UserShortlist.id == shortlist_id, UserShortlist.user_id == user_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.is_locked = True
    
    # 2. Advance User to Stage 3 (APPLICATION)
    user = db.query(User).filter(User.id == user_id).first()
    user.current_stage = "APPLICATION"
    
    db.commit()
    return {"status": "success", "locked_uni": item.university.name}        


# backend/main.py

@app.post("/user/{user_id}/advance_stage")
def advance_user_stage(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # State Machine Logic
    if user.current_stage == "ONBOARDING":
        user.current_stage = "SHORTLISTING"
    elif user.current_stage == "SHORTLISTING":
        user.current_stage = "APPLICATION"
    elif user.current_stage == "APPLICATION":
        # 👇 NEW: The Final Victory Stage
        user.current_stage = "ADMITTED" 
        
    db.commit()
    return {"status": "success", "new_stage": user.current_stage}    