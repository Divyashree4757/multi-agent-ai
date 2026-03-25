from ..db.database import SessionLocal
from ..db.models import Task

def create_task(title: str, description: str = ""):
    db = SessionLocal()
    task = Task(title=title, description=description)
    db.add(task)
    db.commit()
    db.refresh(task)
    db.close()
    return {"id": task.id, "title": task.title, "description": task.description}

def list_tasks():
    db = SessionLocal()
    tasks = db.query(Task).all()
    db.close()
    return [{"id": t.id, "title": t.title, "done": t.done} for t in tasks]

def complete_task(task_id: str):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.done = True
        db.commit()
        db.close()
        return {"status": "completed", "title": task.title}
    db.close()
    return {"error": "Task not found"}

def delete_task(task_id: str):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
        db.close()
        return {"status": "deleted"}
    db.close()
    return {"error": "Task not found"}   
