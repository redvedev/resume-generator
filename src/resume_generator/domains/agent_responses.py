from pydantic import BaseModel


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
