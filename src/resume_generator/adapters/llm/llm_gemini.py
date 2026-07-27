import logging
import os

from google import genai

from resume_generator.ports.llm import LLMInterface

logger = logging.getLogger(__name__)


class GeminiAdapter(LLMInterface):
    def __init__(self, llm_model: str):
        self.model = llm_model
        API_KEY = os.environ.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=API_KEY)

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response based on the given prompt using the underlying LLM.

        Args:
            prompt (str): The input prompt.

        Returns:
            str: The generated response.
        """
        logger.info(f"LLM PROMPT: {prompt}")

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        ).text
        logger.info(f"LLM RESPONSE: {response}")
        if response is None:
            raise RuntimeError("LLM response is None")
        return response
