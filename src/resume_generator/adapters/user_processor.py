import json
import logging
from pathlib import Path

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

    def get_user_education(self) -> dict:
        """
        Split skills by header (category) and turn them into list
        """
        education_file = self.data_dir / self.education_file
        if not education_file.exists():
            logger.error(f"Education file not found: {education_file}")
            raise FileNotFoundError(f"Education file not found: {education_file}")
        content = education_file.read_text(encoding="utf-8")
        return json.loads(content)

    def get_user_experience(self) -> str:
        experience_dir = self.data_dir / self.experience_dir
        if not experience_dir.exists() or not experience_dir.is_dir():
            logger.error(f"Experience directory not found: {experience_dir}")
            raise FileNotFoundError(f"Experience directory not found: {experience_dir}")
        experience = ""
        for exp_file in experience_dir.glob("*.md"):
            content = exp_file.read_text(encoding="utf-8")
            experience += content
            experience += "\n=====================\n"  # Separator between experiences

        return experience

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
