import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time
import streamlit as st
from src.quiz import (
    generate_quiz,
    evaluate_quiz,
    save_quiz_result,
    load_quiz_history
)


from src.llm_engine import LLMEngine
from src.mood import detect_mood
from src.prompts import (
    build_chat_prompt,
    build_feedback_prompt,
    build_quiz_prompt,      
)

# 4.1 Create app.py with tab layout
st.set_page_config(page_title=os.getenv("APP_TITLE", "Adaptive Tutoring Agent"))
tab1, tab2, tab3 = st.tabs(["💬 Study Chat", "🧪 Quiz", "📝 Notes"])

# 4.2 Add subject dropdown in sidebar
subject = st.sidebar.selectbox("Subject", [
    "Physics", "Mathematics", "History",
    "Chemistry", "Biology", "Computer Science", "Literature"
])

# Initialize session state for notes
if "notes" not in st.session_state:
    st.session_state["notes"] = []

# 4.3 Implement chat history via st.session_state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

NOTES_FILE = os.getenv("NOTES_FILE", "data/notes.txt")

@st.cache_resource
def get_llm():
    return LLMEngine()

llm = get_llm()

with tab1:
    # Render existing chat history
    for i, msg in enumerate(st.session_state["messages"]):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant":
                # 4.5 Add mood badge display
                mood = msg.get("mood", "neutral")
                color_map = {"frustrated": "🔴", "happy": "🟢", "neutral": "🔵", "disengaged": "⚫"}
                color = color_map.get(mood, "🔵")
                st.caption(f"{color} {mood.capitalize()}")
                
                # 4.6 Add Save to Notes button
                if st.button("💾 Save", key=f"save_{i}"):
                    st.session_state["notes"].append(msg["content"])
                    os.makedirs(os.path.dirname(NOTES_FILE), exist_ok=True)
                    with open(NOTES_FILE, "a") as f:
                        f.write(msg["content"] + "\n\n")

    # 4.4 Wire chat input to LLM engine
    if prompt := st.chat_input("Ask a question..."):
        # Detect mood
        mood = detect_mood(prompt)
        timestamp = time.time()
        
        # Add user message to state
        st.session_state["messages"].append({
            "role": "user",
            "content": prompt,
            "mood": mood,
            "timestamp": timestamp
        })
        
        # Add assistant placeholder in state first, then rerun 
        # (This avoids duplicating standard streamlit chat message logic)
        full_prompt = build_chat_prompt(subject, prompt)
        
        with st.spinner("Thinking..."):
            response = llm.generate(full_prompt)
            
        st.session_state["messages"].append({
            "role": "assistant",
            "content": response,
            "mood": mood,
            "timestamp": time.time()
        })
        
        # Persist only the last 10 messages across reruns
        if len(st.session_state["messages"]) > 10:
            st.session_state["messages"] = st.session_state["messages"][-10:]
            
        st.rerun()

with tab2:

    st.header("🧪 Quiz Generator")

    quiz_subject = st.selectbox(
        "Choose Quiz Subject",
        [
            "Physics",
            "Mathematics",
            "History",
            "Chemistry",
            "Biology",
            "Computer Science",
            "Literature"
        ],
        key="quiz_subject"
    )

    if st.button("Generate Quiz"):

        with st.spinner("Generating quiz..."):

            quiz = generate_quiz(llm, quiz_subject)

            if quiz:

                st.session_state["quiz"] = quiz
                st.session_state["quiz_subject"] = quiz_subject

            else:

                st.error("Failed to generate quiz.")

    # Show quiz if available
    if "quiz" in st.session_state:

        quiz = st.session_state["quiz"]

        answers = {}

        st.markdown("---")

        for i, q in enumerate(quiz):

            st.progress((i + 1) / len(quiz))

            st.subheader(f"Q{i+1}. {q['question']}")

            selected = st.radio(
                "Select your answer:",
                options=range(len(q["options"])),
                format_func=lambda x: q["options"][x],
                key=f"quiz_{i}"
            )

            answers[i] = selected

        # Submit button
        if st.button("Submit Quiz"):

            score, total, results = evaluate_quiz(
                quiz,
                answers
            )

            st.success(f"🎯 Score: {score}/{total}")

            # Save result
            save_quiz_result(
                score,
                total,
                st.session_state["quiz_subject"]
            )

            # Performance badge
            if score >= 7:

                st.success("🟢 Excellent Performance")

            elif score >= 5:

                st.warning("🟡 Average Performance")

            else:

                st.error("🔴 Needs Improvement")

            # Adaptive AI feedback
            feedback_prompt = build_feedback_prompt(
                score,
                st.session_state["quiz_subject"]
            )

            with st.spinner("Generating adaptive feedback..."):

                feedback = llm.generate(
                    feedback_prompt,
                    max_tokens=300,
                    temperature=0.7
                )

            st.markdown("## 🤖 Adaptive Feedback")

            st.write(feedback)

            # Detailed results
            st.markdown("## 📋 Quiz Review")

            for idx, result in enumerate(results):

                if result["is_correct"]:

                    st.success(
                        f"Q{idx+1}: Correct ✅"
                    )

                else:

                    st.error(
                        f"Q{idx+1}: Incorrect ❌"
                    )

                    st.write(
                        f"Correct Answer: {result['correct_option']}"
                    )

    # Quiz history section
    st.markdown("---")

    st.subheader("📊 Recent Quiz History")

    history = load_quiz_history()

    if history:

        recent_history = history[-5:]

        st.table(recent_history)

    else:

        st.info("No quiz history available yet.")
