from src.mood import detect_mood

def test_detect_mood_frustrated():
    assert detect_mood("I am stuck and don't get it at all.") == "frustrated"
    assert detect_mood("This makes no sense, I give up.") == "frustrated"
    assert detect_mood("ugh, this is too hard and I'm tired") == "frustrated"

def test_detect_mood_happy():
    assert detect_mood("yay! I finally got it!") == "happy"
    assert detect_mood("this is fun and amazing") == "happy"
    assert detect_mood("yes! it makes sense now, easy!") == "happy"

def test_detect_mood_disengaged():
    assert detect_mood("whatever, I don't care") == "disengaged"
    assert detect_mood("this is boring, let's skip it") == "disengaged"

def test_detect_mood_neutral():
    assert detect_mood("what is the capital of France?") == "neutral"
    assert detect_mood("please explain the pythagorean theorem.") == "neutral"
