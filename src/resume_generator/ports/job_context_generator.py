from abc import ABC, abstractmethod

from resume_generator.domains.user import User


class JobContextGenerator(ABC):
    def __init__(self, job_description: str, user: User):
        self.job_description = job_description
        self.user = user
        self.user = self._filter_user_info()

    @abstractmethod
    def generate_job_keywords(self) -> list[str]:
        """
        Generate job keywords based on the provided job description.

        Args:
            job_description (str): The job description text.

        Returns:
            dict: A dictionary containing the generated job keywords.
        """
        pass

    @abstractmethod
    def get_llm_prompt_work(self) -> str:
        pass

    @abstractmethod
    def get_llm_prompt_education(self) -> str:
        pass

    @abstractmethod
    def get_llm_prompt_projects(self) -> str:
        pass

    @abstractmethod
    def _filter_user_info(self) -> User:
        pass
