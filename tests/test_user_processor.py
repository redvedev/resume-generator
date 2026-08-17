from pathlib import Path

import pytest

from resume_generator.application.prompt_generator import PromptGenerator
from resume_generator.domains.user import User
from resume_generator.ports.user_processor import UserDataReader
from tests.conftest import READER_CONFIGS

# Definiujemy konfiguracje dla obu readerów: (Klasa, Ścieżka do danych)


@pytest.fixture(
    params=READER_CONFIGS,
    ids=["markdown_reader"],  # Ładne nazwy w raporcie pytest
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
