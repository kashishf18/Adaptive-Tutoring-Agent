import os
import google.generativeai as genai

class LLMEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not set in environment!")
        
        genai.configure(api_key=api_key)
        
        # Use gemini-2.5-flash which is very fast and has a free tier
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7, stop=None) -> str:
        try:
            config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                stop_sequences=stop if stop else []
            )
            response = self.model.generate_content(
                prompt,
                generation_config=config
            )
            return response.text.strip()
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {e}")