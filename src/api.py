import os
import json
import time
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from dotenv import load_dotenv
load_dotenv()

from src.llm_engine import LLMEngine
from src.mood import detect_mood
from src.prompts import build_chat_prompt, build_feedback_prompt
from src.quiz import generate_quiz, evaluate_quiz, save_quiz_result, load_quiz_history

app = FastAPI(title="Adaptive Tutoring API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM engine once
llm = LLMEngine()

class ChatRequest(BaseModel):
    subject: str
    message: str
    context: Optional[str] = ""

class QuizRequest(BaseModel):
    subject: str
    topic: str
    num_questions: Optional[int] = 10

class EvaluateRequest(BaseModel):
    subject: str
    questions: List[Dict[str, Any]]
    answers: Dict[int, int]

class NoteRequest(BaseModel):
    content: str

@app.post("/api/chat")
def chat_endpoint(req: ChatRequest):
    mood = detect_mood(req.message)
    full_prompt = build_chat_prompt(req.subject, req.message, req.context)
    response = llm.generate(full_prompt)
    return {
        "response": response,
        "mood": mood,
        "timestamp": time.time()
    }

@app.post("/api/quiz/generate")
def quiz_generate_endpoint(req: QuizRequest):
    quiz = generate_quiz(llm, req.subject, req.topic, req.num_questions)
    if not quiz:
        raise HTTPException(status_code=500, detail="Failed to generate quiz")
    return {"quiz": quiz}

@app.post("/api/quiz/evaluate")
def quiz_evaluate_endpoint(req: EvaluateRequest):
    # Convert string keys in dict to int (if parsed from JSON)
    answers = {int(k): v for k, v in req.answers.items()}
    score, total, results = evaluate_quiz(req.questions, answers)
    save_quiz_result(score, total, req.subject)
    
    # Generate feedback
    feedback_prompt = build_feedback_prompt(score, req.subject)
    feedback = llm.generate(feedback_prompt, max_tokens=300, temperature=0.7)
    
    return {
        "score": score,
        "total": total,
        "results": results,
        "feedback": feedback
    }

@app.get("/api/quiz/history")
def quiz_history_endpoint():
    history = load_quiz_history()
    return {"history": history}

@app.post("/api/notes")
def save_note_endpoint(req: NoteRequest):
    notes_file = os.getenv("NOTES_FILE", "data/notes.txt")
    if not os.path.isabs(notes_file):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        notes_file = os.path.join(project_root, notes_file)
    os.makedirs(os.path.dirname(notes_file), exist_ok=True)
    with open(notes_file, "a", encoding="utf-8") as f:
        f.write(req.content + "\n\n")
    return {"status": "success"}

@app.get("/api/notes")
def get_notes_endpoint():
    notes_file = os.getenv("NOTES_FILE", "data/notes.txt")
    if not os.path.isabs(notes_file):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        notes_file = os.path.join(project_root, notes_file)
    if not os.path.exists(notes_file):
        return {"notes": []}
    with open(notes_file, "r", encoding="utf-8") as f:
        content = f.read()
    # Split notes by double newline
    notes = [n.strip() for n in content.split("\n\n") if n.strip()]
    return {"notes": notes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
