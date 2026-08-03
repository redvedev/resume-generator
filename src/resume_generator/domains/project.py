from enum import Enum
from itertools import count
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field


class ProjectType(Enum):
    WORK = "Work"
    ACADEMIC = "Academic"
    PERSONAL = "Personal"


class Project(BaseModel):
    _id_counter: ClassVar[count] = count(1)
    project_id: int = Field(default_factory=lambda: next(Project._id_counter))
    name: str = Field(alias="name")
    type: ProjectType = Field(alias="project type")
    year: str = Field(alias="year")
    technologies: list[str] = Field(alias="technologies")
    metrics: list[str] = Field(alias="metrices")
    description: str = Field(alias="description")
    outcome: list[str] = Field(alias="outcome")
    actions: list[str] = Field(alias="actions", default=[])
