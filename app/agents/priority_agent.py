from groq import Groq
from ..tools.task_tools import list_tasks
from ..db.database import SessionLocal
from ..db.models import Task
import os, json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def rank_tasks_by_priority() -> dict:
    tasks = list_tasks()
    pending = [t for t in tasks if not t["done"]]

    if not pending:
        return {"ranked_tasks": [], "message": "No pending tasks to rank!"}

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a task priority expert. Rank tasks by importance and urgency.
Respond ONLY in this JSON format:
{
  "ranked_tasks": [
    {
      "id": "task_id",
      "title": "task title",
      "priority": "CRITICAL|HIGH|MEDIUM|LOW",
      "priority_score": 0-100,
      "reason": "why this priority",
      "do_by": "today|tomorrow|this week|someday",
      "emoji": "relevant emoji"
    }
  ],
  "focus_task": "title of the single most important task to do right now",
  "tip": "one tip for tackling these tasks"
}
Rank from highest to lowest priority."""
            },
            {
                "role": "user",
                "content": f"Tasks to rank: {pending}"
            }
        ],
        max_tokens=500
    )

    raw = response.choices[0].message.content.strip()
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        result = json.loads(raw[start:end])

        # Update priorities in database
        db = SessionLocal()
        for task in result.get("ranked_tasks", []):
            db_task = db.query(Task).filter(Task.id == task["id"]).first()
            if db_task:
                db_task.priority = task["priority"]
        db.commit()
        db.close()

        return result
    except:
        return {
            "ranked_tasks": pending,
            "focus_task": pending[0]["title"] if pending else "None",
            "tip": "Focus on one task at a time!"
        }
