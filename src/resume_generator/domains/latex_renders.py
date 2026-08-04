from datetime import datetime

from pydantic import BaseModel


class LatexSkill(BaseModel):
    category: str
    skills: list[str]


class LatexSkills(BaseModel):
    skills: list[LatexSkill]


class LatexJob(BaseModel):
    position: str
    company: str
    location: str
    dates: str
    beginning_date: datetime
    bullet_points: list[str]


class LatexJobs(BaseModel):
    jobs: list[LatexJob]


class LatexSchool(BaseModel):
    name: str
    dates: str
    beginning_date: datetime
    courses: list[str]
    degree: str


class LatexSchools(BaseModel):
    schools: list[LatexSchool]


class LatexProject(BaseModel):
    name: str
    project_type: str
    description: str
    year: str
    technologies: list[str]
    bullet_points: list[str]


class LatexProjects(BaseModel):
    projects: list[LatexProject]
