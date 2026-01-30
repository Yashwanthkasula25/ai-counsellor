# backend/check_models.py
import google.generativeai as genai
import os

# 👇 PASTE YOUR KEY HERE
os.environ["GOOGLE_API_KEY"] = "AIzaSyAQ-NHr9DIWOf5uPkqrtdsR2vw36nG8TlA" 

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

print("🔍 Checking available models for your API key...")

try:
    count = 0
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ FOUND: {m.name}")
            count += 1
    
    if count == 0:
        print("❌ No models found. Check your API Key or Region availability.")
    else:
        print(f"\n✨ Success! Found {count} usable models.")

except Exception as e:
    print(f"\n❌ CRITICAL ERROR: {e}")