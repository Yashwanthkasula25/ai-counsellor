import os
import json
from openai import OpenAI
from sqlalchemy.orm import Session
from app.db.models import User, University, UserShortlist 

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. Define the Tool (Function Definition)
tools = [
    {
        "type": "function",
        "function": {
            "name": "shortlist_university",
            "description": "Add a university to the user's shortlist when it fits their profile.",
            "parameters": {
                "type": "object",
                "properties": {
                    "university_name": {"type": "string"},
                    "category": {"type": "string", "enum": ["DREAM", "TARGET", "SAFE"]},
                    "reasoning": {"type": "string", "description": "Why this university fits the user."}
                },
                "required": ["university_name", "category", "reasoning"]
            }
        }
    }
]

def run_counsellor_agent(user_id: int, user_message: str, db: Session):
    # Fetch user context
    user = db.query(User).filter(User.id == user_id).first()
    
    # System Prompt: Enforce the persona
    system_prompt = f"""
    You are an expert Study Abroad Counsellor. 
    User Profile: {user.profile_summary}
    Current Stage: {user.current_stage}
    
    Your Goal: Guide them. If they ask for recommendations, analyze their profile.
    If you find a good university, DO NOT just talk about it. USE the 'shortlist_university' tool to save it.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    # 2. Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=messages,
        tools=tools,
        tool_choice="auto" 
    )

    response_message = response.choices[0].message

    # 3. Check if AI wants to run a function (Take Action)
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "shortlist_university":
                # Parse arguments from AI
                args = json.loads(tool_call.function.arguments)
                
                # --- ACTUAL DATABASE INSERTION ---
                # Find university ID by name (simplified logic)
                uni = db.query(University).filter(University.name.ilike(f"%{args['university_name']}%")).first()
                if uni:
                    new_shortlist = UserShortlist(
                        user_id=user.id,
                        university_id=uni.id,
                        category=args['category'],
                        ai_reasoning=args['reasoning']
                    )
                    db.add(new_shortlist)
                    db.commit()
                    return {
                        "type": "action",
                        "content": f"✅ I've added **{uni.name}** to your {args['category']} list.",
                        "data": args
                    }
                else:
                    return {"type": "error", "content": "I couldn't find that university in our database."}

    # If no action, just return the chat reply
    return {"type": "chat", "content": response_message.content}