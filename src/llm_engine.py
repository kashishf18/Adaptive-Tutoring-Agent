import os
from llama_cpp import Llama

class LLMEngine:
    def __init__(self):
        model_path = os.getenv("MODEL_PATH", "models/llama-2-7b-chat.gguf")
        context_length = int(os.getenv("CONTEXT_LENGTH", "2048"))
        n_threads = int(os.getenv("N_THREADS", "4"))
        
        self.max_tokens = int(os.getenv("MAX_TOKENS", "512"))
        
        self.llm = Llama(
            model_path=model_path,
            n_ctx=context_length,
            n_threads=n_threads,
            verbose=False
        )
        
    def generate(self, prompt: str) -> str:
        response = self.llm(
            prompt,
            max_tokens=self.max_tokens,
            echo=False
        )
        return response['choices'][0]['text'].strip()
