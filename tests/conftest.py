from pathlib import Path

import pytest

from resume_generator.adapters.json_user_reader import JsonUserReader
from resume_generator.adapters.markdown_user_reader import MarkdownUserReader

READER_CONFIGS = [
    (JsonUserReader, Path(__file__).parent / "example_data" / "personal_data_json"),
    (
        MarkdownUserReader,
        Path(__file__).parent / "example_data" / "personal_data_markdown",
    ),
]
