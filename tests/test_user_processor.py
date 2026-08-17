from pathlib import Path

import pytest

from resume_generator.application.prompt_generator import PromptGenerator
from resume_generator.domains.user import User
from resume_generator.ports.user_processor import UserDataReader
from tests.conftest import READER_CONFIGS

# Definiujemy konfiguracje dla obu readerów: (Klasa, Ścieżka do danych)


@pytest.fixture(
    params=READER_CONFIGS,
    ids=["json_reader", "markdown_reader"],  # Ładne nazwy w raporcie pytest
)
def user_processor(request: pytest.FixtureRequest) -> UserDataReader:
    """Fixture parametryzowany - tworzy instancję readera dla każdego zestawu danych."""
    reader_cls, path = request.param
    return reader_cls(path)


@pytest.fixture
def user(user_processor: UserDataReader) -> User:
    return user_processor.read_user()


@pytest.fixture
def offer_description() -> str:
    return "Example offer description"


@pytest.fixture
def prompt_generator() -> PromptGenerator:
    return PromptGenerator()


def test_reading_personal_data(user_processor: UserDataReader):
    user_processor._get_user_personal_info()


def test_reading_skills(user_processor: UserDataReader):
    user_processor._get_user_skills()


def test_reading_education(user_processor: UserDataReader):
    user_processor._get_user_education()


def test_reading_experience(user_processor: UserDataReader):
    user_processor._get_user_experience()


def test_reading_projects(user_processor: UserDataReader):
    user_processor._get_user_projects()


def test_prompt_generation(
    prompt_generator: PromptGenerator, user: User, offer_description: str
):
    prompt_generator.get_llm_prompt_work(offer_description, user.experience)
    prompt_generator.get_llm_prompt_projects(offer_description, user.projects)
    # prompt_generator.get_llm_prompt_education(user.education)
