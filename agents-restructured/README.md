# Debate-Coach-PresentationAnalysis_AI-ML
=======================================================

# 🧠 AI Debate Coach – Argument Analysis and Logical Fallacy Engine

## 📌 Overview
This folder contains the core argument analysis and fallacy detection modules for the AI Debate Coach.
It uses Google Gemini to inspect a debate argument, score it, and return structured JSON results.

---

## 🚀 Features

- Analyze a user argument
- Extract the main claim and evidence
- Score argument strength, clarity, relevance, and logical consistency
- Detect common logical fallacies
- Return structured JSON output
- Keep API keys out of the source code using `.env`

---

## 🛠️ Tech Stack

- Python 3.10+
- Google Gemini API (`google-genai`)
- Python Dotenv
- FastAPI / Uvicorn dependencies available for future API integration

---

## 📁 Project Structure

```
agents-restructured/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── llm_client.py
│   ├── run_flow.py
│   └── agents/
│       ├── __init__.py
│       ├── argument_analysis_agent.py
│       ├── base_agent.py
│       └── fallacy_detection_agent.py
│
├── requirements.txt
├── tests/
│   ├── test_agents_demo.py
│   └── test_fallacies.py
└── .env
```

---

## ⚙️ Setup

### 1. Clone Repository

```
git clone <repository-url>
```

### 2. Install Dependencies

```
pip install -r requirements.txt
```

### 3. Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
LLM_MODEL=gemini-flash-latest
```

> **Do NOT commit the `.env` file to GitHub.**

---

## ▶️ Run the module

```
python app/run_flow.py "Your argument goes here"
```

or from package mode:

```
python -m app.run_flow
```

---

## 📮 Output

The module returns structured JSON for the argument analysis and fallacy detection logic.

---

## Example Response

```
{
  "claim": "Artificial Intelligence should replace teachers.",
  "evidence": [
    "AI can provide personalized tutoring.",
    "AI is available 24/7.",
    "AI can reduce educational costs."
  ],
  "strength_label": "weak",
  "strength_score": 45,
  "clarity_score": 85,
  "relevance_score": 90,
  "logical_consistency_score": 40,
  "notes": "The argument provides relevant points regarding convenience and cost, but it fundamentally undermines its own conclusion by admitting that human empathy and guidance—essential parts of teaching—remain important."
}
```

---

## 🔄 Workflow

```
User Input
      │
      ▼
Run Flow / Module
      │
      ▼
Argument Analysis Agent
      │
      ▼
Google Gemini API
      │
      ▼
Structured JSON Output
      │
      ▼
Backend / Frontend Integration
```

---

## 🔗 Integration
This module can be used by:

- Recommendation & coaching engine
- Debate simulation engine
- Performance scoring engine
- Backend API
- Frontend dashboard

---

## 📌 Current Status
- Gemini integration: ✅ Completed
- Argument analysis agent: ✅ Completed
- Fallacy detection agent: ✅ Completed
- FastAPI endpoint: ⏳ Pending
- Frontend integration: ⏳ Pending

---

## 👩‍💻 Developed By
**Archit**
