from groq import Groq
from ..tools.task_tools import list_tasks, create_task
from ..tools.calendar_tools import list_events
from ..tools.notes_tools import list_notes
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def auto_suggest_tasks() -> dict:
    tasks = list_tasks()
    events = list_events()
    notes = list_notes()

    pending_tasks = [t for t in tasks if not t["done"]]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a smart productivity assistant.
Analyze the user's current data and suggest helpful tasks.
Respond ONLY in this exact JSON format:
{
  "suggestions": [
    {
      "title": "task title",
      "reason": "why this task is suggested",
      "priority": "HIGH|MEDIUM|LOW",
      "auto_create": true|false
    }
  ],
  "productivity_tip": "one helpful tip based on their data"
}
Rules:
- Max 3 suggestions
- Only suggest relevant tasks based on existing data
- auto_create true only for obvious follow-up tasks"""
            },
            {
                "role": "user",
                "content": f"""Current data:
Pending tasks: {pending_tasks}
Upcoming events: {events}
Recent notes: {notes}

Suggest helpful tasks based on this data."""
            }
        ],
        max_tokens=400
    )

    raw = response.choices[0].message.content.strip()
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        result = json.loads(raw[start:end])

        # Auto create suggested tasks
        created = []
        for s in result.get("suggestions", []):
            if s.get("auto_create"):
                task = create_task(s["title"])
                created.append(task["title"])

        result["auto_created"] = created
        return result
    except:
        return {
            "suggestions": [],
            "productivity_tip": "Stay focused and tackle one task at a time!",
            "auto_created": []
        }
