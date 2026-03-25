from groq import Groq
from ..tools.memory_tools import get_recent_memory
import os, json
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def detect_mood() -> dict:
    memories = get_recent_memory(10)
    user_messages = [m["content"] for m in memories if m["role"] == "user"]

    if not user_messages:
        return {
            "mood": "Neutral",
            "emoji": "😐",
            "stress_level": 50,
            "energy": "MEDIUM",
            "insight": "Not enough data yet. Keep chatting!",
            "recommendation": "Start by adding your tasks for today!"
        }

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """Analyze the user messages and detect their mood and stress level.
Respond ONLY in this JSON format:
{
  "mood": "Happy|Stressed|Focused|Overwhelmed|Motivated|Tired|Anxious|Calm",
  "emoji": "appropriate emoji",
  "stress_level": 0-100,
  "energy": "HIGH|MEDIUM|LOW",
  "insight": "one sentence insight about their current state",
  "recommendation": "one actionable recommendation to improve their day"
}"""
            },
            {
                "role": "user",
                "content": f"User's recent messages: {user_messages}"
            }
        ],
        max_tokens=200
    )

    raw = response.choices[0].message.content.strip()
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        return json.loads(raw[start:end])
    except:
        return {
            "mood": "Focused",
            "emoji": "🎯",
            "stress_level": 40,
            "energy": "MEDIUM",
            "insight": "You seem focused and productive!",
            "recommendation": "Keep up the great work!"
        }
