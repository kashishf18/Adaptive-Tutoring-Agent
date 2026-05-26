MOOD_KEYWORDS = {
    "frustrated": ["stuck", "confused", "ugh", "don't get it", "i give up",
                   "makes no sense", "hate this", "tired", "hard"],
    "happy":      ["yay", "got it", "i love this", "this is fun", "amazing",
                   "finally", "yes!", "makes sense now", "easy"],
    "disengaged": ["whatever", "don't care", "boring", "idk", "meh", "skip"],
    "neutral":    []
}

TONE_MAP = {
    "frustrated":  "Use simple steps, short sentences, and be extra encouraging",
    "happy":       "Be celebratory, build on their momentum, suggest next challenge",
    "disengaged":  "Be very brief, practical, and use a motivational hook",
    "neutral":     "Be clear, structured, and direct"
}

def detect_mood(text: str) -> str:
    """
    Detect the emotional mood of a student's message using keyword matching.
    """
    if not text:
        return "neutral"
        
    text_lower = text.lower()
    best_mood = "neutral"
    highest_count = 0

    for mood, keywords in MOOD_KEYWORDS.items():
        if mood == "neutral":
            continue
        count = sum(1 for kw in keywords if kw in text_lower)
        if count > highest_count:
            highest_count = count
            best_mood = mood

    return best_mood
