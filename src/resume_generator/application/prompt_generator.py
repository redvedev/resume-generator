import logging

from langchain_core.prompts import PromptTemplate

from resume_generator.application.config import PERSONAL_INFO_DIR
from resume_generator.domains.user import (
    Education,
    Experience,
    PersonalInfo,
    Project,
    Skills,
    User,
)
from resume_generator.prompt_templates import (
    NOTES_TEMPLATE,
    RATE_USER_FIT_TEMPLATE,
    USER_SELECTION_FACT_TEMPLATE,
)

logger = logging.getLogger(__name__)


class PromptGenerator:
    def __init__(self):
        pass

    def read_user_data(self) -> str:
        user_data_home_dir = PERSONAL_INFO_DIR
        user_data_dir_content = ""

        for file in user_data_home_dir.glob("*.md"):
            user_data_dir_content += f"""File name: {file.name}
        ============================================
        {file.read_text(encoding="utf-8")}
        ============================================
        """

        for directory in user_data_home_dir.glob("*/"):
            if directory.stem[0] == ".":
                continue
            for file in directory.glob("*.md"):
                user_data_dir_content += f"""Directory name: {directory.stem}
        ============================================
        {file.read_text(encoding="utf-8")}
        ============================================
        """
        return user_data_dir_content

    def select_user_facts(self, job_description: str) -> str:
        template = PromptTemplate.from_template(USER_SELECTION_FACT_TEMPLATE)
        user = self.read_user_data()
        prompt = template.format(job_description=job_description, user_json=user)
        logger.info(f"User selection prompt: {prompt}")
        return prompt

    def rate_user_fit(self, job_description: str) -> str:
        template = PromptTemplate.from_template(RATE_USER_FIT_TEMPLATE)
        user = self.read_user_data()
        prompt = template.format(job_description=job_description, user=user)
        return prompt

    def get_job_notes(self, job_description: str, user: User) -> str:
        # Now we want make notes based on the actual user data, not entire database
        template = PromptTemplate.from_template(NOTES_TEMPLATE)
        prompt = template.format(
            job_description=job_description, user=user.model_dump_json(indent=4)
        )
        return prompt
