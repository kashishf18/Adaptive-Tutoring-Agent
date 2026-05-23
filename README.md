# Adaptive Tutoring Agent

An offline, cost-free, AI-powered study companion built on LLaMA 2 7B (GGUF quantized format) served via a Streamlit web interface.

## Features
- **Multi-turn Study Chat**: Conversational partner with mood-adaptive responses.
- **Quiz Generator**: Generates 10 multiple-choice questions per session and evaluates with adaptive feedback.
- **Persistent Notes**: Save chatbot answers and custom observations locally.
- **Subject Switcher**: Re-contextualizes tutor replies with domain-specific formatting.

## Tech Stack
- Streamlit (1.35.0)
- llama-cpp-python (0.3.4)
- python-dotenv (1.0.1)
- huggingface-hub (0.23.2)
- streamlit-chat (0.1.1)
- pydantic (2.7.1)
- regex (2024.5.15)
- LLaMA 2 7B Chat GGUF (`llama-2-7b-chat.Q4_K_M.gguf`)
