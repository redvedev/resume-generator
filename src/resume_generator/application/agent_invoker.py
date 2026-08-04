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
        logger.info("Experience input: ", experience)
        logger.info("Experience output: ", response)
        if type(response) == ExperienceResponse:
            return response
        raise RuntimeError(
            "Experience response from LLM Doesn't match format: ", response
        )

    def get_user_projects_summary(self, projects: list[Project]) -> ProjectResponse:
        prompt = self.prompt_generator.get_llm_prompt_projects(projects)
        model = self.agent.with_structured_output(ProjectResponse)
        response = model.invoke(prompt)
        logger.info("Projects input: ", projects)
        logger.info("Projects output: ", response)
        if type(response) == ProjectResponse:
            return response
        raise RuntimeError("Project response from LLM Doesn't match format: ", response)

    def get_user_education_summary(self, schools: list[Education]) -> EducationResponse:
        prompt = self.prompt_generator.get_llm_prompt_education(schools)
        model = self.agent.with_structured_output(EducationResponse)
        response = model.invoke(prompt)
        logger.info("Education input: ", schools)
        logger.info("Education output: ", response)
        if type(response) == EducationResponse:
            return response
        raise RuntimeError(
            "Education response from LLM Doesn't match format: ", response
        )
