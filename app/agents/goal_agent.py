from groq import Groq
from ..tools.task_tools import list_tasks
from ..tools.memory_tools import get_memory_context
import os, json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def coach_user(goal: str) -> dict:
    tasks = list_tasks()
    memory = get_memory_context()

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an AI life coach helping users achieve their goals.
Respond ONLY in this JSON format:
{
  "goal_analysis": "analysis of the goal in one sentence",
  "feasibility": "HIGH|MEDIUM|LOW",
  "milestones": [
    {"step": 1, "title": "milestone title", "timeframe": "Day 1-3"},
    {"step": 2, "title": "milestone title", "timeframe": "Day 4-7"},
    {"step": 3, "title": "milestone title", "timeframe": "Week 2"}
  ],
  "action_tasks": ["task 1", "task 2", "task 3"],
  "potential_blockers": ["blocker 1", "blocker 2"],
  "success_probability": 75,
  "coach_message": "motivating personal message from coach",
  "first_step": "the very first thing to do RIGHT NOW"
}"""
            },
            {
                "role": "user",
                "content": f"My goal: {goal}\nMy current tasks: {tasks}\nContext: {memory}"
            }
        ],
        max_tokens=500
    )

    raw = response.choices[0].message.content.strip()
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except:
        return {
            "goal_analysis": f"Working towards: {goal}",
            "feasibility": "HIGH",
            "milestones": [{"step": 1, "title": "Get started", "timeframe": "Today"}],
            "action_tasks": [f"Start working on {goal}"],
            "potential_blockers": [],
            "success_probability": 80,
            "coach_message": "You've got this! Take it one step at a time.",
            "first_step": f"Begin with the first part of {goal}"
        }

def brainstorm(topic: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a creative AI brainstorming partner.
Respond ONLY in this JSON format:
{
  "ideas": [
    {"title": "idea title", "description": "brief description", "difficulty": "Easy|Medium|Hard", "impact": "HIGH|MEDIUM|LOW"},
    {"title": "idea title", "description": "brief description", "difficulty": "Easy|Medium|Hard", "impact": "HIGH|MEDIUM|LOW"},
    {"title": "idea title", "description": "brief description", "difficulty": "Easy|Medium|Hard", "impact": "HIGH|MEDIUM|LOW"},
    {"title": "idea title", "description": "brief description", "difficulty": "Easy|Medium|Hard", "impact": "HIGH|MEDIUM|LOW"},
    {"title": "idea title", "description": "brief description", "difficulty": "Easy|Medium|Hard", "impact": "HIGH|MEDIUM|LOW"}
  ],
  "best_idea": "title of the best idea",
  "quick_win": "easiest idea to implement right now",
  "creative_insight": "one unexpected creative angle on this topic"
}"""
            },
            {
                "role": "user",
                "content": f"Brainstorm ideas for: {topic}"
            }
        ],
        max_tokens=500
    )

    raw = response.choices[0].message.content.strip()
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except:
        return {"ideas": [], "best_idea": "", "quick_win": "", "creative_insight": "Think outside the box!"}
