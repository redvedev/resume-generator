from pydantic import BaseModel, Field


class Skills(BaseModel):
    skills_category: str = Field(alias="category")
    skills: list[str] = Field(alias="skills")
