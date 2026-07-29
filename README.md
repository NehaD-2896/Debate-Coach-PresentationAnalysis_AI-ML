# Debate-Coach-PresentationAnalysis_AI-ML

=======================================================
# 🧠 AI Debate Coach – Argument Analysis Engine

## 📌 Overview

This module is part of the **AI Debate Coach & Presentation Analysis Platform**.

The Argument Analysis Engine uses **Google Gemini AI** to analyze a user's debate argument and returns structured insights that can be used by other AI modules and the backend.

---

## 🚀 Features

- Analyze a user's argument
- Extract the main claim
- Identify supporting evidence
- Identify reasoning
- Detect argument type
- Calculate:
  - Strength Score
  - Clarity Score
  - Relevance Score
  - Persuasiveness Score
- Identify missing points
- Generate AI feedback
- Return structured JSON response

---

## 🛠️ Tech Stack

- Python 3.10+
- FastAPI
- Google Gemini API
- Python Dotenv

---

## 📁 Project Structure

```
Debate-Coach-PresentationAnalysis_AI-ML/
│
├── argument_analysis/
│   ├── __init__.py
│   └── analyzer.py
│
├── debate_simulation/
│   └── __init__.py
│
├── recommendation_engine/
│   └── __init__.py
│
├── main.py
├── requirements.txt
├── .gitignore
└── test_gemini.py
```

---

## ⚙️ Setup

### 1. Clone Repository

```bash
git clone <repository-url>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

> **Do NOT commit the `.env` file to GitHub.**

---

## ▶️ Run the API

```bash
uvicorn main:app --reload
```

Server starts at

```
http://127.0.0.1:8000
```

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 📮 API Endpoint

### POST `/argument-analysis`

### Request

```json
{
  "argument": "Artificial Intelligence should replace teachers because it is available 24/7 and provides personalized learning."
}
```

---

## Example Response

```json
{
  "claim": "Artificial Intelligence should replace teachers.",
  "evidence": "AI is available 24/7 and provides personalized learning.",
  "reasoning": "Continuous availability and tailored instruction make AI superior or sufficient to fully take over the responsibilities of human educators.",
  "argument_type": "Policy Argument",
  "persuasiveness": 4,
  "strength_score": 4,
  "clarity_score": 9,
  "relevance_score": 8,
  "missing_points": [
    "Need supporting evidence",
    "Need counterarguments"
  ],
  "feedback": "The argument is clear but lacks supporting evidence and ignores counterarguments."
}
```

---

## 🔄 Workflow

```
User Input
      │
      ▼
FastAPI Endpoint
      │
      ▼
Argument Analysis Engine
      │
      ▼
Google Gemini API
      │
      ▼
JSON Response
      │
      ▼
Frontend / Backend
```

---

## 🔗 Integration

This module will provide its output to:

- Recommendation & Coaching Engine
- AI Debate Simulation Engine
- Performance Scoring Engine
- Backend API
- Frontend Dashboard

---

## 📌 Current Status

| Feature | Status |
|----------|--------|
| Gemini Integration | ✅ Completed |
| FastAPI Integration | ✅ Completed |
| Argument Analysis | ✅ Completed |
| Swagger Testing | ✅ Completed |
| JSON Response | ✅ Completed |
| Backend Integration | ⏳ Pending |
| Frontend Integration | ⏳ Pending |

---

## 👩‍💻 Developed By

**Subhalaxmi Jena**

Infosys Springboard Virtual Internship

AI Debate Coach & Presentation Analysis Platform
