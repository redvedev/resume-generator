from itertools import count
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field


class Education(BaseModel):
    _id_counter: ClassVar[count] = count(1)
    school_id: int = Field(default_factory=lambda: next(Education._id_counter))
    degree: str = Field(alias="degree")
    school_name: str = Field(alias="school name")
    dates: str = Field(alias="date")
    skills: list[str] = Field(alias="skills")
