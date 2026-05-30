import os
import google.generativeai as genai

class LLMEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not set in environment!")
        
        genai.configure(api_key=api_key)
        
        # Use gemini-2.0-flash which is stable and has a free tier
        self.model = genai.GenerativeModel(
            "gemini-2.0-flash",
            safety_settings={
                genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
                genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            }
        )

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

            # Handle cases where response has no valid parts
            if not response.candidates:
                raise RuntimeError("LLM returned no candidates")
            
            candidate = response.candidates[0]
            if candidate.finish_reason not in (1, "STOP", None):
                # Try to extract text anyway
                if candidate.content and candidate.content.parts:
                    return candidate.content.parts[0].text.strip()
                raise RuntimeError(
                    f"LLM generation blocked (finish_reason={candidate.finish_reason}). "
                    "Try rephrasing your question."
                )
            
            return response.text.strip()
        except RuntimeError:
            raise
        except Exception as e:
            raise RuntimeError(f"LLM generation failed: {e}")

    def generate_stream(self, prompt: str, max_tokens: int = 1024, temperature: float = 0.7, stop=None):
        try:
            config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                stop_sequences=stop if stop else []
            )
            response = self.model.generate_content(
                prompt,
                generation_config=config,
                stream=True
            )
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            raise RuntimeError(f"LLM streaming generation failed: {e}")