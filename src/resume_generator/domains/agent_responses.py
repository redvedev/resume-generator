from pydantic import BaseModel


class ExperienceSummary(BaseModel):
    job_id: int
    bullets: list[str]


class ExperienceResponse(BaseModel):
    jobs: list[ExperienceSummary]


class ProjectSummary(BaseModel):
    project_id: int
    description: str
    bullets: list[str]


class ProjectResponse(BaseModel):
    projects: list[ProjectSummary]


class EducationSummary(BaseModel):
    school_id: int
    courses: list[str]


class EducationResponse(BaseModel):
    schools: list[EducationSummary]
