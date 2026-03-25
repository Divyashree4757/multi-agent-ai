from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from pydantic import BaseModel
from .agents.orchestrator import orchestrate
from .agents.suggester_agent import auto_suggest_tasks
from .agents.predictor_agent import predict_day
from .agents.mood_agent import detect_mood
from .agents.summary_agent import generate_weekly_summary
from .agents.priority_agent import rank_tasks_by_priority
from .agents.goal_agent import coach_user, brainstorm
from .agents.alert_agent import check_risks, generate_daily_report
from .tools.analytics_tools import get_analytics
from .tools.voice_tools import transcribe_audio
from .tools.memory_tools import save_memory, get_recent_memory, clear_memory
from .db.database import init_db
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Multi Agent AI System", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
def startup():
    init_db()
    print("✅ Database initialized")
    print("✅ All agents ready")
    print("✅ Server started")

class ChatRequest(BaseModel):
    message: str

class GoalRequest(BaseModel):
    goal: str

class BrainstormRequest(BaseModel):
    topic: str

@app.get("/", response_class=HTMLResponse)
def root():
    with open("app/templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    save_memory("user", req.message)
    result = orchestrate(req.message)
    save_memory("assistant", result.get("response", ""), result.get("intent", ""))
    return result

@app.get("/analytics")
def analytics():
    return get_analytics()

@app.get("/suggest")
def suggest():
    return auto_suggest_tasks()

@app.get("/predict")
def predict():
    return predict_day()

@app.get("/mood")
def mood():
    return detect_mood()

@app.get("/summary")
def summary():
    return generate_weekly_summary()

@app.get("/priority")
def priority():
    return rank_tasks_by_priority()

@app.post("/goal")
def goal(req: GoalRequest):
    return coach_user(req.goal)

@app.post("/brainstorm")
def brainstorm_ideas(req: BrainstormRequest):
    return brainstorm(req.topic)

@app.get("/risks")
def risks():
    return check_risks()

@app.get("/report")
def report():
    return generate_daily_report()

@app.post("/voice")
async def voice(file: UploadFile = File(...)):
    audio_bytes = await file.read()
    text = transcribe_audio(audio_bytes, file.filename)
    return {"text": text}

@app.get("/memory")
def memory():
    return get_recent_memory()

@app.delete("/memory")
def delete_memory():
    return clear_memory()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "3.0.0",
        "features": [
            "tasks", "calendar", "notes",
            "memory", "analytics", "suggestions",
            "voice", "mood", "prediction",
            "summary", "priority", "goals",
            "brainstorm", "risks", "report"
        ]
    }
