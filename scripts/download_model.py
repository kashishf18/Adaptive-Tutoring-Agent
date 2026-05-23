"""
Download the LLaMA 2 7B Chat GGUF model from HuggingFace Hub.
Reads configuration from .env file.
"""
import os
import sys

# Add parent directory to path so we can find .env
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def download_model():
    """Download the GGUF model file from HuggingFace Hub."""
    from huggingface_hub import hf_hub_download

    model_repo = os.getenv("MODEL_REPO", "TheBloke/Llama-2-7B-Chat-GGUF")
    model_filename = os.getenv("MODEL_FILENAME", "llama-2-7b-chat.Q4_K_M.gguf")
    model_path = os.getenv("MODEL_PATH", "./models/llama-2-7b-chat.Q4_K_M.gguf")

    # Ensure models directory exists
    models_dir = os.path.dirname(model_path)
    os.makedirs(models_dir, exist_ok=True)

    # Check if model already exists
    if os.path.exists(model_path):
        size_gb = os.path.getsize(model_path) / (1024 ** 3)
        print(f"[OK] Model already exists at: {model_path} ({size_gb:.2f} GB)")
        return model_path

    print(f"[DOWNLOAD] Downloading model from: {model_repo}")
    print(f"   File: {model_filename}")
    print(f"   Destination: {model_path}")
    print(f"   This may take a while (~4 GB download)...")
    print()

    try:
        downloaded_path = hf_hub_download(
            repo_id=model_repo,
            filename=model_filename,
            local_dir=models_dir,
        )

        # Verify the file exists at the expected path
        final_path = os.path.join(models_dir, model_filename)
        if os.path.exists(final_path):
            size_gb = os.path.getsize(final_path) / (1024 ** 3)
            print(f"\n[OK] Download complete!")
            print(f"   Path: {final_path}")
            print(f"   Size: {size_gb:.2f} GB")
            return final_path
        else:
            print(f"\n[OK] Download complete!")
            print(f"   Path: {downloaded_path}")
            size_gb = os.path.getsize(downloaded_path) / (1024 ** 3)
            print(f"   Size: {size_gb:.2f} GB")
            return downloaded_path

    except Exception as e:
        print(f"\n[ERROR] Download failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Check your internet connection")
        print("  2. Verify MODEL_REPO and MODEL_FILENAME in .env")
        print(f"  3. Ensure you have ~4 GB free disk space in '{models_dir}'")
        sys.exit(1)


if __name__ == "__main__":
    download_model()
