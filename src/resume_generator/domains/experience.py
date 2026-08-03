from itertools import count
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field


class Experience(BaseModel):
    _id_counter: ClassVar[count] = count(1)
    job_id: int = Field(default_factory=lambda: next(Experience._id_counter))
    company: str = Field(alias="company")
    position: str = Field(alias="position")
    dates: str = Field(alias="date")
    location: str = Field(alias="location")
    summary: str = Field(alias="summary")
    achievements: list[str] = Field(alias="achievements")
    technologies: list[str] = Field(alias="technologies")
    impact: list[str] = Field(alias="impact")
