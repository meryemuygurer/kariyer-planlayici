# main.py
# FastAPI backend for Career Path Recommendation

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from pathlib import Path

app = FastAPI()

# ===== CORS Setup =====
# frontend and backend need CORS to talk to each other
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend is running here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== User Data Model =====
# Using Pydantic for input validation, still learning this
class UserData(BaseModel):
    interests: list[str]
    skills: list[str]
    goal: str

# ===== Load Careers Dataset =====
# I created a JSON file with some basic career info
DATA_PATH = Path(__file__).parent / "data" / "careers.json"
with open(DATA_PATH, "r") as f:
    careers_data = json.load(f)

# ===== Recommend Endpoint =====
@app.post("/recommend")
def recommend(user: UserData):
    # Simple matching logic: I know it's basic but works for now :)
    for career_entry in careers_data:
        if any(interest in career_entry["interests"] for interest in user.interests) and \
           any(skill in career_entry["skills"] for skill in user.skills):
            return {
                "career": career_entry["career"],
                "learning_path": career_entry["learning_path"]
            }
    
    # Default suggestion if no match is found
    # I will improve this later with AI or more rules
    return {
        "career": "General Software Developer",
        "learning_path": ["Python", "Git", "Databases", "API Development"]
    }
