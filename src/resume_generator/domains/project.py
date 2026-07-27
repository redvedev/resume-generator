from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class ProjectType(Enum):
    WORK = "Work"
    ACADEMIC = "Academic"
    PERSONAL = "Personal"


class Project(BaseModel):
    name: str = Field(alias="name")
    type: ProjectType = Field(alias="project type")
    year: str = Field(alias="year")
    technologies: list[str] = Field(alias="technologies")
    metrics: list[str] = Field(alias="metrices")
    description: str = Field(alias="description")
    outcome: list[str] = Field(alias="outcome")
