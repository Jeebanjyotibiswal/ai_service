from fastapi import FastAPI
from pydantic import BaseModel
class ChatRequest(BaseModel):
    message: str
app = FastAPI()


from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables (useful for local development)
load_dotenv()

# Debug tip requested by the user
print("KEY CHECK:", os.getenv("GROQ_API_KEY"))

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("Warning: GROQ_API_KEY not found in environment.")

client = Groq(api_key=api_key)

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

@app.post("/chat")
def chat(request: ChatRequest):
    response = generate_response(request.message)
    return {"reply": response}