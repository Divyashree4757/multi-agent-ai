from ..db.database import SessionLocal
from ..db.models import Task, Event, Note, Memory
from datetime import datetime, timedelta

def get_analytics() -> dict:
    db = SessionLocal()

    # Task stats
    all_tasks = db.query(Task).all()
    completed = [t for t in all_tasks if t.done]
    pending = [t for t in all_tasks if not t.done]

    # Events stats
    all_events = db.query(Event).all()
    upcoming = [e for e in all_events if e.start_time and e.start_time > datetime.utcnow()]

    # Notes stats
    all_notes = db.query(Note).all()

    # Memory / chat stats
    all_chats = db.query(Memory).all()
    user_chats = [m for m in all_chats if m.role == "user"]

    # Most used intent
    intents = [m.intent for m in all_chats if m.intent]
    intent_counts = {}
    for i in intents:
        intent_counts[i] = intent_counts.get(i, 0) + 1
    top_intent = max(intent_counts, key=intent_counts.get) if intent_counts else "NONE"

    # Tasks created this week
    week_ago = datetime.utcnow() - timedelta(days=7)
    tasks_this_week = [t for t in all_tasks if t.created_at and t.created_at > week_ago]

    db.close()

    completion_rate = round((len(completed) / len(all_tasks) * 100)) if all_tasks else 0

    return {
        "tasks": {
            "total": len(all_tasks),
            "completed": len(completed),
            "pending": len(pending),
            "completion_rate": f"{completion_rate}%",
            "this_week": len(tasks_this_week)
        },
        "calendar": {
            "total_events": len(all_events),
            "upcoming": len(upcoming)
        },
        "notes": {
            "total": len(all_notes)
        },
        "conversations": {
            "total_messages": len(user_chats),
            "most_used_feature": top_intent
        },
        "summary": f"You have {len(pending)} pending tasks, {len(upcoming)} upcoming events and {len(all_notes)} notes saved."
    }
