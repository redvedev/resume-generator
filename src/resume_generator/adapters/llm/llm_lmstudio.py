from src.ports.llm import LLMInterface
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
        logger.info(f"LLM PROMPT: {prompt}")
        response = self.llm.respond(prompt).content
        logger.info(f"LLM RESPONSE: {response}")
        return parse_llm_response_to_json(response)


def parse_llm_response_to_json(llm_response: str) -> dict:
    """
    Parse the LLM response string into a JSON object.

    Args:
        llm_response (str): The LLM response string.

    Returns:
        dict: The parsed JSON object.
    """
    match = re.search(r'\{.*\}', llm_response, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            data = json.loads(json_str)
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            logger.debug(f"LLM response that failed to decode: {llm_response}")
            raise ValueError(f"Failed to decode JSON: {e}")