import os
import json
import google.generativeai as genai
from sqlalchemy.orm import Session
from models import University, UserShortlist, User

# 👇 KEEP YOUR API KEY
os.environ["GOOGLE_API_KEY"] = "AIzaSyAQ-NHr9DIWOf5uPkqrtdsR2vw36nG8TlA" 
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- 1. TOOL: Shortlist University ---
def shortlist_university(user_id: int, university_name: str, category: str, reasoning: str, db: Session):
    # 1. Try Exact Match first
    uni = db.query(University).filter(University.name.ilike(f"{university_name}")).first()
    
    # 2. If not found, try Partial Match (e.g., "Stanford" matches "Stanford University")
    if not uni:
        uni = db.query(University).filter(University.name.ilike(f"%{university_name}%")).first()

    if uni:
        existing = db.query(UserShortlist).filter_by(user_id=user_id, university_id=uni.id).first()
        if existing:
            return f"INFO: {uni.name} is already in your {existing.category} list."

        new_item = UserShortlist(
            user_id=user_id,
            university_id=uni.id,
            category=category.upper(),
            ai_reasoning=reasoning
        )
        db.add(new_item)
        db.commit()
        return f"SUCCESS: Added {uni.name} to {category} list."
    else:
        return f"ERROR: Could not find '{university_name}' in database. (Try: MIT, Stanford, University of Toronto)"

# --- 2. MAIN AGENT LOGIC ---
def get_ai_response(user_id: int, user_message: str, db: Session):
    try:
        user = db.query(User).filter(User.id == user_id).first()
        
        current_stage = user.current_stage if user else "ONBOARDING"
        profile_data = user.profile_summary if user and user.profile_summary else {}

        # --- SELECT PERSONA ---
        if current_stage == "ONBOARDING":
            system_instruction = f"""
            You are a strict Study Abroad Counsellor. The user is in the ONBOARDING stage.
            YOUR GOAL: Gather their GPA, Major, Budget, and Target Country.
            CRITICAL RULE: You can NOT shortlist universities yet. 
            If the user asks to add/shortlist a university, politely REFUSE. 
            Say: "I can't shortlist universities yet. We need to complete your profile first."
            Current Profile Data: {profile_data}
            """
            tools_enabled = False

        elif current_stage == "SHORTLISTING":
            # 👇 UPDATED PROMPT: Explicit JSON Format Definition
            system_instruction = f"""
            You are a Study Abroad Counsellor. The user is in the SHORTLISTING stage.
            YOUR GOAL: Recommend and Shortlist universities.
            
            DATABASE RULES:
            Use these exact names: "MIT", "Stanford", "Technical University of Munich", "University of Toronto".
            
            REQUIRED OUTPUT FORMAT:
            If the user wants to shortlist a university, you MUST output this EXACT JSON structure:
            {{
                "tool_use": "shortlist_university",
                "university_name": "Stanford",
                "category": "DREAM", 
                "reasoning": "Strong match for your GPA."
            }}
            
            Current Profile Data: {profile_data}
            """
            tools_enabled = True

        elif current_stage == "APPLICATION":
             system_instruction = "You are an Application Guide. Help with SOPs and Deadlines."
             tools_enabled = False

        else:
            system_instruction = "You are a helpful assistant."
            tools_enabled = False

        # --- CALL GEMINI ---
        model = genai.GenerativeModel('gemini-flash-latest')
        full_prompt = f"{system_instruction}\n\nUser: {user_message}"
        response = model.generate_content(full_prompt)
        text_response = response.text
        
        # --- HANDLE TOOLS ---
        # We look for the "tool_use" key we defined in the prompt above
        if tools_enabled and '"tool_use": "shortlist_university"' in text_response:
            try:
                # Clean JSON
                clean_json = text_response.replace("```json", "").replace("```", "").strip()
                start = clean_json.find("{")
                end = clean_json.rfind("}") + 1
                json_str = clean_json[start:end]
                
                data = json.loads(json_str)
                
                # Extract Data safely
                uni_name = data.get('university_name', 'Unknown')
                category = data.get('category', 'TARGET')
                reasoning = data.get('reasoning', 'AI Recommendation')
                
                result_msg = shortlist_university(user_id, uni_name, category, reasoning, db)
                
                return {
                    "response": f"✅ {result_msg}",
                    "action_taken": data
                }

            except Exception as e:
                return {"response": f"System Error during shortlisting: {str(e)}"}

        return {"response": text_response}

    except Exception as e:
        return {"response": f"⚠️ CRITICAL AI ERROR: {str(e)}"}