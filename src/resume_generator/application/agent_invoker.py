import logging

from resume_generator.application.port_selector import llm_agent
from resume_generator.application.prompt_generator import PromptGenerator
from resume_generator.domains.agent_responses import JobNotesResponse, UserFitResponse
from resume_generator.domains.user import (
    Education,
    Experience,
    PersonalInfo,
    Project,
    Skills,
    User,
)

logger = logging.getLogger(__name__)


class AgentInvoker:
    def __init__(self, prompt_generator: PromptGenerator) -> None:
        self.agent = llm_agent()
        self.prompt_generator = prompt_generator

    def prepare_user_model(self, job_description: str) -> User:
        prompt = self.prompt_generator.select_user_facts(job_description)
        model = self.agent.with_structured_output(User)
        response = model.invoke(prompt)
        logger.info(f"User output: {response}")
        if type(response) == User:
            return response
        raise RuntimeError("User response from LLM Doesn't match format: ", response)

    def get_user_fit(self, job_description: str, user: User) -> float:
        prompt = self.prompt_generator.rate_user_fit(job_description)
        model = self.agent.with_structured_output(UserFitResponse)
        response = model.invoke(prompt)
        logger.info(f"Response: {response}")
        if type(response) == UserFitResponse:
            return response.fit_score
        raise RuntimeError(
            "User fit response from LLM Doesn't match format: ", response
        )

    def prepare_job_notes(self, job_description: str, user: User) -> str:
        prompt = self.prompt_generator.get_job_notes(job_description, user)
        model = self.agent.with_structured_output(JobNotesResponse)
        response = model.invoke(prompt)
        logger.info(f"Response: {response}")
        if type(response) == JobNotesResponse:
            return response.notes
        raise RuntimeError
