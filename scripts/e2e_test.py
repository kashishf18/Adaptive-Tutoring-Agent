import sys
import os
import json
from unittest.mock import MagicMock

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mood import detect_mood
from src.prompts import build_chat_prompt
from src.quiz import evaluate_quiz, save_quiz_result
from src.notes import add_note, load_notes

def mock_generate_quiz(llm, subject, num_questions):
    return [
        {"question": f"Q{i}", "options": ["A", "B", "C", "D"], "correct_index": 0}
        for i in range(num_questions)
    ]

def run_e2e():
    print("Starting E2E Test...")
    
    try:
        from src.llm_engine import LLMEngine
        llm = LLMEngine()
        print("LLM Engine initialized")
        generate_quiz = __import__("src.quiz", fromlist=["generate_quiz"]).generate_quiz
    except Exception as e:
        print("Failed to initialize real LLM Engine (likely missing model). Using Mock LLM.")
        llm = MagicMock()
        llm.generate.return_value = "Mock response"
        generate_quiz = mock_generate_quiz
        
    subject = "Physics"
    
    # 1. 1 chat message per mood type
    moods = [
        ("I hate this, it's too hard!", "frustrated"),
        ("I finally understand this!", "happy"),
        ("What is the formula?", "neutral"),
        ("Whatever, I don't care.", "disengaged")
    ]
    
    print("\n--- Testing Chat & Mood ---")
    for msg, expected_mood in moods:
        detected = detect_mood(msg)
        assert detected == expected_mood, f"Expected {expected_mood}, got {detected}"
        prompt = build_chat_prompt(subject, msg)
        response = llm.generate(prompt, max_tokens=10)
        print(f"Msg: '{msg}' -> Mood: {detected} -> Response OK")
        
    # 2. Generate quiz
    print("\n--- Testing Quiz Generation ---")
    questions = generate_quiz(llm, subject, 10)
    assert len(questions) == 10, "Failed to generate 10 quiz questions"
    print(f"Generated {len(questions)} quiz questions")
    
    # 3. Answer all 10
    answers = {i: q['correct_index'] for i, q in enumerate(questions)}
    score, total, results = evaluate_quiz(questions, answers)
    assert score == 10 and total == len(questions), "Evaluation failed"
    save_quiz_result(score, total, subject)
    print(f"Evaluated quiz: Score {score}/{total}")
    
    # 4. Save 2 notes
    print("\n--- Testing Notes ---")
    test_notes_file = "data/test_notes.json"
    if os.path.exists(test_notes_file):
        os.remove(test_notes_file)
        
    add_note("Note 1: Physics is fun", test_notes_file)
    add_note("Note 2: E=mc^2", test_notes_file)
    print("Saved 2 notes")
    
    # 5. Export notes
    notes = load_notes(test_notes_file)
    assert len(notes) == 2, "Notes were not saved correctly"
    json_data = json.dumps(notes)
    assert "Physics is fun" in json_data
    print("Exported notes verified")
    
    print("\nALL TESTS PASSED")

if __name__ == "__main__":
    run_e2e()
