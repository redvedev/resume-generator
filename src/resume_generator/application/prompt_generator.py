from langchain_core.prompts import PromptTemplate

from resume_generator.domains.education import Education
from resume_generator.domains.experience import Experience
from resume_generator.domains.project import Project
from resume_generator.domains.skills import Skills
from resume_generator.domains.user import User
from resume_generator.ports.job_context_generator import PromptGenerator
from resume_generator.prompt_templates import (
    EDUCATION_SCHOOL_DESCRIPTION_TEMPLATE,
    EDUCATION_SELECTION_TEMPLATE,
    JOB_BULLET_POINT_GENERATOR_TEMPLATE,
    JOB_DESCRIPTION_TEMPLATE,
    PROJECT_BULLET_POINT_GENERATOR_TEMPLATE,
    PROJECT_DESCRIPTION_TEMPLATE,
)


class PromptGenrator:
    def __init__(self, job_description: str, user: User):
        self.job_description = job_description
        self.user = user

    def get_llm_prompt_work(self) -> str:
        experience_template = PromptTemplate.from_template(JOB_DESCRIPTION_TEMPLATE)
        experiences = []
        for job_id, job in enumerate(self.user.experience):
            tasks = "\n".join("- " + task for task in job.achievements)
            impact = "\n".join("- " + imp for imp in job.impact)
            tech_stack = ", ".join(job.technologies)
            experiences.append(
                experience_template.format(
                    job_id=job_id,
                    summary=job.summary,
                    tasks=tasks,
                    impact=impact,
                    tech_stack=tech_stack,
                )
            )

        work_bullet_points_template = PromptTemplate.from_template(
            JOB_BULLET_POINT_GENERATOR_TEMPLATE
        )
        return work_bullet_points_template.format(
            job_description=self.job_description, work_experience="\n".join(experiences)
        )

    def get_llm_prompt_education(self) -> str:
        school_description_template = PromptTemplate.from_template(
            EDUCATION_SCHOOL_DESCRIPTION_TEMPLATE
        )
        education = []
        for school_id, school in enumerate(self.user.education):
            education.append(
                school_description_template.format(
                    school_id=school_id,
                    relevant_courses=", ".join(school.skills),
                    irrelevant_courses=", ".join(school.irrelevant_skills),
                )
            )

        education_template = PromptTemplate.from_template(EDUCATION_SELECTION_TEMPLATE)
        return education_template.format(
            job_description=self.job_description, education="\n".join(education)
        )

    def get_llm_prompt_projects(self) -> str:
        project_template = PromptTemplate.from_template(PROJECT_DESCRIPTION_TEMPLATE)
        projects = []
        for project_id, project in enumerate(self.user.projects):
            actions = "\n".join("- " + task for task in project.actions)
            outcome = "\n".join("- " + imp for imp in project.outcome)
            metrices = "\n".join("- " + imp for imp in project.metrics)
            tech_stack = ", ".join(project.technologies)
            projects.append(
                project_template.format(
                    project_id=project_id,
                    project_name=project.name,
                    project_type=project.type.value,
                    project_description=project.description,
                    actions=actions,
                    project_outcome=outcome,
                    metrics=metrices,
                    tech_stack=tech_stack,
                )
            )

        project_bullet_points_template = PromptTemplate.from_template(
            PROJECT_BULLET_POINT_GENERATOR_TEMPLATE
        )
        return project_bullet_points_template.format(
            job_description=self.job_description,
            projects_description="\n".join(projects),
        )
