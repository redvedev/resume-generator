from pydantic import BaseModel


class Experience(BaseModel):
    company: str
    position: str
    dates: str
    location: str
    summary: str
    achievements: list[str]
    technologies: list[str]
    impact: list[str]
