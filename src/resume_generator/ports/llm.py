from abc import ABC, abstractmethod


class LLMInterface(ABC):
    def __init__(self, model_name: str):
        self.model_name = model_name

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        """
        Generate a response based on the given prompt.

        Args:
            prompt (str): The input prompt.

        Returns:
            str: The generated response.
        """
        pass

