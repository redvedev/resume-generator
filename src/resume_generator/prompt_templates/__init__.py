from pathlib import Path

current_path = Path(__file__).parent.resolve()

JOB_BULLET_POINT_GENERATOR_TEMPLATE = (
    current_path / "JOB_BULLET_GENERATOR.md"
).read_text(encoding="utf-8")

JOB_DESCRIPTION_TEMPLATE = (current_path / "JOB_DESCRIPTION.md").read_text(
    encoding="utf-8"
)

PROJECT_BULLET_POINT_GENERATOR_TEMPLATE = (
    current_path / "PROJECT_BULLET_GENERATOR.md"
).read_text(encoding="utf-8")

PROJECT_DESCRIPTION_TEMPLATE = (current_path / "PROJECT_DESCRIPTION.md").read_text(
    encoding="utf-8"
)

EDUCATION_SELECTION_TEMPLATE = (current_path / "EDUCATION_SELECTION.md").read_text(
    encoding="utf-8"
)

EDUCATION_SCHOOL_DESCRIPTION_TEMPLATE = (
    current_path / "EDUCATION_SCHOOL.md"
).read_text(encoding="utf-8")
