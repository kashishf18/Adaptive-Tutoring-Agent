"""
Mood Detection — Keyword-based emotional tone detection for student messages.

Detects four mood categories: frustrated, happy, confused, disengaged.
Maps each mood to an LLM tone instruction for adaptive responses.
"""

# Keyword dictionaries for mood detection
MOOD_KEYWORDS = {
    "frustrated": [
        "frustrated", "frustrating", "annoyed", "angry", "hate", "stupid",
        "dumb", "confused", "lost", "give up", "quit", "hopeless", "ugh",
        "terrible", "awful", "impossible", "cant", "can't", "don't get it",
        "makes no sense", "too hard", "difficult", "struggling", "stuck",
        "failing", "failed", "wrong", "mistake", "sucks", "irritating",
        "stressed", "overwhelmed", "tired of", "sick of", "fed up",
    ],
    "happy": [
        "happy", "excited", "great", "awesome", "amazing", "love",
        "wonderful", "fantastic", "excellent", "brilliant", "got it",
        "understand", "makes sense", "finally", "eureka", "yes",
        "cool", "perfect", "thanks", "thank you", "helpful", "wow",
        "interesting", "fascinating", "fun", "enjoy", "learned",
        "clicked", "easy", "clear", "nice", "good", "yay",
    ],
    "confused": [
        "confused", "confusing", "what", "how", "why", "huh",
        "don't understand", "unclear", "not sure", "explain",
        "clarify", "what do you mean", "lost", "complicated",
        "complex", "elaborate", "break it down", "simplify",
        "what is", "define", "meaning", "difference between",
        "help me understand", "i think", "maybe", "sort of",
    ],
    "disengaged": [
        "bored", "boring", "whatever", "idc", "don't care",
        "meh", "ok", "okay", "fine", "sure", "yeah", "hmm",
        "lol", "idk", "doesn't matter", "skip", "next",
        "k", "kk", "nvm", "nevermind", "anyway", "moving on",
    ],
}

# Tone instructions that get injected into the LLM system prompt
TONE_MAP = {
    "frustrated": (
        "The student seems frustrated. Use a calm, patient, and empathetic tone. "
        "Simplify your explanations. Break things into very small steps. "
        "Acknowledge their frustration and reassure them that struggling is a normal part of learning. "
        "Use phrases like 'I understand this can be tricky' and 'Let's take it step by step.'"
    ),
    "happy": (
        "The student is feeling positive and engaged! Match their energy with enthusiasm. "
        "Celebrate their understanding and progress. Use encouraging language like "
        "'Great job!' and 'You're really getting the hang of this!' "
        "You can introduce slightly more advanced concepts to keep their momentum going."
    ),
    "confused": (
        "The student seems confused and needs clarification. Be extra clear and structured. "
        "Use numbered steps, simple analogies, and concrete examples. "
        "Ask if they'd like you to explain from a different angle. "
        "Avoid jargon and technical language unless you define it first."
    ),
    "disengaged": (
        "The student seems disengaged or distracted. Try to re-spark their interest! "
        "Use fascinating real-world examples, fun facts, or surprising connections. "
        "Keep responses concise and punchy. Ask thought-provoking questions "
        "to draw them back into the conversation."
    ),
    "neutral": (
        "The student's mood is neutral. Use a friendly, professional teaching tone. "
        "Balance clarity with depth. Be conversational but focused. "
        "Provide thorough explanations with relevant examples."
    ),
}


def detect_mood(text: str) -> str:
    """
    Detect the emotional mood of a student's message using keyword matching.

    Scans the input text against keyword dictionaries for each mood category.
    Returns the category with the highest keyword match count.

    Args:
        text: The student's message text.

    Returns:
        One of: "frustrated", "happy", "confused", "disengaged", or "neutral".
    """
    if not text or not text.strip():
        return "neutral"

    text_lower = text.lower()
    scores = {}

    for mood, keywords in MOOD_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in text_lower)
        scores[mood] = score

    # Find the mood with the highest score
    max_score = max(scores.values())

    # If no keywords matched at all, return neutral
    if max_score == 0:
        return "neutral"

    # Return the mood with the highest match count
    best_mood = max(scores, key=scores.get)
    return best_mood


def get_tone(mood: str) -> str:
    """
    Get the LLM tone instruction string for a given mood.

    Args:
        mood: The detected mood category.

    Returns:
        A tone instruction string to inject into the LLM system prompt.
    """
    return TONE_MAP.get(mood, TONE_MAP["neutral"])


# Mood display configuration for the UI
MOOD_DISPLAY = {
    "frustrated": {"emoji": "😤", "color": "#FF6B6B", "label": "Frustrated"},
    "happy": {"emoji": "😊", "color": "#51CF66", "label": "Happy"},
    "confused": {"emoji": "🤔", "color": "#FFD43B", "label": "Confused"},
    "disengaged": {"emoji": "😐", "color": "#868E96", "label": "Disengaged"},
    "neutral": {"emoji": "🙂", "color": "#74C0FC", "label": "Neutral"},
}
