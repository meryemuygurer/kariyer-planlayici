from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserData(BaseModel):
    interests: list[str]
    skills: list[str]
    goal: str

@app.post("/recommend")
def recommend(user: UserData):
    if "Web" in user.interests and "JavaScript" in user.skills:
        career = "Frontend Developer"
        learning_path = ["HTML/CSS", "JavaScript", "React", "Next.js"]
    elif "Data" in user.interests and "Python" in user.skills:
        career = "Data Analyst"
        learning_path = ["Python", "Pandas", "SQL", "Tableau"]
    else:
        career = "Genel Yazılım Geliştirici"
        learning_path = ["Python", "Git", "Veritabanları", "API geliştirme"]

    return {
        "career": career,
        "learning_path": learning_path
    }
