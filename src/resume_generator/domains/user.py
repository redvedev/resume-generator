from enum import Enum
from itertools import count
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field


class PersonalInfo(BaseModel):
    name: str = Field(alias="name")
    phone_number: str = Field(alias="phone")
    location: str = Field(alias="location")
    email: str = Field(alias="email")
    linkedin_preview_link: str = Field(alias="linkedin_preview")
    linkedin_actual_link: str = Field(alias="linkedin_url")
    website: str = Field(alias="website")
    summary: str = Field(alias="summary")


class Education(BaseModel):
    _id_counter: ClassVar[count] = count(1)
    degree: str = Field(alias="degree")
    school_name: str = Field(alias="school name")
    dates: str = Field(alias="date")
    skills: list[str] = Field(alias="skills")


class Experience(BaseModel):
    _id_counter: ClassVar[count] = count(1)
    company: str = Field(alias="company")
    position: str = Field(alias="position")
    dates: str = Field(alias="date")
    location: str = Field(alias="location")
    summary: str = Field(alias="summary")
    bullets: list[str] = Field(alias="bullets")


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
    description: str = Field(alias="description")
    bullets: list[str] = Field(alias="bullets")


class Skills(BaseModel):
    skills_category: str = Field(alias="category")
    skills: list[str] = Field(alias="skills")


class User(BaseModel):
    personal_info: PersonalInfo
    education: list[Education]
    experience: list[Experience]
    projects: list[Project]
    skills: list[Skills]
