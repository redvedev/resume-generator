from pathlib import Path

current_path = Path(__file__).parent.resolve()


USER_SELECTION_FACT_TEMPLATE = (current_path / "USER_FACT_SELECTION.md").read_text(
    encoding="utf-8"
)

RATE_USER_FIT_TEMPLATE = (current_path / "RATE_USER_FIT.md").read_text(encoding="utf-8")

NOTES_TEMPLATE = (current_path / "PREPARE_NOTES.md").read_text(encoding="utf-8")

REQUIREMENT_ANALYSIS_TEMPLATE = (current_path / "REQUIREMENT_ANALYSIS.md").read_text(
    encoding="utf-8"
)

RESUME_VALIDATION_TEMPLATE = (current_path / "RESUME_VALIDATION.md").read_text(
    encoding="utf-8"
)
