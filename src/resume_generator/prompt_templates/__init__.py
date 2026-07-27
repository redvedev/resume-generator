from pathlib import Path

current_path = Path(__file__).parent.resolve()

job_description_prompt_file = current_path / "JOB_DESCRIPTION.md"
job_bullet_point_generation_prompt_file = current_path / "JOB_BULLET_GENERATOR.md"

JOB_BULLET_POINT_GENERATOR_TEMPLATE = job_bullet_point_generation_prompt_file.read_text(
    encoding="utf-8"
)
JOB_DESCRIPTION_TEMPLATE = job_description_prompt_file.read_text(encoding="utf-8")
