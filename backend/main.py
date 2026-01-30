# main.py
# FastAPI backend for AI-powered Career Recommendation
# Written as a student / junior-level backend project 🙂

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import json
import os

app = FastAPI()

# Allow requests from React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client (API key is read from environment variable)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class UserData(BaseModel):
    interests: list[str]
    skills: list[str]
    goal: str


def get_ai_recommendation(user_data: UserData):
    """
    I send user interests, skills and goal to the AI
    and expect a structured JSON response.
    """

    prompt = f"""
    You are a career advisor.

    User interests: {user_data.interests}
    User skills: {user_data.skills}
    Career goal: {user_data.goal}

    Suggest:
    - ONE suitable career
    - A short learning path (3–5 steps)

    Respond ONLY in valid JSON format like:
    {{
      "career": "...",
      "learning_path": ["step 1", "step 2", "step 3"]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        content = response.choices[0].message.content
        return json.loads(content)

    except Exception as e:
        print("AI error:", e)
        return {
            "career": "General Software Developer",
            "learning_path": [
                "Learn Python basics",
                "Understand Git and GitHub",
                "Build small projects",
                "Learn basic APIs"
            ]
        }


@app.post("/recommend-ai")
def recommend_ai(user: UserData):
    return get_ai_recommendation(user)
