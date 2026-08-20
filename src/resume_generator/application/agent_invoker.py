import logging

from langchain_core.language_models import LanguageModelInput
from langchain_core.runnables import Runnable
from pydantic import BaseModel

from resume_generator.application.port_selector import llm_agent
from resume_generator.application.prompt_generator import PromptGenerator
from resume_generator.domains.agent_responses import JobNotesResponse, UserFitResponse
from resume_generator.domains.requirement_models import (
    RequirementAnalysis,
    ResumeValidation,
)
from resume_generator.domains.user import User

logger = logging.getLogger(__name__)


class AgentInvoker:
    def __init__(self, prompt_generator: PromptGenerator) -> None:
        self.agent = llm_agent()
        self.prompt_generator = prompt_generator

    def model_invoke(self, output_type: type[BaseModel], prompt: str):
        logger.info(f"Invoking model with prompt: {prompt}")
        model = self.agent.with_structured_output(
            output_type, include_raw=True, method="json_schema"
        )
        response = model.invoke(prompt)
        usage_metadata = response["raw"].usage_metadata
        response = response["parsed"]
        logger.info(f"Model usage: {usage_metadata}")
        logger.info(f"Model response: {response}")
        return response

    def prepare_user_model(
        self,
        job_description: str,
        requirement_analysis: str | None = None,
        validation_feedback: str | None = None,
    ) -> User:
        prompt = self.prompt_generator.select_user_facts(
            job_description,
            requirement_analysis=requirement_analysis,
            validation_feedback=validation_feedback,
        )
        response = self.model_invoke(User, prompt)
        logger.info(f"User output: {response}")
        if type(response) == User:
            return response
        raise RuntimeError("User response from LLM Doesn't match format: ", response)

    def get_user_fit(self, job_description: str) -> float:
        prompt = self.prompt_generator.rate_user_fit(job_description)
        response = self.model_invoke(UserFitResponse, prompt)
        logger.info(f"Response: {response}")
        if type(response) == UserFitResponse:
            return response.fit_score
        raise RuntimeError(
            "User fit response from LLM Doesn't match format: ", response
        )

    def prepare_job_notes(self, job_description: str, user: User) -> str:
        prompt = self.prompt_generator.get_job_notes(job_description, user)
        response = self.model_invoke(JobNotesResponse, prompt)
        logger.info(f"Response: {response}")
        if type(response) == JobNotesResponse:
            return self._normalize_notes(response.notes)
        raise RuntimeError

    @staticmethod
    def _normalize_notes(notes: str) -> str:
        if "\\n" in notes:
            notes = notes.replace("\\n", "\n")
        if "\\t" in notes:
            notes = notes.replace("\\t", "\t")
        return notes

    def analyze_requirements(self, job_description: str) -> RequirementAnalysis:
        prompt = self.prompt_generator.analyze_job_requirements(job_description)
        response = self.model_invoke(RequirementAnalysis, prompt)
        logger.info(f"Requirement analysis: {response}")
        if isinstance(response, RequirementAnalysis):
            return response
        raise RuntimeError("Requirement analysis response is not valid")

    def validate_resume(
        self,
        job_description: str,
        user: User,
        requirement_analysis: RequirementAnalysis,
    ) -> ResumeValidation:
        prompt = self.prompt_generator.validate_resume(
            job_description=job_description,
            user=user,
            requirement_analysis=requirement_analysis.model_dump_json(indent=4),
        )
        response = self.model_invoke(ResumeValidation, prompt)
        logger.info(f"Resume validation: {response}")
        if isinstance(response, ResumeValidation):
            return response
        raise RuntimeError("Resume validation response is not valid")
