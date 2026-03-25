from groq import Groq
from ..tools.task_tools import create_task, list_tasks, complete_task, delete_task
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_task_agent(user_message: str) -> str:
    current_tasks = list_tasks()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""You are a task management assistant.
Current tasks in database: {current_tasks}

Based on user message decide action and respond in this exact format:
ACTION: create|list|complete|delete
TITLE: task title (only for create)
ID: task id (only for complete or delete)
RESPONSE: friendly message to user

Examples:
User: add task to buy milk
ACTION: create
TITLE: Buy milk
ID: none
RESPONSE: I have added 'Buy milk' to your tasks!

User: show my tasks
ACTION: list
TITLE: none
ID: none
RESPONSE: Here are your current tasks!

User: complete task abc123
ACTION: complete
TITLE: none
ID: abc123
RESPONSE: Great job! Task marked as complete!"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        max_tokens=256
    )

    ai_reply = response.choices[0].message.content
    lines = ai_reply.strip().split("\n")

    action = ""
    title = ""
    task_id = ""
    friendly_response = ""

    for line in lines:
        if line.startswith("ACTION:"):
            action = line.replace("ACTION:", "").strip().lower()
        elif line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
        elif line.startswith("ID:"):
            task_id = line.replace("ID:", "").strip()
        elif line.startswith("RESPONSE:"):
            friendly_response = line.replace("RESPONSE:", "").strip()

    if action == "create" and title and title != "none":
        result = create_task(title)
        return f"{friendly_response} (Task ID: {result['id']})"

    elif action == "list":
        tasks = list_tasks()
        if not tasks:
            return "You have no tasks yet! Add one by saying 'add task to...'"
        task_list = "\n".join([f"- {'✅' if t['done'] else '⬜'} {t['title']} (ID: {t['id']})" for t in tasks])
        return f"{friendly_response}\n\n{task_list}"

    elif action == "complete" and task_id and task_id != "none":
        result = complete_task(task_id)
        return friendly_response if "error" not in result else f"Task not found with ID: {task_id}"

    elif action == "delete" and task_id and task_id != "none":
        result = delete_task(task_id)
        return friendly_response if "error" not in result else f"Task not found with ID: {task_id}"

    return friendly_response or "I can help you manage tasks! Try saying 'add task to buy milk'"
