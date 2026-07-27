from pathlib import Path

import pytest

from resume_generator.adapters.job_context import JobContextGeneratorImpl
from resume_generator.adapters.user_processor import JsonUserProcessor
from resume_generator.domains.user import User
from resume_generator.ports.job_context_generator import PromptGenerator
from resume_generator.ports.user_processor import UserProcessor


@pytest.fixture
def user_processor() -> UserProcessor:
    data_path = Path("user_data") / "personal_data"
    return JsonUserProcessor(data_path)


@pytest.fixture
def user(user_processor: UserProcessor) -> User:
    return user_processor.read_user()


@pytest.fixture
def offer_description() -> str:
    return "Example offer description"


@pytest.fixture
def prompt_generator(offer_description: str, user: User) -> PromptGenerator:
    return JobContextGeneratorImpl(offer_description, user)


def test_reading_personal_data(user_processor: UserProcessor):
    user_processor._get_user_personal_info()


def test_reading_skills(user_processor: UserProcessor):
    user_processor._get_user_skills()


def test_reading_education(user_processor: UserProcessor):
    user_processor._get_user_education()


def test_reading_experience(user_processor: UserProcessor):
    user_processor._get_user_experience()


def test_reading_projects(user_processor: UserProcessor):
    user_processor._get_user_projects()


def test_prompt_generation(prompt_generator: PromptGenerator):
    prompt_generator.get_llm_prompt_work()
    prompt_generator.get_llm_prompt_projects()
    prompt_generator.get_llm_prompt_education()
