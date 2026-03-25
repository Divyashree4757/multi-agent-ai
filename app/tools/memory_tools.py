from ..db.database import SessionLocal
from ..db.models import Memory

def save_memory(role: str, content: str, intent: str = ""):
    db = SessionLocal()
    memory = Memory(role=role, content=content, intent=intent)
    db.add(memory)
    db.commit()
    db.close()

def get_recent_memory(limit: int = 10):
    db = SessionLocal()
    memories = db.query(Memory).order_by(Memory.created_at.desc()).limit(limit).all()
    db.close()
    return [{"role": m.role, "content": m.content, "intent": m.intent} for m in reversed(memories)]

def clear_memory():
    db = SessionLocal()
    db.query(Memory).delete()
    db.commit()
    db.close()
    return {"status": "memory cleared"}

def get_memory_context() -> str:
    memories = get_recent_memory(6)
    if not memories:
        return "No previous conversation history."
    context = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in memories])
    return f"Recent conversation:\n{context}"
