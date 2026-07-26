from abc import ABC, abstractmethod

class UserProcessor(ABC):
    def __init__(self):
        pass


    @abstractmethod
    def get_user_personal_info(self) -> str:
        """
        Retrieve the user's personal information and return a string.

        Returns:
            str: A string containing the user's personal information.
        """
        pass


    @abstractmethod
    def get_user_education(self) -> str:
        """
        Retrieve the user's education data and return a string.

        Returns:
            str: A string containing the user's education data.
        """
        pass


    @abstractmethod
    def get_user_skills(self) -> str:
        """
        Retrieve the user's skills data and return a string.

        Returns:
            str: A string containing the user's skills data.
        """
        pass


    @abstractmethod
    def get_user_experience(self) -> str:
        """
        Retrieve the user's experience data and return a string.

        Returns:
            str: A string containing the user's experience data.
        """
        pass

    @abstractmethod
    def get_user_projects(self) -> str:
        """
        Retrieve the user's projects data and return a string.

        Returns:
            str: A string containing the user's projects data.
        """
        pass