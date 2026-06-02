# Adaptive Tutoring Agent

An AI-powered tutoring application that provides personalized learning experiences across various subjects. It features a real-time mood-aware chat interface, adaptive quiz generation, and a notes management system.

## Feature Overview

1. **Study Chat**: A conversational interface powered by Google Gemini. It detects user mood (frustrated, happy, neutral, disengaged) and adapts its tone accordingly. Responses are streamed in real-time.
2. **Quiz Module**: Generates subject-specific multiple-choice quizzes, evaluates answers, provides adaptive feedback, and tracks quiz history.
3. **Notes Management**: Allows users to save important chat responses or manually write notes, persist them locally, and export them as JSON.

## Architecture

This project uses a modern decoupled architecture:
- **Backend**: FastAPI providing REST endpoints and Server-Sent Events (SSE) for real-time streaming.
- **Frontend**: Vite + React 19 + Tailwind CSS for a highly responsive, animated, and modern user interface.

## Prerequisites

- **Python 3.9+**
- **Node.js 18+** & npm
- **Gemini API Key** (Set as `GEMINI_API_KEY` in your environment)

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd adaptive-tutoring-agent
   ```

2. **Backend Setup**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   ```

## .env Guide

Create a `.env` file in the root of the project to configure the application:

```ini
APP_TITLE="Adaptive Tutoring Agent"
GEMINI_API_KEY="your_api_key_here"
NOTES_FILE="data/notes.json"
QUIZ_HISTORY_FILE="data/quiz_history.json"
```

## How to Run

1. **Start the Backend API**:
   ```bash
   # From the project root
   python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the Frontend**:
   ```bash
   # In a new terminal, from the frontend directory
   cd frontend
   npm run dev
   ```

Open your browser to the local URL provided by Vite (usually `http://localhost:5173`) to use the application.
