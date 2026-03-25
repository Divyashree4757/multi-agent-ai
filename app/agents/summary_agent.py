from groq import Groq
from ..tools.task_tools import list_tasks
from ..tools.calendar_tools import list_events
from ..tools.notes_tools import list_notes
from ..tools.analytics_tools import get_analytics
import os, json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_weekly_summary() -> dict:
    analytics = get_analytics()
    tasks = list_tasks()
    events = list_events()
    notes = list_notes()
    completed = [t for t in tasks if t["done"]]
    pending = [t for t in tasks if not t["done"]]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a personal productivity coach generating a weekly summary.
Respond ONLY in this JSON format:
{
  "headline": "catchy one line summary of the week",
  "performance_grade": "A+|A|B+|B|C|D",
  "wins": ["win 1", "win 2", "win 3"],
  "areas_to_improve": ["area 1", "area 2"],
  "key_insight": "most important insight about productivity patterns",
  "next_week_focus": "one clear focus area for next week",
  "streak": "X days productive streak",
  "productivity_percentage": 0-100
}"""
            },
            {
                "role": "user",
                "content": f"""
Analytics: {analytics}
Completed tasks: {completed}
Pending tasks: {pending}
Events: {events}
Notes count: {len(notes)}
Generate an insightful weekly summary."""
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
            "headline": "A productive week overall!",
            "performance_grade": "B+",
            "wins": ["Tasks completed", "Notes saved", "Events scheduled"],
            "areas_to_improve": ["Complete pending tasks faster"],
            "key_insight": "You are most productive in the morning",
            "next_week_focus": "Clear all pending tasks",
            "streak": "3 days productive streak",
            "productivity_percentage": 70
        }
