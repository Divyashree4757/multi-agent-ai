# 🤖 Multi-Agent AI System
### GenAI Academy Hackathon Project

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Groq](https://img.shields.io/badge/Groq-Llama3.3-orange)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

A powerful **Multi-Agent AI System** that helps users manage tasks, schedules, and information by coordinating multiple specialized AI agents. Built with **FastAPI**, **Groq (Llama 3.3)**, and **SQLite**, deployed on **Render**.

> "One system. Multiple agents. Infinite productivity."

---

## 🏗️ System Architecture

```
Client (Browser / API)
         ↓
  Primary Orchestrator Agent
  (Intelligent Intent Routing)
         ↓
  ┌──────┬──────────┬───────┐
  │      │          │       │
Task   Calendar   Notes   General
Agent   Agent     Agent   Handler
  │      │          │
  └──────┴──────────┘
         ↓
   SQLite Database
   (Tasks, Events, Notes, Memory)
```

---

## ✨ Features

### 🤖 Core Agents
| Agent | Capabilities |
|-------|-------------|
| **Task Agent** | Create, list, complete, delete tasks |
| **Calendar Agent** | Schedule, list, delete events |
| **Notes Agent** | Save, search, list, delete notes |
| **Orchestrator** | Intelligent routing with multi-intent support |

### 🧠 AI-Powered Features
| Feature | Description |
|---------|-------------|
| 🔮 **Day Predictor** | Predicts productivity score for your day |
| 😊 **Mood Detector** | Analyzes stress level from your messages |
| 🧠 **Weekly Summary** | Generates performance grade and insights |
| ⚡ **Priority Ranker** | Auto-ranks tasks by importance and urgency |
| 🎯 **Goal Coach** | Creates milestones and coaching plans |
| 💡 **Brainstorm Partner** | Generates 5 creative ideas on any topic |
| ⚠️ **Risk Alerter** | Detects deadline risks and overload |
| 📄 **Daily Report** | Auto-generates daily productivity report |
| 🧠 **AI Memory** | Remembers all past conversations |
| 🎤 **Voice Input** | Transcribes voice to text commands |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| **FastAPI** | REST API framework |
| **Groq + Llama 3.3** | Free AI model (no cost!) |
| **SQLAlchemy** | Database ORM |
| **SQLite / PostgreSQL** | Data storage |
| **Python 3.11** | Backend language |
| **HTML/CSS/JS** | Beautiful dark UI |
| **Render** | Cloud deployment |

---

## 📁 Project Structure

```
multi-agent/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI entry point
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py      # Primary agent (intelligent routing)
│   │   ├── task_agent.py        # Task management agent
│   │   ├── calendar_agent.py    # Calendar management agent
│   │   ├── notes_agent.py       # Notes management agent
│   │   ├── predictor_agent.py   # Day prediction agent
│   │   ├── mood_agent.py        # Mood detection agent
│   │   ├── summary_agent.py     # Weekly summary agent
│   │   ├── priority_agent.py    # Task priority ranker
│   │   ├── goal_agent.py        # Goal coaching agent
│   │   ├── alert_agent.py       # Risk alerter + daily report
│   │   └── suggester_agent.py   # Auto task suggester
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── task_tools.py        # Task CRUD operations
│   │   ├── calendar_tools.py    # Calendar CRUD operations
│   │   ├── notes_tools.py       # Notes CRUD operations
│   │   ├── memory_tools.py      # Conversation memory
│   │   ├── analytics_tools.py   # Productivity analytics
│   │   └── voice_tools.py       # Voice transcription
│   ├── db/
│   │   ├── __init__.py
│   │   ├── models.py            # SQLAlchemy models
│   │   └── database.py          # DB connection
│   └── templates/
│       └── index.html           # Beautiful dark UI
├── .env                         # Environment variables
├── .gitignore
├── requirements.txt
├── render.yaml                  # Render deployment config
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Groq API Key (free at [console.groq.com](https://console.groq.com))
- Render Account (free at [render.com](https://render.com))

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/multi-agent-ai.git
cd multi-agent-ai
```

**2. Create virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**
```bash
# Create .env file
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxx
RENDER_API_KEY=rnd_xxxxxxxxxxxxxxxxxxxxxxxx
DATABASE_URL=sqlite:///./local.db
```

**5. Run the application**
```bash
python -m uvicorn app.main:app --reload
```

**6. Open in browser**
```
http://127.0.0.1:8000
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Main chat endpoint — routes to agents |
| `GET` | `/analytics` | Productivity analytics |
| `GET` | `/suggest` | AI task suggestions |
| `GET` | `/predict` | Day prediction score |
| `GET` | `/mood` | Mood detection |
| `GET` | `/summary` | Weekly summary |
| `GET` | `/priority` | Task priority ranking |
| `POST` | `/goal` | AI goal coaching |
| `POST` | `/brainstorm` | Idea generation |
| `GET` | `/risks` | Deadline risk alerts |
| `GET` | `/report` | Daily auto report |
| `POST` | `/voice` | Voice transcription |
| `GET` | `/memory` | Chat history |
| `DELETE` | `/memory` | Clear memory |
| `GET` | `/health` | Server health check |
| `GET` | `/docs` | Swagger UI |

---

## 💬 Example Usage

### Add a Task
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "add task to finish the project today"}'
```

**Response:**
```json
{
  "intent": "TASK",
  "confidence": "✅ HIGH",
  "urgency": "🔴 HIGH",
  "action": "create",
  "response": "I've added 'Finish the project' to your tasks!"
}
```

### Schedule a Meeting
```bash
curl -X POST http://localhost:8000/chat \
  -d '{"message": "schedule team standup tomorrow at 10am"}'
```

### Get Day Prediction
```bash
curl http://localhost:8000/predict
```

**Response:**
```json
{
  "productivity_score": 85,
  "predicted_mood": "Focused",
  "energy_level": "HIGH",
  "ai_advice": "Great day for deep work — tackle your hardest task first!",
  "motivational_quote": "Progress over perfection!"
}
```

---

## 🎨 UI Panels

| Panel | Description |
|-------|-------------|
| 💬 **Chat** | Talk to all agents naturally |
| 🔮 **Predict** | See AI day prediction with productivity score |
| 😊 **Mood** | Check your current stress level |
| 📊 **Analytics** | View full productivity statistics |
| ⚡ **Priority** | See AI-ranked task list |
| 🧠 **Summary** | Weekly performance grade |
| 🎯 **Goals** | Set goals and get AI coaching |
| 💡 **Brainstorm** | Generate ideas with AI |
| 📄 **Report** | Daily report with risk alerts |

---

## ☁️ Deployment on Render

### Using render.yaml (Automatic)
```yaml
services:
  - type: web
    name: multi-agent-api
    runtime: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
    healthCheckPath: /health
    envVars:
      - key: GROQ_API_KEY
        sync: false
      - key: DATABASE_URL
        value: sqlite:///./local.db
```

### Manual Deployment Steps
1. Push code to GitHub
2. Go to [dashboard.render.com](https://dashboard.render.com)
3. New → Web Service → Connect GitHub repo
4. Add `GROQ_API_KEY` in Environment Variables
5. Click Deploy!

**Live URL:** `https://multi-agent-api.onrender.com`

---

## 🔒 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | Groq API key for AI | ✅ Yes |
| `DATABASE_URL` | Database connection string | ✅ Yes |
| `RENDER_API_KEY` | Render API key for deployment | Optional |

---

## 📊 Database Schema

```
memories         tasks            events           notes
──────────       ──────────       ──────────       ──────────
id (PK)          id (PK)          id (PK)          id (PK)
role             title            title            content
content          description      start_time       tags
intent           done             end_time         created_at
created_at       priority         created_at
                 created_at
```

---

## 🤝 How Multi-Agent Coordination Works

```
User: "Add task to prepare slides and schedule meeting tomorrow"
          ↓
1. Orchestrator analyzes intent
   → primary_intent: CALENDAR
   → secondary_intent: TASK
   → confidence: HIGH
          ↓
2. Routes to BOTH agents simultaneously
   → Task Agent: creates "Prepare slides" task
   → Calendar Agent: schedules meeting
          ↓
3. Returns combined response to user
```

---

## 🏆 Hackathon Highlights

- ✅ **Multi-agent coordination** with intelligent routing
- ✅ **15+ AI-powered features** built on free Groq API
- ✅ **Zero cost** — completely free to run and deploy
- ✅ **Real-world workflows** — tasks, calendar, notes
- ✅ **Beautiful dark UI** — production-ready design
- ✅ **REST API** — 15+ endpoints with Swagger docs
- ✅ **AI Memory** — context-aware conversations
- ✅ **Voice input** — speak your commands

---

## 📈 Future Enhancements

- [ ] User authentication and multi-user support
- [ ] Mobile app (React Native)
- [ ] Email and Slack notifications
- [ ] Google Calendar integration
- [ ] Export reports as PDF
- [ ] Collaborative tasks (team features)
- [ ] Custom AI agent creation

---

## 👥 Team

Built for **GenAI Academy Hackathon** 🏆

---

## 📄 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- [Groq](https://groq.com) — Free and fast AI API
- [FastAPI](https://fastapi.tiangolo.com) — Amazing Python framework
- [Render](https://render.com) — Free cloud deployment
- [SQLAlchemy](https://sqlalchemy.org) — Powerful Python ORM

---

<div align="center">
  <strong>Built with ❤️ for GenAI Academy Hackathon 🏆</strong>
</div>
