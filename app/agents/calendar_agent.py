from groq import Groq
from ..tools.calendar_tools import create_event, list_events, delete_event
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_calendar_agent(user_message: str) -> str:
    current_events = list_events()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""You are a calendar assistant.
Current events in database: {current_events}

Based on user message decide action and respond in this exact format:
ACTION: create|list|delete
TITLE: event title (only for create)
START: start time in ISO format like 2024-03-25T10:00:00 (only for create)
END: end time in ISO format like 2024-03-25T11:00:00 (only for create)
ID: event id (only for delete)
RESPONSE: friendly message to user

Examples:
User: schedule a meeting tomorrow at 10am
ACTION: create
TITLE: Meeting
START: 2024-03-25T10:00:00
END: 2024-03-25T11:00:00
ID: none
RESPONSE: I have scheduled your meeting for tomorrow at 10am!

User: show my events
ACTION: list
TITLE: none
START: none
END: none
ID: none
RESPONSE: Here are your upcoming events!"""
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
    start = ""
    end = ""
    event_id = ""
    friendly_response = ""

    for line in lines:
        if line.startswith("ACTION:"):
            action = line.replace("ACTION:", "").strip().lower()
        elif line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
        elif line.startswith("START:"):
            start = line.replace("START:", "").strip()
        elif line.startswith("END:"):
            end = line.replace("END:", "").strip()
        elif line.startswith("ID:"):
            event_id = line.replace("ID:", "").strip()
        elif line.startswith("RESPONSE:"):
            friendly_response = line.replace("RESPONSE:", "").strip()

    if action == "create" and title and title != "none":
        result = create_event(title, start, end)
        return f"{friendly_response} (Event ID: {result['id']})"

    elif action == "list":
        events = list_events()
        if not events:
            return "You have no events yet! Try saying 'schedule a meeting tomorrow at 10am'"
        event_list = "\n".join([f"- 📅 {e['title']} at {e['start_time']} (ID: {e['id']})" for e in events])
        return f"{friendly_response}\n\n{event_list}"

    elif action == "delete" and event_id and event_id != "none":
        result = delete_event(event_id)
        return friendly_response if "error" not in result else f"Event not found with ID: {event_id}"

    return friendly_response or "I can help you manage your calendar! Try saying 'schedule a meeting tomorrow at 10am'"
