from groq import Groq
from .task_agent import run_task_agent
from .calendar_agent import run_calendar_agent
from .notes_agent import run_notes_agent
import os
import json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def analyze_intent(user_message: str) -> dict:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an intelligent intent analyzer for a personal assistant system.

Analyze the user message deeply and respond ONLY in this exact JSON format:
{
  "primary_intent": "TASK|CALENDAR|NOTES|GENERAL",
  "secondary_intent": "TASK|CALENDAR|NOTES|GENERAL|NONE",
  "confidence": "HIGH|MEDIUM|LOW",
  "urgency": "HIGH|MEDIUM|LOW",
  "action_type": "create|list|complete|delete|search|update|NONE",
  "entities": {
    "title": "extracted title or NONE",
    "datetime": "extracted date/time or NONE",
    "keyword": "extracted keyword or NONE"
  },
  "reasoning": "one line explanation of why you chose this intent"
}

Intent rules:
- TASK → buy, finish, complete, todo, work, assignment, deadline, submit
- CALENDAR → schedule, meeting, appointment, remind, tomorrow, at [time], on [date]
- NOTES → remember, save, note, write down, record, search, find, recall
- GENERAL → greetings, questions, anything else

Multi-intent example:
"Schedule meeting and add task to prepare slides"
→ primary_intent: CALENDAR, secondary_intent: TASK

Urgency rules:
- HIGH → today, urgent, asap, immediately, now
- MEDIUM → tomorrow, this week, soon
- LOW → someday, eventually, no time mentioned"""
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        max_tokens=300
    )

    raw = response.choices[0].message.content.strip()

    try:
        # Clean and parse JSON
        start = raw.find("{")
        end = raw.rfind("}") + 1
        json_str = raw[start:end]
        return json.loads(json_str)
    except:
        # Fallback if JSON parsing fails
        return {
            "primary_intent": "GENERAL",
            "secondary_intent": "NONE",
            "confidence": "LOW",
            "urgency": "LOW",
            "action_type": "NONE",
            "entities": {"title": "NONE", "datetime": "NONE", "keyword": "NONE"},
            "reasoning": "Could not parse intent"
        }

def handle_multi_intent(user_message: str, primary: str, secondary: str) -> str:
    results = []

    if primary == "TASK":
        results.append(f"📋 Tasks: {run_task_agent(user_message)}")
    elif primary == "CALENDAR":
        results.append(f"📅 Calendar: {run_calendar_agent(user_message)}")
    elif primary == "NOTES":
        results.append(f"📝 Notes: {run_notes_agent(user_message)}")

    if secondary and secondary != "NONE":
        if secondary == "TASK":
            results.append(f"📋 Tasks: {run_task_agent(user_message)}")
        elif secondary == "CALENDAR":
            results.append(f"📅 Calendar: {run_calendar_agent(user_message)}")
        elif secondary == "NOTES":
            results.append(f"📝 Notes: {run_notes_agent(user_message)}")

    return "\n\n".join(results)

def handle_low_confidence(user_message: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are a helpful assistant. The user said something unclear.
Ask a smart clarifying question to understand if they want to:
1. Manage tasks
2. Schedule something on calendar
3. Save/search notes
Keep it friendly and short — one sentence only."""
            },
            {
                "role": "user",
                "content": user_message
            }
        ],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

def generate_summary_response(intent_data: dict, result: str) -> dict:
    urgency_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}.get(intent_data.get("urgency"), "⚪")
    confidence_emoji = {"HIGH": "✅", "MEDIUM": "⚠️", "LOW": "❓"}.get(intent_data.get("confidence"), "⚪")

    return {
        "intent": intent_data.get("primary_intent"),
        "secondary_intent": intent_data.get("secondary_intent"),
        "confidence": f"{confidence_emoji} {intent_data.get('confidence')}",
        "urgency": f"{urgency_emoji} {intent_data.get('urgency')}",
        "action": intent_data.get("action_type"),
        "reasoning": intent_data.get("reasoning"),
        "response": result
    }

def orchestrate(user_message: str) -> dict:

    # Step 1 — Deep intent analysis
    intent_data = analyze_intent(user_message)

    primary = intent_data.get("primary_intent", "GENERAL")
    secondary = intent_data.get("secondary_intent", "NONE")
    confidence = intent_data.get("confidence", "LOW")

    # Step 2 — Handle low confidence → ask clarification
    if confidence == "LOW":
        clarification = handle_low_confidence(user_message)
        return generate_summary_response(intent_data, clarification)

    # Step 3 — Handle multi-intent messages
    if secondary and secondary != "NONE" and secondary != primary:
        result = handle_multi_intent(user_message, primary, secondary)
        return generate_summary_response(intent_data, result)

    # Step 4 — Route to correct agent based on primary intent
    if primary == "TASK":
        result = run_task_agent(user_message)

    elif primary == "CALENDAR":
        result = run_calendar_agent(user_message)

    elif primary == "NOTES":
        result = run_notes_agent(user_message)

    else:
        # Step 5 — Handle general conversation
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful personal assistant. Answer general questions. Keep it short and friendly."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=200
        )
        result = response.choices[0].message.content.strip()

    return generate_summary_response(intent_data, result)
