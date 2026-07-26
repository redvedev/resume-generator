from pydantic import BaseModel, ConfigDict, Field


class Education(BaseModel):
    degree: str = Field(alias="degree")
    school_name: str = Field(alias="school name")
    date: str = Field(alias="date")
    skills: list[str] = Field(alias="important skills")
    irrelevant_skills: list[str] = Field(alias="general skills")
