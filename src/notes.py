import json
import os
import datetime

def load_notes(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_notes(notes, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4)

def add_note(content, file_path):
    notes = load_notes(file_path)
    notes.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "content": content
    })
    save_notes(notes, file_path)

def delete_note(index, file_path):
    notes = load_notes(file_path)
    if 0 <= index < len(notes):
        notes.pop(index)
        save_notes(notes, file_path)
