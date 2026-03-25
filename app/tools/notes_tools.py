from ..db.database import SessionLocal
from ..db.models import Note

def save_note(content: str, tags: str = ""):
    db = SessionLocal()
    note = Note(content=content, tags=tags)
    db.add(note)
    db.commit()
    db.refresh(note)
    db.close()
    return {"id": note.id, "content": note.content, "tags": note.tags}

def list_notes():
    db = SessionLocal()
    notes = db.query(Note).all()
    db.close()
    return [{"id": n.id, "content": n.content, "tags": n.tags} for n in notes]

def search_notes(keyword: str):
    db = SessionLocal()
    notes = db.query(Note).filter(Note.content.contains(keyword)).all()
    db.close()
    return [{"id": n.id, "content": n.content, "tags": n.tags} for n in notes]

def delete_note(note_id: str):
    db = SessionLocal()
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
        db.close()
        return {"status": "deleted"}
    db.close()
    return {"error": "Note not found"} 
