# Adaptive Tutoring Agent

An AI-powered tutoring application that provides personalized learning experiences across various subjects. It features a mood-aware chat interface, adaptive quiz generation, and a notes management system.

## Feature Overview

1. **Study Chat**: A conversational interface powered by a local LLM. It detects user mood (frustrated, happy, neutral, disengaged) and adapts its tone accordingly.
2. **Quiz Module**: Generates subject-specific multiple-choice quizzes, evaluates answers, provides adaptive feedback, and tracks quiz history.
3. **Notes Management**: Allows users to save important chat responses or manually write notes, persist them locally, and export them as JSON.

## Prerequisites

- **Python 3.9+**
- **pip** package manager
- (Optional) **C++ compiler** if you want to build `llama-cpp-python` with hardware acceleration.

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd adaptive-tutoring-agent
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## .env Guide

Create a `.env` file in the root of the project to configure the application:

```ini
APP_TITLE="Adaptive Tutoring Agent"
MODEL_PATH="models/llama-2-7b-chat.gguf"
CONTEXT_LENGTH=2048
N_THREADS=4
MAX_TOKENS=512
NOTES_FILE="data/notes.json"
QUIZ_HISTORY_FILE="data/quiz_history.json"
```

## How to Download Model

By default, the application expects a Llama 2 7B Chat GGUF model.

1. Create a `models` directory:
   ```bash
   mkdir models
   ```
2. Download the model (e.g., from TheBloke on Hugging Face):
   ```bash
   wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf -O models/llama-2-7b-chat.gguf
   ```

## How to Run

Start the Streamlit application:

```bash
streamlit run src/app.py
```
