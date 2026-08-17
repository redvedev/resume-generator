from resume_generator.application.agent_invoker import AgentInvoker
from resume_generator.application.config import TEMPLATE_DIR
from resume_generator.application.latex.latex_processor import LatexProcessor
from resume_generator.domains.user import User


class LatexGenerator:
    """Build LaTeX resume from structured data."""

    def __init__(self):
        self.latex_processor = LatexProcessor()

    def generate_tex(self, user: User) -> str:
        """Generate complete LaTeX from data."""
        # Load template
        template_path = TEMPLATE_DIR / "main.tex"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found at {template_path}")

        template = template_path.read_text(encoding="utf-8")
        personal = self.latex_processor.generate_personal_info(user.personal_info)

        # Replace placeholders
        replacements = {
            "{{NAME}}": personal.name,
            "{{PHONE}}": personal.phone_number,
            "{{LOCATION}}": personal.location,
            "{{EMAIL}}": personal.email,
            "{{LINKEDIN_PREVIEW}}": personal.linkedin_preview_link,
            "{{LINKEDIN_URL}}": personal.linkedin_actual_link,
            "{{WEBSITE}}": personal.website,
            "{{OBJECTIVE_SECTION}}": self.latex_processor.generate_objective(
                personal.summary
            ),
            "{{EDUCATION_SECTION}}": self.latex_processor.generate_education(
                user.education
            ),
            "{{SKILLS_SECTION}}": self.latex_processor.generate_skills(user.skills),
            "{{EXPERIENCE_SECTION}}": self.latex_processor.generate_experience(
                user.experience
            ),
            "{{PROJECTS_SECTION}}": self.latex_processor.generate_project(
                user.projects
            ),
        }

        rendered = template
        for placeholder, value in replacements.items():
            rendered = rendered.replace(placeholder, value)

        return rendered
