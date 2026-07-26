from abc import ABC, abstractmethod
from pathlib import Path
from src.ports.user_processor import UserProcessor

class LatexHandler(ABC):
    @abstractmethod
    def generate_tex(self, user_data: UserProcessor, llm_response: dict) -> str:
        """
        Generate LaTeX code based on the given user data.

        Args:
            user_data (UserProcessor): The user data.

        Returns:
            str: The generated LaTeX code.
        """
        pass