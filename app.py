from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

class ChatRequest(BaseModel):
    message: str

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for better security in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key check
api_key = os.getenv("GROQ_API_KEY")

def generate_response(message: str) -> str:
    if not api_key:
        return "Error: GROQ_API_KEY is not set in Render environment variables."
        
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": message}
            ],
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Groq Error: {str(e)}")
        return f"Error: {str(e)}"

@app.post("/chat")
async def chat(request: ChatRequest):
    response = generate_response(request.message)
    return {"reply": response}

@app.get("/health")
def health_check():
    return {"status": "ok", "api_key_set": api_key is not None}