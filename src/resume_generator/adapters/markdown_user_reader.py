import json
import logging
from pathlib import Path

from langchain_text_splitters import MarkdownHeaderTextSplitter
from pydantic import ConfigDict

from resume_generator.domains.education import Education
from resume_generator.domains.experience import Experience
from resume_generator.domains.personal_info import PersonalInfo
from resume_generator.domains.project import Project, ProjectType
from resume_generator.domains.skills import Skills
from resume_generator.domains.user import User
from resume_generator.ports.user_processor import UserDataReader

logger = logging.getLogger(__name__)


class MarkdownUserReader(UserDataReader):
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.personal_data_file = "personal.md"
        self.skills_file = "skills.md"
        self.education_file = "education.md"
        self.projects_dir = "projects"
        self.experience_dir = "experience"

        self.splitting_headers = [("#", "H1"), ("##", "H2"), ("###", "H3")]
        self.splitter = MarkdownHeaderTextSplitter(self.splitting_headers)

    def _get_user_personal_info(self) -> PersonalInfo:
        personal_file = self.data_dir / self.personal_data_file
        if not personal_file.exists():
            raise FileNotFoundError(f"Personal data file not found: {personal_file}")
        content = personal_file.read_text(encoding="utf-8")
        splitted = self.splitter.split_text(content)
        cleared_metadata = {
            el.metadata[self.splitting_headers[1][1]]: format_lists(el.page_content)
            for el in splitted
            if self.splitting_headers[1][1] in el.metadata
        }
        return PersonalInfo.model_validate(cleared_metadata)

    def _get_user_skills(self) -> list[Skills]:
        """
        Implementation of skills file parser. Markdown to json
        """
        skills_file = self.data_dir / self.skills_file
        if not skills_file.exists():
            raise FileNotFoundError(f"Skills file not found: {skills_file}")
        splitted = self.splitter.split_text(skills_file.read_text(encoding="utf-8"))
        cleared_metadata = [
            {
                "category": el.metadata[self.splitting_headers[1][1]],
                "skills": format_lists(el.page_content),
            }
            for el in splitted
            if self.splitting_headers[1][1] in el.metadata
        ]
        result = []
        for skill in cleared_metadata:
            result.append(Skills.model_validate(skill))
        return result

    def _get_user_education(self) -> list[Education]:
        """
        Split skills by header (category) and turn them into list
        """
        education_file = self.data_dir / self.education_file
        if not education_file.exists():
            raise FileNotFoundError(f"Education file not found: {education_file}")
        file_text = education_file.read_text(encoding="utf-8")
        splitted = self.splitter.split_text(file_text)

        schools = dict()
        for s in splitted:
            title = s.metadata[self.splitting_headers[0][1]]
            field_name = s.metadata[self.splitting_headers[1][1]]
            field_value = s.page_content
            if title not in schools:
                schools[title] = dict()
            schools[title][field_name] = format_lists(field_value)

        result = []
        for school in schools.values():
            result.append(Education.model_validate(school))
        return result

    def _get_user_experience(self) -> list[Experience]:
        experience_dir = self.data_dir / self.experience_dir
        if not experience_dir.exists() or not experience_dir.is_dir():
            raise FileNotFoundError(f"Experience directory not found: {experience_dir}")
        result = []
        for exp_file in experience_dir.glob("*.md"):
            work = exp_file.read_text(encoding="utf-8")
            splitted = self.splitter.split_text(work)
            cleared_metadata = {
                el.metadata[self.splitting_headers[1][1]]: format_lists(el.page_content)
                for el in splitted
                if self.splitting_headers[1][1] in el.metadata
            }
            cleared_metadata["company"] = splitted[0].metadata[
                self.splitting_headers[0][1]
            ]
            result.append(Experience.model_validate(cleared_metadata))

        return result

    def _get_user_projects(self) -> list[Project]:
        projects_dir = self.data_dir / self.projects_dir
        if not projects_dir.exists() or not projects_dir.is_dir():
            raise FileNotFoundError(f"Projects directory not found: {projects_dir}")
        result = []
        for project_file in projects_dir.glob("*.md"):
            proj = project_file.read_text(encoding="utf-8")
            splitted = self.splitter.split_text(proj)
            cleared_metadata = {
                el.metadata[self.splitting_headers[1][1]]: format_lists(el.page_content)
                for el in splitted
                if self.splitting_headers[1][1] in el.metadata
            }
            if "description" not in cleared_metadata:
                description = [
                    s
                    for s in splitted
                    if self.splitting_headers[1][1] not in s.metadata
                ]
                if len(description) == 0:
                    raise Exception(f"File {project_file} has empty description")
                cleared_metadata["description"] = description[0].page_content

            project_header = splitted[0].metadata[self.splitting_headers[0][1]]
            for header, value in zip(
                ["name", "project type", "year"], project_header.split(", ")
            ):
                cleared_metadata[header] = value
            cleared_metadata["project type"] = cleared_metadata["project type"][
                : len(cleared_metadata["project type"]) - len(" project")
            ]
            try:
                result.append(Project.model_validate(cleared_metadata))
            except Exception as e:
                logger.error(f"Error parsing project file {project_file}: {e}")
                raise (e)
        return result

    def read_user(self) -> User:
        return User(
            personal_info=self._get_user_personal_info(),
            education=self._get_user_education(),
            experience=self._get_user_experience(),
            projects=self._get_user_projects(),
            skills=self._get_user_skills(),
        )


def format_lists(text: str):
    if text[0] != "-":
        # Not a markdown list, abort
        return text
    text = text[2:]  # Skip first "- "
    return text.split("\n- ")
