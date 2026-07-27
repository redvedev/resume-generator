from pathlib import Path

import pytest

from resume_generator.adapters.user_processor import JsonUserProcessor
from resume_generator.ports.user_processor import UserProcessor


@pytest.fixture
def user_processor() -> UserProcessor:
    data_path = Path("user_data_copy") / "personal_data"
    return JsonUserProcessor(data_path)


def test_reading_personal_data(user_processor: UserProcessor):
    user_processor.get_user_personal_info()


def test_reading_skills(user_processor: UserProcessor):
    user_processor.get_user_skills()


def test_reading_education(user_processor: UserProcessor):
    user_processor.get_user_education()


def test_reading_experience(user_processor: UserProcessor):
    user_processor.get_user_experience()


def test_reading_projects(user_processor: UserProcessor):
    user_processor.get_user_projects()
