from groq import Groq
from ..tools.task_tools import list_tasks
from ..tools.calendar_tools import list_events
from ..tools.memory_tools import get_memory_context
import os, json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def predict_day() -> dict:
    tasks = list_tasks()
    events = list_events()
    memory = get_memory_context()
    pending = [t for t in tasks if not t["done"]]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an AI life coach that predicts how productive the user's day will be.
Respond ONLY in this JSON format:
{
  "productivity_score": 85,
  "energy_level": "HIGH|MEDIUM|LOW",
  "predicted_mood": "Focused|Stressed|Relaxed|Overwhelmed|Motivated",
  "busiest_hour": "10am-12pm",
  "risk_factors": ["too many tasks", "back to back meetings"],
  "opportunities": ["good morning for deep work", "light afternoon for creative tasks"],
  "ai_advice": "one powerful personalized advice sentence",
  "predicted_completion": "60%",
  "motivational_quote": "short inspiring quote"
}"""
            },
            {
                "role": "user",
                "content": f"Pending tasks: {pending}\nEvents: {events}\nRecent context: {memory}"
            }
        ],
        max_tokens=400
    )

    raw = response.choices[0].message.content.strip()
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except:
        return {
            "productivity_score": 75,
            "energy_level": "MEDIUM",
            "predicted_mood": "Focused",
            "busiest_hour": "Morning",
            "risk_factors": [],
            "opportunities": ["Great day ahead!"],
            "ai_advice": "Take it one task at a time!",
            "predicted_completion": "70%",
            "motivational_quote": "Every day is a new opportunity!"
        }
