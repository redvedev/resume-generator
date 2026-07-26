import json
import logging
from pathlib import Path

from resume_generator.domains.education import Education
from resume_generator.domains.experience import Experience
from resume_generator.ports.user_processor import UserProcessor

logger = logging.getLogger(__name__)


class UserProcessorImpl(UserProcessor):
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.personal_data_file = "personal.json"
        self.skills_file = "skills.json"
        self.education_file = "education.json"
        self.projects_dir = "projects"
        self.experience_dir = "experience"

    def get_user_personal_info(self) -> dict:
        personal_file = self.data_dir / self.personal_data_file
        if not personal_file.exists():
            logger.error(f"Personal data file not found: {personal_file}")
            raise FileNotFoundError(f"Personal data file not found: {personal_file}")
        content = personal_file.read_text(encoding="utf-8")
        return json.loads(content)

    def get_user_skills(self) -> dict:
        """
        Implementation of skills file parser. Markdown to json
        """
        skills_file = self.data_dir / self.skills_file
        if not skills_file.exists():
            raise FileNotFoundError(f"Skills file not found: {skills_file}")
        content = skills_file.read_text(encoding="utf-8")
        return json.loads(content)

    def get_user_education(self) -> list[Education]:
        """
        Split skills by header (category) and turn them into list
        """
        education_file = self.data_dir / self.education_file
        if not education_file.exists():
            logger.error(f"Education file not found: {education_file}")
            raise FileNotFoundError(f"Education file not found: {education_file}")
        content = json.loads(education_file.read_text(encoding="utf-8"))
        result = []
        for school in content:
            result.append(
                Education(
                    degree=school.get("degree"),
                    school_name=school.get("school"),
                    date=school.get("date"),
                    skills=school.get("relevant courses"),
                )
            )
        return result

    def get_user_experience(self) -> list[Experience]:
        experience_dir = self.data_dir / self.experience_dir
        if not experience_dir.exists() or not experience_dir.is_dir():
            logger.error(f"Experience directory not found: {experience_dir}")
            raise FileNotFoundError(f"Experience directory not found: {experience_dir}")
        result = []
        for exp_file in experience_dir.glob("*.json"):
            content = json.loads(exp_file.read_text(encoding="utf-8"))
            for work in content:
                result.append(
                    Experience(
                        company=work.get("company"),
                        position=work.get("position"),
                        dates=work.get("date"),
                        location=work.get("location"),
                        summary=work.get("context"),
                        achievements=work.get("achievements"),
                        technologies=work.get("technologies"),
                        impact=work.get("impact"),
                    )
                )

        return result

    def get_user_projects(self) -> str:
        projects_dir = self.data_dir / self.projects_dir
        if not projects_dir.exists() or not projects_dir.is_dir():
            logger.error(f"Projects directory not found: {projects_dir}")
            raise FileNotFoundError(f"Projects directory not found: {projects_dir}")
        projects = ""
        for project_file in projects_dir.glob("*.md"):
            content = project_file.read_text(encoding="utf-8")
            projects += content
            projects += "\n=====================\n"  # Separator between projects
        return projects
