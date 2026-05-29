"""
Quiz Module — MCQ generation, evaluation, and history management.

Generates multiple-choice quizzes via the LLM, parses JSON responses,
evaluates student answers, and persists quiz history to disk.
"""
import json
import os
import re
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()


def generate_quiz(llm, subject: str, num_questions: int = 5) -> list:
    """
    Generate a multiple-choice quiz using the LLM.

    Args:
        llm: An LLMEngine instance.
        subject: The academic subject for quiz questions.
        num_questions: Number of MCQ questions to generate.

    Returns:
        A list of question dicts: [{"question", "options", "correct_index"}].
        Returns an empty list on failure.
    """
    from src.prompts import build_quiz_prompt

    prompt = build_quiz_prompt(subject, num_questions)

    # Attempt generation (with one retry on parse failure)
    for attempt in range(2):
        response = llm.generate(
            prompt,
            max_tokens=2048,
            temperature=0.5
        )

        questions = _parse_quiz_json(response, num_questions)
        if questions:
            return questions

        if attempt == 0:
            # Retry with a more explicit prompt
            prompt = (
                f"You are a quiz generator. Return ONLY a valid JSON array, no explanation.\n\n"
                f"Generate {num_questions} multiple choice questions about {subject}.\n"
                f'Format: [{{"question": "...", "options": ["A", "B", "C", "D"], "correct_index": 0}}]\n'
                f"Return ONLY the JSON array."
            )

    return []


def _parse_quiz_json(response: str, expected_count: int) -> list:
    """
    Parse the LLM response to extract a JSON array of quiz questions.

    Args:
        response: Raw LLM output text.
        expected_count: Expected number of questions.

    Returns:
        Parsed list of question dicts, or None on failure.
    """
    try:
        # Try to find a JSON array in the response
        # The prompt ends with '[' so we prepend it
        text = "[" + response if not response.strip().startswith("[") else response

        # Try to extract JSON array using regex
        match = re.search(r'\[.*\]', text, re.DOTALL)
        if not match:
            return None

        json_str = match.group(0)

        # Clean up common LLM formatting issues
        json_str = json_str.replace("'", '"')  # Single to double quotes
        json_str = re.sub(r',\s*]', ']', json_str)  # Trailing commas
        json_str = re.sub(r',\s*}', '}', json_str)  # Trailing commas in objects

        questions = json.loads(json_str)

        if not isinstance(questions, list):
            return None

        # Validate each question structure
        validated = []
        for q in questions:
            if _validate_question(q):
                validated.append({
                    "question": str(q["question"]),
                    "options": [str(opt) for opt in q["options"][:4]],
                    "correct_index": int(q["correct_index"]),
                })

        return validated if len(validated) >= 1 else None

    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return None


def _validate_question(q: dict) -> bool:
    """Check if a question dict has the required structure."""
    if not isinstance(q, dict):
        return False
    if "question" not in q or "options" not in q or "correct_index" not in q:
        return False
    if not isinstance(q["options"], list) or len(q["options"]) < 4:
        return False
    if not isinstance(q["correct_index"], (int, float)):
        return False
    if int(q["correct_index"]) < 0 or int(q["correct_index"]) > 3:
        return False
    return True


def evaluate_quiz(questions: list, answers: dict) -> tuple:
    """
    Evaluate student answers against correct answers.

    Args:
        questions: List of question dicts with correct_index.
        answers: Dict mapping question index (int) to selected option index (int).

    Returns:
        Tuple of (score, total, results_list) where results_list contains
        per-question result dicts.
    """
    score = 0
    total = len(questions)
    results = []

    for i, q in enumerate(questions):
        student_answer = answers.get(i, -1)
        correct = q["correct_index"]
        is_correct = student_answer == correct

        if is_correct:
            score += 1

        results.append({
            "question": q["question"],
            "student_answer": student_answer,
            "correct_answer": correct,
            "is_correct": is_correct,
            "correct_option": q["options"][correct] if correct < len(q["options"]) else "N/A",
        })

    return score, total, results


def save_quiz_result(score: int, total: int, subject: str) -> None:
    """
    Save a quiz result to the history file.

    Args:
        score: Number of correct answers.
        total: Total number of questions.
        subject: The quiz subject.
    """
    history_file = os.getenv("QUIZ_HISTORY_FILE", "./data/quiz_history.json")

    # Resolve relative path
    if not os.path.isabs(history_file):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        history_file = os.path.join(project_root, history_file)

    # Ensure directory exists
    os.makedirs(os.path.dirname(history_file), exist_ok=True)

    history = load_quiz_history()
    history.append({
        "score": score,
        "total": total,
        "subject": subject,
        "percentage": round((score / total) * 100, 1) if total > 0 else 0,
        "timestamp": datetime.now().isoformat(),
    })

    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)


def load_quiz_history() -> list:
    """
    Load quiz history from the JSON file.

    Returns:
        List of quiz result dicts. Empty list if file doesn't exist.
    """
    history_file = os.getenv("QUIZ_HISTORY_FILE", "./data/quiz_history.json")

    if not os.path.isabs(history_file):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        history_file = os.path.join(project_root, history_file)

    if not os.path.exists(history_file):
        return []

    try:
        with open(history_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, IOError):
        return []
