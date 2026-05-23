"""
Quick smoke test to verify the LLaMA 2 model loads and generates output.
"""
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def test_model():
    """Load the model and generate a short test output."""
    from llama_cpp import Llama

    model_path = os.getenv("MODEL_PATH", "./models/llama-2-7b-chat.Q4_K_M.gguf")
    n_threads = int(os.getenv("N_THREADS", "4"))
    context_length = int(os.getenv("CONTEXT_LENGTH", "2048"))

    # Resolve relative path
    if not os.path.isabs(model_path):
        model_path = os.path.join(os.path.dirname(__file__), "..", model_path)

    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        print("   Run 'python scripts/download_model.py' first.")
        sys.exit(1)

    print(f"🔄 Loading model from: {model_path}")
    print(f"   Threads: {n_threads} | Context: {context_length}")

    start = time.time()
    llm = Llama(
        model_path=model_path,
        n_ctx=context_length,
        n_threads=n_threads,
        verbose=False,
    )
    load_time = time.time() - start
    print(f"   Loaded in {load_time:.1f}s")

    # Generate a short test response
    test_prompt = "[INST] Say hello in exactly 10 words. [/INST]"
    print(f"\n📝 Test prompt: {test_prompt}")

    start = time.time()
    output = llm(test_prompt, max_tokens=50, stop=["\n"])
    gen_time = time.time() - start

    response = output["choices"][0]["text"].strip()
    print(f"🤖 Response: {response}")
    print(f"   Generated in {gen_time:.1f}s")

    # Assertions
    assert response, "Response should not be empty"
    assert len(response) > 0, "Response should have content"

    print(f"\n✅ Model loaded and verified successfully!")
    print(f"   Total time: {load_time + gen_time:.1f}s")


if __name__ == "__main__":
    test_model()
