from pathlib import Path

import pytest

from resume_generator.adapters.markdown_user_reader import MarkdownUserReader

READER_CONFIGS = [
    (
        MarkdownUserReader,
        Path(__file__).parent / "example_data" / "personal_data_markdown",
    ),
]
