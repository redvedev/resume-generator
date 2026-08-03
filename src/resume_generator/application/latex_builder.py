import logging
import re
from datetime import datetime
from typing import Any, Dict, List

from resume_generator.application.agent_invoker import AgentInvoker
from resume_generator.application.config import TEMPLATE_DIR
from resume_generator.domains.agent_responses import (
    EducationResponse,
    ExperienceResponse,
    ProjectResponse,
)
from resume_generator.domains.education import Education
from resume_generator.domains.experience import Experience
from resume_generator.domains.project import Project
from resume_generator.domains.skills import Skills
from resume_generator.domains.user import User

logger = logging.getLogger(__name__)


class LatexGenerator:
    """Build LaTeX resume from structured data."""

    def __init__(self):
        pass

    def escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        if not text:
            return ""

        # Don't escape LaTeX commands
        if text.startswith("\\"):
            return text

        replacements = {
            "&": r"\&",
            "%": r"\%",
            "$": r"\$",
            "#": r"\#",
            "_": r"\_",
            "{": r"\{",
            "}": r"\}",
            "~": r"\textasciitilde{}",
            "^": r"\textasciicircum{}",
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
            return website[len("https://") :]
        if website.startswith("http://"):
            return website[len("http://") :]
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
            skills_text = ", ".join(
                [self.escape_and_normalize(s) for s in skill.skills]
            )
            items.append(f"{category_escaped} & {skills_text}")

        if not items:
            return ""

        latex += "\\\\\n".join(items)
        latex += "\n\\end{tabularx}\\\\"

        return latex

    def build_experience_section(
        self, experience_summary: ExperienceResponse, experiences: list[Experience]
    ) -> str:
        """Build experience section as LaTeX."""
        if not experiences:
            return ""

        latex = ""
        jobs_summaries_pairs = sorted(
            [
                (S, J, datetime.strptime(J.dates.split("-")[0].strip(), "%m/%Y"))
                for S in experience_summary.jobs
                for J in experiences
                if S.job_id == J.job_id
            ],
            key=lambda x: x[2],
            reverse=True,
        )
        for summary, job, _ in jobs_summaries_pairs:
            company = self.escape_and_normalize(job.company)
            role = self.escape_and_normalize(job.position)
            dates = self.escape_and_normalize(job.dates)
            location = self.escape_and_normalize(job.location)
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

            for bullet in summary.bullets:
                bullet_text = self.escape_and_normalize(bullet)
                block_lines.append(f"    \\item {bullet_text}")

            block_lines.append("\\end{itemize}")
            latex += "\n".join(block_lines) + "\n\n"

        return latex

    def build_projects_section(
        self, projects_summaries: ProjectResponse, projects: list[Project]
    ) -> str:
        """Build projects section as LaTeX."""
        if not projects:
            return ""

        row_break = " \\\\"
        latex = ""
        for summary in projects_summaries.projects:
            project = [p for p in projects if p.project_id == summary.project_id][0]
            name = self.escape_and_normalize(project.name)
            year = self.escape_and_normalize(project.year)
            project_type = self.escape_and_normalize(project.type.value)

            # Header {Project name} - {Project type} {year}
            latex += (
                f"\\noindent \\textbf{{{name}}} - {project_type} \\hfill {year}"
                + row_break
                + "\n"
            )
            # Project description
            latex += (
                "\\textbf{Description}: "
                + self.escape_and_normalize(summary.description)
                + row_break
                + "\n"
            )
            # Listed technologies used in the project
            latex += (
                "\\textbf{Technologies}: "
                + ", ".join(
                    [self.escape_and_normalize(t) for t in project.technologies if t]
                )
                + "\n"
            )

            latex += "\\begin{itemize}[leftmargin=*,labelsep=0.5em,itemsep=-0.5em,topsep=0pt]\n"
            # metrics = self.escape_and_normalize(project.metrics)
            # outcome = self.escape_and_normalize(project.outcome)
            for bullet in summary.bullets:
                # TODO: If we have outcome / measures we append them here
                latex += f"\\item {self.escape_and_normalize(bullet)}\n"
            latex += "\\end{itemize}\n\n"

        return latex

    def build_education_section(
        self, summaries: EducationResponse, schools: list[Education]
    ) -> str:
        """Build education section as LaTeX matching original template."""
        latex = ""
        schools_summaries_pairs = sorted(
            [
                (S, J, datetime.strptime(J.dates.split("-")[0].strip(), "%m/%Y"))
                for S in summaries.schools
                for J in schools
                if S.school_id == J.school_id
            ],
            key=lambda x: x[2],
            reverse=True,
        )
        for summary in summaries.schools:
            school = [s for s in schools if s.school_id == summary.school_id][0]
            degree = self.escape_and_normalize(school.degree)
            school_name = self.escape_and_normalize(school.school_name)
            dates = self.escape_and_normalize(school.dates)
            courses = summary.courses
            dates_cell = self._format_header_dates(dates)
            row_break = "\\\\"

            block_lines = [
                "\\noindent",
                "\\begin{tabular*}{\\textwidth}{@{}l@{\\extracolsep{\\fill}}r@{}}",
                f"\\textbf{{{degree}}} & {dates_cell} {row_break}",
                "\\end{tabular*}",
                "\\noindent",
                "\\begin{tabular*}{\\textwidth}{@{}l@{\\extracolsep{\\fill}}r@{}}",
                f"\\textit{{{school_name}}} {row_break}",
                "\\end{tabular*}",
            ]

            if courses:
                courses_text = ", ".join(
                    [self.escape_and_normalize(c) for c in courses]
                )
                block_lines.extend(
                    [
                        "\\noindent",
                        f"Relevant Coursework: {courses_text}",
                    ]
                )

            latex += "\n".join(block_lines) + "\n\n"

        return latex

    def build_simple_body_section(self, title: str, body: str) -> str:
        """Build a section only when its body is non-empty."""
        return self._wrap_section(title, body)

    def generate_tex(self, user: User, agent_invoker: AgentInvoker) -> str:
        """Generate complete LaTeX from data."""
        # Load template
        template_path = TEMPLATE_DIR / "main.tex"
        if not template_path.exists():
            raise FileNotFoundError(f"Template not found at {template_path}")

        template = template_path.read_text(encoding="utf-8")

        # Personal info
        personal = user.personal_info
        name = self.escape_latex(personal.name)
        phone = self.escape_latex(personal.phone_number)
        location = self.escape_latex(personal.location)
        email = self.escape_latex(personal.email)
        linkedin_preview = self.escape_latex(personal.linkedin_preview_link)
        linkedin_url = self._normalize_website(
            self.escape_latex(personal.linkedin_actual_link)
        )
        website = self._normalize_website(
            self.escape_latex(self._normalize_website(personal.website))
        )

        # Sections
        objective_section = self.build_simple_body_section(
            "Objective", self.escape_latex(personal.summary)
        )

        education_section = self.build_simple_body_section(
            "Education",
            self.build_education_section(
                agent_invoker.get_user_education_summary(), user.education
            ),
        )

        skills_section = self.build_simple_body_section(
            "Skills", self.build_skills_section(user.skills)
        )

        experience_section = self.build_simple_body_section(
            "Experience",
            self.build_experience_section(
                agent_invoker.get_user_experience_summary(), user.experience
            ),
        )

        projects_section = self.build_simple_body_section(
            "Projects",
            self.build_projects_section(
                agent_invoker.get_user_projects_summary(), user.projects
            ),
        )

        # Replace placeholders
        replacements = {
            "{{NAME}}": name,
            "{{PHONE}}": phone,
            "{{LOCATION}}": location,
            "{{EMAIL}}": email,
            "{{LINKEDIN_PREVIEW}}": linkedin_preview,
            "{{LINKEDIN_URL}}": linkedin_url,
            "{{WEBSITE}}": website,
            "{{OBJECTIVE_SECTION}}": objective_section,
            "{{EDUCATION_SECTION}}": education_section,
            "{{SKILLS_SECTION}}": skills_section,
            "{{EXPERIENCE_SECTION}}": experience_section,
            "{{PROJECTS_SECTION}}": projects_section,
        }

        rendered = template
        for placeholder, value in replacements.items():
            rendered = rendered.replace(placeholder, value)

        return rendered
