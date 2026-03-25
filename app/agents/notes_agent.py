from groq import Groq
from ..tools.notes_tools import save_note, list_notes, search_notes, delete_note
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_notes_agent(user_message: str) -> str:
    current_notes = list_notes()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""You are a notes assistant.
Current notes in database: {current_notes}

Based on user message decide action and respond in this exact format:
ACTION: save|list|search|delete
CONTENT: note content (only for save)
KEYWORD: search keyword (only for search)
TAGS: comma separated tags (only for save)
ID: note id (only for delete)
RESPONSE: friendly message to user

Examples:
User: save a note that the meeting is at 10am
ACTION: save
CONTENT: The meeting is at 10am
TAGS: meeting
ID: none
KEYWORD: none
RESPONSE: I have saved your note!

User: search notes about meeting
ACTION: search
CONTENT: none
TAGS: none
ID: none
KEYWORD: meeting
RESPONSE: Here are your notes about meeting!

User: show all my notes
ACTION: list
CONTENT: none
TAGS: none
ID: none
KEYWORD: none
RESPONSE: Here are all your notes!"""
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
    content = ""
    keyword = ""
    tags = ""
    note_id = ""
    friendly_response = ""

    for line in lines:
        if line.startswith("ACTION:"):
            action = line.replace("ACTION:", "").strip().lower()
        elif line.startswith("CONTENT:"):
            content = line.replace("CONTENT:", "").strip()
        elif line.startswith("KEYWORD:"):
            keyword = line.replace("KEYWORD:", "").strip()
        elif line.startswith("TAGS:"):
            tags = line.replace("TAGS:", "").strip()
        elif line.startswith("ID:"):
            note_id = line.replace("ID:", "").strip()
        elif line.startswith("RESPONSE:"):
            friendly_response = line.replace("RESPONSE:", "").strip()

    if action == "save" and content and content != "none":
        result = save_note(content, tags)
        return f"{friendly_response} (Note ID: {result['id']})"

    elif action == "list":
        notes = list_notes()
        if not notes:
            return "You have no notes yet! Try saying 'save a note that...'"
        notes_list = "\n".join([f"- 📝 {n['content']} (ID: {n['id']})" for n in notes])
        return f"{friendly_response}\n\n{notes_list}"

    elif action == "search" and keyword and keyword != "none":
        notes = search_notes(keyword)
        if not notes:
            return f"No notes found containing '{keyword}'"
        notes_list = "\n".join([f"- 📝 {n['content']} (ID: {n['id']})" for n in notes])
        return f"{friendly_response}\n\n{notes_list}"

    elif action == "delete" and note_id and note_id != "none":
        result = delete_note(note_id)
        return friendly_response if "error" not in result else f"Note not found with ID: {note_id}"

    return friendly_response or "I can help you manage notes! Try saying 'save a note that...'"
