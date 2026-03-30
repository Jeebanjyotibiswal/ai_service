from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from groq import Groq

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    response = generate_response(message)
    return jsonify({"reply": response})

@app.route("/predict", methods=["POST"])
def predict():
    # Placeholder for ML prediction logic as per user instructions
    data = request.get_json()
    message = data.get("message", "")
    response = generate_response(message)
    return jsonify({"reply": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)