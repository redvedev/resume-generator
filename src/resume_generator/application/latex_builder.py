import logging
import re
from typing import Any, Dict, List

from resume_generator.application.config import TEMPLATE_DIR
from resume_generator.domains.experience import Experience
from resume_generator.domains.skills import Skills
from resume_generator.ports.user_processor import UserProcessor

logger = logging.getLogger(__name__)

class LatexGenerator():
    """Build LaTeX resume from structured data."""

    def __init__(self):
        pass

    def escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        if not text:
            return ""

        # Don't escape LaTeX commands
        if text.startswith('\\'):
            return text

        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
        }

        for char, replacement in replacements.items():
            text = text.replace(char, replacement)

        return text

    def normalize_text(self, text: str) -> str:
        """Normalize text for LaTeX and ATS extraction."""
        if not text:
            return ""

        text = text.replace("–", "--")
        text = text.replace("—", "---")
        text = re.sub(r"\s*--\s*", " -- ", text)
        return text

    def escape_and_normalize(self, text: str) -> str:
        """Normalize unicode punctuation before LaTeX escaping."""
        return self.escape_latex(self.normalize_text(text))

    def _wrap_section(self, title: str, body: str) -> str:
        if not body or not body.strip():
            return ""

        return f"\\begin{{rSection}}{{{title}}}\n{body}\n\\end{{rSection}}\n"

    def _normalize_website(self, website: str) -> str:
        website = (website or "").strip()
        if website.startswith("https://"):
            return website[len("https://"):]
        if website.startswith("http://"):
            return website[len("http://"):]
        return website

    def _format_header_dates(self, dates: str) -> str:
        """Wrap header dates so PDF text extraction keeps them separated."""
        return f"\\mbox{{~{dates}~}}"

    def build_skills_section(self, skills: list[Skills]) -> str:
        """Build skills section as LaTeX tabular."""
        if not skills:
            return ""

        latex = "\\begin{tabularx}{\\textwidth}{@{}>{\\bfseries}l@{\\hspace{2ex}}>{\\RaggedRight\\arraybackslash}X@{}}\n"
        items = []

        for skill in skills:
            category_escaped = self.escape_and_normalize(skill.skills_category)
            skills_text = ", ".join([self.escape_and_normalize(s) for s in skill.skills])
            items.append(f"{category_escaped} & {skills_text}")

        if not items:
            return ""

        latex += "\\\\\n".join(items)
        latex += "\n\\end{tabularx}\\\\"

        return latex

    def build_experience_section(self, experiences: list[Experience], bullets: list[str]) -> str:
        """Build experience section as LaTeX."""
        if not experiences:
            return ""

        latex = ""
        for exp in experiences:
            company = self.escape_and_normalize(exp.company)
            role = self.escape_and_normalize(exp.position)
            dates = self.escape_and_normalize(exp.dates)
            location = self.escape_and_normalize(exp.location)
            dates_cell = self._format_header_dates(dates)
            row_break = "\\\\"

            block_lines = [
                "\\noindent",
                "\\begin{tabular*}{\\textwidth}{@{}l@{\\extracolsep{\\fill}}r@{}}",
                f"\\textbf{{{role}}} & {dates_cell} {row_break}",
                "\\end{tabular*}",
                "\\noindent",
                "\\begin{tabular*}{\\textwidth}{@{}l@{\\extracolsep{\\fill}}r@{}}",
                f"\\textit{{{company}}} & \\textit{{{location}}} {row_break}",
                "\\end{tabular*}",
                "\\begin{itemize}[leftmargin=*,labelsep=0.5em,itemsep=-0.5em,topsep=0pt]",
            ]

            for bullet in bullets:
                bullet_text = self.escape_and_normalize(bullet)
                block_lines.append(f"    \\item {bullet_text}")

            block_lines.append("\\end{itemize}")
            latex += "\n".join(block_lines) + "\n\n"

        return latex

    def build_projects_section(self, projects: List[Dict]) -> str:
        """Build projects section as LaTeX."""
        if not projects:
            return ""

        row_break = " \\\\"
        latex = ""
        for project in projects:
            name = self.escape_and_normalize(project.get('name', 'Unknown'))
            year = self.escape_and_normalize(project.get('year', ''))
            project_type = self.escape_and_normalize(project.get('type', ''))
            tech = [self.escape_and_normalize(t) for t in project.get('tech', []) if t]
            metrics = self.escape_and_normalize(project.get('metrics', ''))
            description = self.escape_and_normalize(project.get('description', ''))
            outcome = self.escape_and_normalize(project.get('outcome', ''))
            bullets = project.get('bullets', [])
            header_line = f"\\noindent \\textbf{{{name}}} - {project_type}"
            if year:
                header_line += f" \\hfill {year}"

            bullet_lines = []
            for bullet in bullets:
                bullet_lines.append(f"\\item {self.escape_and_normalize(bullet)}")
            if outcome:
                if metrics and not description:
                    outcome = f"{outcome} (Metrics: {metrics})"
                bullet_lines.append(f"\\item Outcome: {outcome}")

            latex += header_line + row_break + "\n"
            if description:
                description_sentences = [
                    sentence.strip()
                    for sentence in re.split(r'(?<=[.!?])\s+', description)
                    if sentence.strip()
                ]
                if metrics and description_sentences:
                    description_sentences[0] = f"{description_sentences[0]} (Metrics: {metrics})"
                latex += "Description: " + " ".join(description_sentences) + row_break + "\n"
            if tech:
                latex += "Technologies: " + ", ".join(tech) + "\n"

            latex += "\\begin{itemize}[leftmargin=*,labelsep=0.5em,itemsep=-0.5em,topsep=0pt]\n"
            for bullet_line in bullet_lines:
                latex += f"    {bullet_line}\n"
            latex += "\\end{itemize}\n\n"

        return latex

    def build_education_section(self, education: List[Dict]) -> str:
        """Build education section as LaTeX matching original template."""
        if not education:
            return ""

        latex = ""
        for entry in education:
            degree = self.escape_and_normalize(entry.get('degree', 'Unknown'))
            school = self.escape_and_normalize(entry.get('school', 'Unknown'))
            dates = self.escape_and_normalize(entry.get('dates', 'Unknown'))
            location = self.escape_and_normalize(entry.get('location', ''))
            courses = entry.get('courses', [])
            dates_cell = self._format_header_dates(dates)
            row_break = "\\\\"

            block_lines = [
                "\\noindent",
                "\\begin{tabular*}{\\textwidth}{@{}l@{\\extracolsep{\\fill}}r@{}}",
                f"\\textbf{{{degree}}} & {dates_cell} {row_break}",
                "\\end{tabular*}",
                "\\noindent",
                "\\begin{tabular*}{\\textwidth}{@{}l@{\\extracolsep{\\fill}}r@{}}",
                f"\\textit{{{school}}} & \\textit{{{location}}} {row_break}",
                "\\end{tabular*}",
            ]

            if courses:
                courses_text = ", ".join([self.escape_and_normalize(c) for c in courses])
                block_lines.extend([
                    "\\noindent",
                    f"Relevant Coursework: {courses_text}",
                ])

            latex += "\n".join(block_lines) + "\n\n"

        return latex

    def build_simple_body_section(self, title: str, body: str) -> str:
        """Build a section only when its body is non-empty."""
        return self._wrap_section(title, body)

    def generate_tex(self, user_processor: UserProcessor, llm_response: Dict[str, Any]) -> str:
        """Generate complete LaTeX from data."""
        # Load template
        template_path = TEMPLATE_DIR / "main.tex"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found at {template_path}")

        template = template_path.read_text(encoding='utf-8')

        # Build sections
        # TODO: Construct skills, experience and shit from LLM response using pydantic validate method
        skills_section = self.build_skills_section(llm_response.get('skills', {}))
        experience_section = self.build_experience_section(llm_response.get('experience', []))
        projects_section = self.build_projects_section(llm_response.get('projects', []))
        education_section = self.build_education_section(llm_response.get('education', []))

        # Personal info
        personal = user_processor.get_user_personal_info()
        name = self.escape_latex(personal.name)
        phone = self.escape_latex(personal.phone_number)
        location = self.escape_latex(personal.location)
        email = self.escape_latex(personal.email)
        linkedin_preview = self.escape_latex(personal.linkedin_preview_link)
        linkedin_url = self._normalize_website(self.escape_latex(personal.linkedin_actual_link))
        website = self._normalize_website(self.escape_latex(self._normalize_website(personal.website)))
        objective = self.escape_latex(llm_response.get('objective', 'No objective provided.'))

        objective_section = self.build_simple_body_section("Objective", objective)
        education_section = self.build_simple_body_section("Education", education_section)
        skills_section = self.build_simple_body_section("Skills", skills_section)
        experience_section = self.build_simple_body_section("Experience", experience_section)
        projects_section = self.build_simple_body_section("Projects", projects_section)

        # Replace placeholders
        replacements = {
            '{{NAME}}': name,
            '{{PHONE}}': phone,
            '{{LOCATION}}': location,
            '{{EMAIL}}': email,
            '{{LINKEDIN_PREVIEW}}': linkedin_preview,
            '{{LINKEDIN_URL}}': linkedin_url,
            '{{WEBSITE}}': website,
            '{{OBJECTIVE_SECTION}}': objective_section,
            '{{EDUCATION_SECTION}}': education_section,
            '{{SKILLS_SECTION}}': skills_section,
            '{{EXPERIENCE_SECTION}}': experience_section,
            '{{PROJECTS_SECTION}}': projects_section
        }

        rendered = template
        for placeholder, value in replacements.items():
            rendered = rendered.replace(placeholder, value)

        return rendered
