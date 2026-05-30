

# ── Chat Prompt ──────────────────────────────────────────────
CHAT_TEMPLATE = """You are a friendly and knowledgeable {subject} tutor.
Your response should be clear, well‑structured, and encouraging.
If the student seems confused, use simple language and short steps.

Student's question: {user_message}"""

# ── Quiz Prompt ──────────────────────────────────────────────
QUIZ_TEMPLATE = """Generate exactly {num_questions} multiple-choice questions about {subject}.

Rules:
- Each question must have exactly 4 answer options
- Only one option is correct
- correct_index must be an integer between 0 and 3 (0=first option, 3=last)
- complexity must be one of: "Easy", "Medium", "Hard"
- explanation must be a brief explanation of why the answer is correct
- Return ONLY a valid JSON array — no explanation outside of JSON, no markdown, no code fences

Required JSON format:
[
  {{
    "question": "Your question here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_index": 0,
    "complexity": "Medium",
    "explanation": "Because X is Y."
  }}
]"""

# ── Feedback Prompt ──────────────────────────────────────────
FEEDBACK_TEMPLATE = """A student just completed a {subject} quiz and scored {score} out of {total}.

Write 3 to 4 sentences of personalized feedback:
- If score is 70% or above: be celebratory and suggest an advanced next topic
- If score is 50-69%: be encouraging, highlight what they likely got right, suggest review areas
- If score is below 50%: be warm and supportive, give 2 specific revision tips for {subject}

Do not repeat the score back to the student. Write naturally."""

# ── Prompt Builder Functions ──────────────────────────────────

def build_chat_prompt(subject: str, user_message: str, context: str = "") -> str:
    prompt = CHAT_TEMPLATE.format(
        subject=subject,
        user_message=user_message
    )
    if context and context.strip():
        prompt = f"Use this additional context to help answer:\n{context}\n\n{prompt}"
    return prompt

def build_quiz_prompt(subject: str, num_questions: int = 5) -> str:
    return QUIZ_TEMPLATE.format(subject=subject, num_questions=num_questions)

def build_feedback_prompt(subject: str, score: int, total: int = 10) -> str:
    return FEEDBACK_TEMPLATE.format(subject=subject, score=score, total=total)