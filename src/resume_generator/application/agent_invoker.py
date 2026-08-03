from resume_generator.application.port_selector import llm_agent
from resume_generator.application.prompt_generator import PromptGenerator
from resume_generator.domains.agent_responses import (
    EducationResponse,
    ExperienceResponse,
    ProjectResponse,
)


class AgentInvoker:
    def __init__(self, prompt_generator: PromptGenerator) -> None:
        self.agent = llm_agent()
        self.prompt_generator = prompt_generator

    def get_user_experience_summary(self) -> ExperienceResponse:
        prompt = self.prompt_generator.get_llm_prompt_work()
        model = self.agent.with_structured_output(ExperienceResponse)
        response = model.invoke(prompt)
        if type(response) == ExperienceResponse:
            return response
        raise RuntimeError(
            "Experience response from LLM Doesn't match format: ", response
        )

    def get_user_projects_summary(self) -> ProjectResponse:
        prompt = self.prompt_generator.get_llm_prompt_projects()
        model = self.agent.with_structured_output(ProjectResponse)
        response = model.invoke(prompt)
        if type(response) == ProjectResponse:
            return response
        raise RuntimeError("Project response from LLM Doesn't match format: ", response)

    def get_user_education_summary(self) -> EducationResponse:
        prompt = self.prompt_generator.get_llm_prompt_education()
        model = self.agent.with_structured_output(EducationResponse)
        response = model.invoke(prompt)
        if type(response) == EducationResponse:
            return response
        raise RuntimeError(
            "Education response from LLM Doesn't match format: ", response
        )
