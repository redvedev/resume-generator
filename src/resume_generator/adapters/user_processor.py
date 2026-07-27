import json
import logging
from pathlib import Path

from pydantic import ConfigDict

from resume_generator.domains.education import Education
from resume_generator.domains.experience import Experience
from resume_generator.domains.personal_info import PersonalInfo
from resume_generator.domains.project import Project, ProjectType
from resume_generator.domains.skills import Skills
from resume_generator.domains.user import User
from resume_generator.ports.user_processor import UserProcessor

logger = logging.getLogger(__name__)


class JsonUserProcessor(UserProcessor):
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.personal_data_file = "personal.json"
        self.skills_file = "skills.json"
        self.education_file = "education.json"
        self.projects_dir = "projects"
        self.experience_dir = "experience"

    def _get_user_personal_info(self) -> PersonalInfo:
        personal_file = self.data_dir / self.personal_data_file
        if not personal_file.exists():
            logger.error(f"Personal data file not found: {personal_file}")
            raise FileNotFoundError(f"Personal data file not found: {personal_file}")
        content = personal_file.read_text(encoding="utf-8")
        return PersonalInfo.model_validate_json(content)

    def _get_user_skills(self) -> list[Skills]:
        """
        Implementation of skills file parser. Markdown to json
        """
        skills_file = self.data_dir / self.skills_file
        if not skills_file.exists():
            raise FileNotFoundError(f"Skills file not found: {skills_file}")
        content = json.loads(skills_file.read_text(encoding="utf-8"))
        result = []
        for skill in content:
            result.append(Skills.model_validate_json(json.dumps(skill)))
        return result

    def _get_user_education(self) -> list[Education]:
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
            result.append(Education.model_validate_json(json.dumps(school)))
        return result

    def _get_user_experience(self) -> list[Experience]:
        experience_dir = self.data_dir / self.experience_dir
        if not experience_dir.exists() or not experience_dir.is_dir():
            logger.error(f"Experience directory not found: {experience_dir}")
            raise FileNotFoundError(f"Experience directory not found: {experience_dir}")
        result = []
        for exp_file in experience_dir.glob("*.json"):
            work = exp_file.read_text(encoding="utf-8")
            result.append(Experience.model_validate_json(work))

        return result

    def _get_user_projects(self) -> list[Project]:
        projects_dir = self.data_dir / self.projects_dir
        if not projects_dir.exists() or not projects_dir.is_dir():
            logger.error(f"Projects directory not found: {projects_dir}")
            raise FileNotFoundError(f"Projects directory not found: {projects_dir}")
        result = []
        for project_file in projects_dir.glob("*.json"):
            result.append(
                Project.model_validate_json(project_file.read_text(encoding="utf-8"))
            )

        return result

    def read_user(self) -> User:
        return User(
            personal_info=self._get_user_personal_info(),
            education=self._get_user_education(),
            experience=self._get_user_experience(),
            projects=self._get_user_projects(),
            skills=self._get_user_skills(),
        )
