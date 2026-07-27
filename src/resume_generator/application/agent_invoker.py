from pydantic import BaseModel

from resume_generator.application.port_selector import get_llm_agent
from resume_generator.application.prompt_generator import PromptGenerator


class BulletPointSummary(BaseModel):
    object_id: int
    bullets: list[str]


class EducationSummary(BaseModel):
    school_id: int
    courses: list[str]


class ExperienceResponse(BaseModel):
    jobs: list[BulletPointSummary]


class ProjectResponse(BaseModel):
    projects: list[BulletPointSummary]


class EducationResponse(BaseModel):
    schools: list[EducationSummary]


class AgentInvoker:
    def __init__(self, prompt_generator: PromptGenerator) -> None:
        self.agent = get_llm_agent()
        self.prompt_generator = prompt_generator

    def get_user_experience_summary(self):
        prompt = self.prompt_generator.get_llm_prompt_work()
        model = self.agent.with_structured_output(ExperienceResponse)
        return model.invoke(prompt)

    def get_user_projects_summary(self):
        prompt = self.prompt_generator.get_llm_prompt_projects()
        model = self.agent.with_structured_output(ProjectResponse)
        return model.invoke(prompt)

    def get_user_education_summary(self):
        prompt = self.prompt_generator.get_llm_prompt_education()
        model = self.agent.with_structured_output(EducationResponse)
        return model.invoke(prompt)
