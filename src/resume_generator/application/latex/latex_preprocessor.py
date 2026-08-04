from datetime import datetime

from resume_generator.application.latex.latex_normalizer import LatexNormalizer
from resume_generator.domains.agent_responses import (
    EducationResponse,
    ExperienceResponse,
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
from resume_generator.domains.project import Project
from resume_generator.domains.skills import Skills


class LatexPreprocessor:
    def __init__(self) -> None:
        self.text_normalizer = LatexNormalizer()

    def prepare_skill_latex(self, skill: Skills) -> LatexSkill:
        return LatexSkill(
            category=self.text_normalizer.escape_and_normalize(skill.skills_category),
            skills=[self.text_normalizer.escape_and_normalize(s) for s in skill.skills],
        )

    def prepare_skills_latex(self, skills: list[Skills]) -> LatexSkills:
        return LatexSkills(skills=[self.prepare_skill_latex(s) for s in skills])

    def prepare_experience_latex(
        self, experiences: list[Experience], experience_summary: ExperienceResponse
    ) -> LatexJobs:
        items = []
        for job in experiences:
            for job_summary in experience_summary.jobs:
                if job.job_id != job_summary.job_id:
                    continue
                date = datetime.strptime(job.dates.split("-")[0].strip(), "%m/%Y")
                items.append(
                    LatexJob(
                        position=self.text_normalizer.escape_and_normalize(
                            job.position
                        ),
                        company=self.text_normalizer.escape_and_normalize(job.company),
                        location=self.text_normalizer.escape_and_normalize(
                            job.location
                        ),
                        dates=self.text_normalizer.format_header_dates(
                            self.text_normalizer.escape_and_normalize(job.dates)
                        ),
                        beginning_date=date,
                        bullet_points=[
                            self.text_normalizer.escape_and_normalize(bullet)
                            for bullet in job_summary.bullets
                        ],
                    )
                )
        return LatexJobs(
            jobs=sorted(items, key=lambda x: x.beginning_date, reverse=True)
        )

    def prepare_education_latex(
        self, schools: list[Education], schools_summary: EducationResponse
    ) -> LatexSchools:
        items = []
        for school in schools:
            for school_summary in schools_summary.schools:
                if school.school_id != school_summary.school_id:
                    continue
                date = datetime.strptime(school.dates.split("-")[0].strip(), "%m/%Y")
                items.append(
                    LatexSchool(
                        name=self.text_normalizer.escape_and_normalize(
                            school.school_name
                        ),
                        degree=self.text_normalizer.escape_and_normalize(school.degree),
                        dates=self.text_normalizer.format_header_dates(school.dates),
                        beginning_date=date,
                        courses=[
                            self.text_normalizer.escape_and_normalize(s)
                            for s in school_summary.courses
                        ],
                    )
                )
        return LatexSchools(
            schools=sorted(items, key=lambda x: x.beginning_date, reverse=True)
        )

    def prepare_projects_latex(
        self, projects: list[Project], project_summaries: ProjectResponse
    ) -> LatexProjects:
        items = []
        for project in projects:
            for project_summary in project_summaries.projects:
                if project.project_id != project_summary.project_id:
                    continue
                items.append(
                    LatexProject(
                        name=self.text_normalizer.escape_and_normalize(project.name),
                        project_type=self.text_normalizer.escape_and_normalize(
                            project.type.value
                        ),
                        description=self.text_normalizer.escape_and_normalize(
                            project_summary.description
                        ),
                        year=self.text_normalizer.escape_and_normalize(project.year),
                        technologies=[
                            self.text_normalizer.escape_and_normalize(t)
                            for t in project.technologies
                        ],
                        bullet_points=[
                            self.text_normalizer.escape_and_normalize(b)
                            for b in project_summary.bullets
                        ],
                    )
                )
        return LatexProjects(projects=sorted(items, key=lambda x: x.year, reverse=True))
