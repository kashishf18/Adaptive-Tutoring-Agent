import os
import google.generativeai as genai

class LLMEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not set in environment!")
        
        genai.configure(api_key=api_key)
        
        # Use gemini-1.5-flash which is very fast and has a free tier
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def generate(
        self,
        prompt: str,
        max_tokens: int = None,
        temperature: float = 0.7,
        stop: list = None
    ) -> str:
        
        # Gemini handles max_tokens and temperature via generation_config
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens or 2048,
            stop_sequences=stop
        )
        
        response = self.model.generate_content(
            prompt,
            generation_config=generation_config
        )
        return response.text.strip()