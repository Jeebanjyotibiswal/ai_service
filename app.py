from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables (Render automatically deta hai, local ke liye fallback)
if not os.getenv("GROQ_API_KEY"):
    load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found!")

client = Groq(api_key=api_key)

app = FastAPI()

# Request schema
class ChatRequest(BaseModel):
    message: str

# AI response function
def generate_response(message: str) -> str:
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# API route
@app.post("/chat")
def chat(request: ChatRequest):
    response = generate_response(request.message)
    return {"reply": response}