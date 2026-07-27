from pydantic import BaseModel, ConfigDict, Field


class Experience(BaseModel):
    company: str = Field(alias="company")
    position: str = Field(alias="position")
    dates: str = Field(alias="date")
    location: str = Field(alias="location")
    summary: str = Field(alias="summary")
    achievements: list[str] = Field(alias="achievements")
    technologies: list[str] = Field(alias="technologies")
    impact: list[str] = Field(alias="impact")
