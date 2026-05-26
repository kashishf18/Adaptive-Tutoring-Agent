from src.mood import detect_mood, TONE_MAP

CHAT_TEMPLATE = """[INST] <<SYS>>
You are a friendly {subject} tutor. Your tone should be: {mood_tone}.
Keep answers clear, structured, and encouraging.
{context_section}
<</SYS>>
{user_message} [/INST]"""

QUIZ_TEMPLATE = """[INST] Generate exactly {num_questions} multiple-choice questions about {topic} in the context of {subject}.
Each question must have 4 options (A, B, C, D) and one correct answer.
Return ONLY valid JSON in this format:
[{{"question": "...", "options": ["A","B","C","D"], "correct_index": 0}}]
[/INST]"""

FEEDBACK_TEMPLATE = """[INST] A student scored {score} out of 10 on a {subject} quiz.
Give 3-4 sentences of adaptive feedback. If score >= 7, be celebratory.
If 5-6, be encouraging. If < 5, be supportive and suggest revision tips. [/INST]"""

def build_chat_prompt(subject: str, user_message: str, context: str = "") -> str:
    mood = detect_mood(user_message)
    tone = TONE_MAP.get(mood, TONE_MAP["neutral"])
    
    context_section = ""
    if context.strip():
        context_section = f"\nUse the following textbook knowledge to answer the question:\n{context}\n"
        
    return CHAT_TEMPLATE.format(subject=subject, mood_tone=tone, context_section=context_section, user_message=user_message)

def build_quiz_prompt(subject: str, topic: str, num_questions: int) -> str:
    return QUIZ_TEMPLATE.format(subject=subject, topic=topic, num_questions=num_questions)

def build_feedback_prompt(score: int, subject: str) -> str:
    return FEEDBACK_TEMPLATE.format(score=score, subject=subject)
