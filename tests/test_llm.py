import pytest
from src.prompts import CHAT_TEMPLATE, QUIZ_TEMPLATE, FEEDBACK_TEMPLATE

def test_chat_template_formatting():
    """Test that chat template formats correctly and returns a non-empty string."""
    prompt = CHAT_TEMPLATE.format(subject="Math", mood_tone="enthusiastic", user_message="What is 2+2?")
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    assert "Math" in prompt
    assert "enthusiastic" in prompt
    assert "What is 2+2?" in prompt

def test_quiz_template_formatting():
    """Test that quiz template formats correctly and returns a non-empty string."""
    prompt = QUIZ_TEMPLATE.format(subject="History", num_questions=5)
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    assert "History" in prompt

def test_feedback_template_formatting():
    """Test that feedback template formats correctly and returns a non-empty string."""
    prompt = FEEDBACK_TEMPLATE.format(score=8, subject="Science", total=10)
    assert isinstance(prompt, str)
    assert len(prompt) > 0
    assert "8" in prompt
    assert "Science" in prompt
