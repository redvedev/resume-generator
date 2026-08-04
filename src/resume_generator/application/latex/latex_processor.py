import logging

from resume_generator.application.agent_invoker import AgentInvoker
from resume_generator.application.latex.later_renderer import LatexRenderer
from resume_generator.application.latex.latex_normalizer import LatexNormalizer
from resume_generator.application.latex.latex_preprocessor import LatexPreprocessor
from resume_generator.domains.agent_responses import (
    EducationResponse,
    ExperienceResponse,
    ExperienceSummary,
    ProjectResponse,
)
from resume_generator.domains.education import Education
from resume_generator.domains.experience import Experience
from resume_generator.domains.latex_renders import (
    LatexJob,
    LatexJobs,
    LatexProject,
    LatexProjects,
    LatexSchool,
    LatexSchools,
    LatexSkill,
    LatexSkills,
)
from resume_generator.domains.personal_info import PersonalInfo
from resume_generator.domains.project import Project
from resume_generator.domains.skills import Skills
from resume_generator.domains.user import User


class LatexSectionBuilder:
    def __init__(self) -> None:
        self.latex_preprocessor = LatexPreprocessor()
        self.latex_renderer = LatexRenderer()

    def _wrap_section(self, title: str, body: str) -> str:
        if not body or not body.strip():
            return ""
        begin = f"\\begin{{rSection}}{{{title}}}"
        end = f"\\end{{rSection}}"
        return f"{begin}\n{body}\n{end}\n"

    def build_simple_body_section(self, title: str, body: str) -> str:
        """Build a section only when its body is non-empty."""
        return self._wrap_section(title, body)

    def build_skills_section(self, skills: list[Skills]) -> str:
        """Build skills section as LaTeX tabular."""
        processed_skills = self.latex_preprocessor.prepare_skills_latex(skills)
        return self.latex_renderer.render_skills(processed_skills)

    def build_experience_section(
        self, experience_summary: ExperienceResponse, experiences: list[Experience]
    ) -> str:
        """Build experience section as LaTeX."""
        if not experiences:
            return ""

        jobs = self.latex_preprocessor.prepare_experience_latex(
            experiences, experience_summary
        )
        return self.latex_renderer.render_jobs(jobs)

    def build_projects_section(
        self, projects_summaries: ProjectResponse, projects: list[Project]
    ) -> str:
        """Build projects section as LaTeX."""
        if not projects:
            return ""

        processed_projects = self.latex_preprocessor.prepare_projects_latex(
            projects, projects_summaries
        )
        return self.latex_renderer.render_projects(processed_projects)

    def build_education_section(
        self, summaries: EducationResponse, schools: list[Education]
    ) -> str:
        """Build education section as LaTeX matching original template."""
        processed_schools = self.latex_preprocessor.prepare_education_latex(
            schools, summaries
        )
        return self.latex_renderer.render_schools(processed_schools)


class LatexProcessor:
    def __init__(self, agent_invoker: AgentInvoker) -> None:
        self.text_normalizer = LatexNormalizer()
        self.latex_builder = LatexSectionBuilder()
        self.agent_invoker = agent_invoker

    def generate_personal_info(self, personal: PersonalInfo):
        return PersonalInfo(
            name=self.text_normalizer.escape_latex(personal.name),
            phone=self.text_normalizer.escape_latex(personal.phone_number),
            location=self.text_normalizer.escape_latex(personal.location),
            email=self.text_normalizer.escape_latex(personal.email),
            linkedin_preview=self.text_normalizer.escape_latex(
                personal.linkedin_preview_link
            ),
            linkedin_url=self.text_normalizer.normalize_website(
                self.text_normalizer.escape_latex(personal.linkedin_actual_link)
            ),
            website=self.text_normalizer.normalize_website(
                self.text_normalizer.escape_latex(
                    self.text_normalizer.normalize_website(personal.website)
                )
            ),
            summary=self.text_normalizer.escape_latex(personal.summary),
        )

    def generate_objective(self, summary: str) -> str:
        return self.latex_builder.build_simple_body_section("Objective", summary)

    def generate_education(self, education: list[Education]) -> str:
        return self.latex_builder.build_simple_body_section(
            "Education",
            self.latex_builder.build_education_section(
                schools=education,
                summaries=self.agent_invoker.get_user_education_summary(education),
            ),
        )

    def generate_skills(self, skills: list[Skills]) -> str:
        return self.latex_builder.build_simple_body_section(
            "Skills", self.latex_builder.build_skills_section(skills=skills)
        )

    def generate_experience(self, experience: list[Experience]) -> str:

        return self.latex_builder.build_simple_body_section(
            "Experience",
            self.latex_builder.build_experience_section(
                experience_summary=self.agent_invoker.get_user_experience_summary(
                    experience
                ),
                experiences=experience,
            ),
        )

    def generate_project(self, projects: list[Project]) -> str:
        return self.latex_builder.build_simple_body_section(
            "Projects",
            self.latex_builder.build_projects_section(
                projects_summaries=self.agent_invoker.get_user_projects_summary(
                    projects
                ),
                projects=projects,
            ),
        )
