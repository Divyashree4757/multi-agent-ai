from ..db.database import SessionLocal
from ..db.models import Event
from datetime import datetime

def create_event(title: str, start_time: str, end_time: str = ""):
    db = SessionLocal()
    event = Event(
        title=title,
        start_time=datetime.fromisoformat(start_time) if start_time else None,
        end_time=datetime.fromisoformat(end_time) if end_time else None
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    db.close()
    return {"id": event.id, "title": event.title, "start_time": str(event.start_time)}

def list_events():
    db = SessionLocal()
    events = db.query(Event).all()
    db.close()
    return [{"id": e.id, "title": e.title, "start_time": str(e.start_time)} for e in events]

def delete_event(event_id: str):
    db = SessionLocal()
    event = db.query(Event).filter(Event.id == event_id).first()
    if event:
        db.delete(event)
        db.commit()
        db.close()
        return {"status": "deleted"}
    db.close()
    return {"error": "Event not found"} 
