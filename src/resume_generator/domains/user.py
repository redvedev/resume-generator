from pydantic import BaseModel

from resume_generator.domains.education import Education
from resume_generator.domains.experience import Experience
from resume_generator.domains.personal_info import PersonalInfo
from resume_generator.domains.project import Project
from resume_generator.domains.skills import Skills


class User(BaseModel):
    personal_info: PersonalInfo
    education: list[Education]
    experience: list[Experience]
    projects: list[Project]
    skills: list[Skills]
