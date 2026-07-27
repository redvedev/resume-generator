from abc import ABC, abstractmethod

from resume_generator.domains.user import User


class PromptGenerator(ABC):
    def __init__(self, job_description: str, user: User):
        self.job_description = job_description
        self.user = user

    @abstractmethod
    def get_llm_prompt_work(self) -> str:
        pass

    @abstractmethod
    def get_llm_prompt_education(self) -> str:
        pass

    @abstractmethod
    def get_llm_prompt_projects(self) -> str:
        pass
