import logging

from resume_generator.application.port_selector import llm_agent
from resume_generator.application.prompt_generator import PromptGenerator
from resume_generator.domains.agent_responses import (
    EducationResponse,
    ExperienceResponse,
    ProjectResponse,
)
from resume_generator.domains.education import Education
from resume_generator.domains.experience import Experience
from resume_generator.domains.project import Project
from resume_generator.domains.user import User

logger = logging.getLogger(__name__)


class AgentInvoker:
    def __init__(self, prompt_generator: PromptGenerator) -> None:
        self.agent = llm_agent()
        self.prompt_generator = prompt_generator

    def get_user_experience_summary(
        self, experience: list[Experience]
    ) -> ExperienceResponse:
        prompt = self.prompt_generator.get_llm_prompt_work(experience)
        model = self.agent.with_structured_output(ExperienceResponse)
        response = model.invoke(prompt)
        logger.info(f"Experience input: {experience}")
        logger.info(f"Experience output: {response}")
        if type(response) == ExperienceResponse:
            return response
        raise RuntimeError(
            "Experience response from LLM Doesn't match format: ", response
        )

    def get_user_projects_summary(self, projects: list[Project]) -> ProjectResponse:
        prompt = self.prompt_generator.get_llm_prompt_projects(projects)
        model = self.agent.with_structured_output(ProjectResponse)
        response = model.invoke(prompt)
        logger.info(f"Projects input: {projects}")
        logger.info(f"Projects output: {response}")
        if type(response) == ProjectResponse:
            return response
        raise RuntimeError("Project response from LLM Doesn't match format: ", response)

    def filter_user_data(self, user: User) -> User:
        prompt = self.prompt_generator.select_user_facts(user)
        model = self.agent.with_structured_output(User)
        response = model.invoke(prompt)
        logger.info(f"User input: {user}")
        logger.info(f"User output: {response}")
        if type(response) == User:
            return response
        raise RuntimeError("User response from LLM Doesn't match format: ", response)
