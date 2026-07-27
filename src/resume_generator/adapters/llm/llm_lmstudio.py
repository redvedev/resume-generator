from src.resume_generator.ports.llm import LLMInterface
import lmstudio as lms
import json
import re
import logging

logger = logging.getLogger(__name__)


class LMStudioAdapter(LLMInterface):
    def __init__(self, llm_model: str):
        self.llm = lms.llm(llm_model)

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response based on the given prompt using the underlying LLM.

        Args:
            prompt (str): The input prompt.

        Returns:
            str: The generated response.
        """
        response = self.llm.respond(prompt).content
        return response
