from groq import Groq
from ..tools.task_tools import list_tasks
from ..tools.calendar_tools import list_events
from ..tools.analytics_tools import get_analytics
import os, json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def check_risks() -> dict:
    tasks = list_tasks()
    events = list_events()
    pending = [t for t in tasks if not t["done"]]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a risk assessment AI for productivity.
Respond ONLY in this JSON format:
{
  "overall_risk": "HIGH|MEDIUM|LOW",
  "risk_score": 0-100,
  "alerts": [
    {
      "type": "OVERLOAD|DEADLINE|CONFLICT|IDLE",
      "severity": "HIGH|MEDIUM|LOW",
      "message": "alert message",
      "action": "recommended action"
    }
  ],
  "overloaded": true|false,
  "idle_warning": true|false,
  "recommendation": "top recommendation to reduce risk"
}"""
            },
            {
                "role": "user",
                "content": f"Pending tasks: {pending}\nEvents: {events}\nAnalyze risks."
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
            "overall_risk": "LOW",
            "risk_score": 20,
            "alerts": [],
            "overloaded": False,
            "idle_warning": len(pending) == 0,
            "recommendation": "Keep up the good work!"
        }

def generate_daily_report() -> dict:
    tasks = list_tasks()
    events = list_events()
    analytics = get_analytics()
    completed = [t for t in tasks if t["done"]]
    pending = [t for t in tasks if not t["done"]]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """Generate a daily productivity report.
Respond ONLY in this JSON format:
{
  "date": "today",
  "title": "Daily Report Title",
  "score": 0-100,
  "grade": "A+|A|B+|B|C|D",
  "completed_count": 0,
  "pending_count": 0,
  "highlights": ["highlight 1", "highlight 2"],
  "tomorrow_priority": "most important task for tomorrow",
  "daily_quote": "inspirational quote",
  "summary": "two sentence summary of the day"
}"""
            },
            {
                "role": "user",
                "content": f"Completed: {completed}\nPending: {pending}\nEvents: {events}\nAnalytics: {analytics}"
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
            "date": "today",
            "title": "Daily Productivity Report",
            "score": 70,
            "grade": "B+",
            "completed_count": len(completed),
            "pending_count": len(pending),
            "highlights": ["Made progress today!"],
            "tomorrow_priority": pending[0]["title"] if pending else "Plan your day",
            "daily_quote": "Progress over perfection!",
            "summary": "A solid day of work. Keep the momentum going!"
        }
