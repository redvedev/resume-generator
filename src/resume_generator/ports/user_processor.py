from abc import ABC, abstractmethod

from resume_generator.domains.education import Education
from resume_generator.domains.experience import Experience
from resume_generator.domains.personal_info import PersonalInfo
from resume_generator.domains.project import Project
from resume_generator.domains.skills import Skills


class UserProcessor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_user_personal_info(self) -> PersonalInfo:
        """
        Retrieve the user's personal information and return a string.

        Returns:
            str: A string containing the user's personal information.
        """
        pass

    @abstractmethod
    def get_user_education(self) -> list[Education]:
        """
        Retrieve the user's education data and return a json.

        Returns:
            json: A list of schools
        """
        pass

    @abstractmethod
    def get_user_skills(self) -> list[Skills]:
        """
        Retrieve the user's skills data and return a json.

        Returns:
            json: A dict of skills by category and list of skills
        """
        pass

    @abstractmethod
    def get_user_experience(self) -> list[Experience]:
        """
        Retrieve the user's experience data and return a string.

        Returns:
            str: A string containing the user's experience data.
        """
        pass

    @abstractmethod
    def get_user_projects(self) -> list[Project]:
        """
        Retrieve the user's projects data and return a string.

        Returns:
            str: A string containing the user's projects data.
        """
        pass
