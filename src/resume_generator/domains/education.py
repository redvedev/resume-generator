from pydantic import BaseModel


class Education(BaseModel):
    degree: str
    school_name: str
    date: str
    skills: list[str]
