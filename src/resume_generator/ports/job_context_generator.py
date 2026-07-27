from abc import ABC, abstractmethod

from resume_generator.ports.user_processor import UserProcessor


class JobContextGenerator(ABC):
    def __init__(self, job_description: str):
        self.job_description = job_description

    @abstractmethod
    def generate_job_keywords(self) -> dict:
        """
        Generate job keywords based on the provided job description.

        Args:
            job_description (str): The job description text.

        Returns:
            dict: A dictionary containing the generated job keywords.
        """
        pass

    @abstractmethod
    def get_llm_prompt(self, user_processor: UserProcessor) -> str:
        """
        Generate a prompt for the LLM based on the job description and user data.

        Args:
            job_description (str): The job description text.
            user_data (UserData): The user data to be used in the prompt.
        Returns:
            str: A string containing the generated prompt for the LLM.
        """
        pass

