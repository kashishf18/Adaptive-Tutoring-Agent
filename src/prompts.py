CHAT_TEMPLATE = """[INST] <<SYS>>
You are a friendly {subject} tutor. Your tone should be: {mood_tone}.
Keep answers clear, structured, and encouraging.
<</SYS>>
{user_message} [/INST]"""

QUIZ_TEMPLATE = """[INST] Generate exactly 10 multiple-choice questions about {subject}.
Each question must have 4 options (A, B, C, D) and one correct answer.
Return ONLY valid JSON in this format:
[{{"question": "...", "options": ["A","B","C","D"], "correct_index": 0}}]
[/INST]"""

FEEDBACK_TEMPLATE = """[INST] A student scored {score} out of 10 on a {subject} quiz.
Give 3-4 sentences of adaptive feedback. If score >= 7, be celebratory.
If 5-6, be encouraging. If < 5, be supportive and suggest revision tips. [/INST]"""
