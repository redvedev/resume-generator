import logging

from langchain_core.prompts import PromptTemplate

from resume_generator.domains.education import Education
from resume_generator.domains.experience import Experience
from resume_generator.domains.project import Project
from resume_generator.domains.skills import Skills
from resume_generator.prompt_templates import (
    EDUCATION_SCHOOL_DESCRIPTION_TEMPLATE,
    EDUCATION_SELECTION_TEMPLATE,
    JOB_BULLET_POINT_GENERATOR_TEMPLATE,
    JOB_DESCRIPTION_TEMPLATE,
    PROJECT_BULLET_POINT_GENERATOR_TEMPLATE,
    PROJECT_DESCRIPTION_TEMPLATE,
)

logger = logging.getLogger(__name__)


class PromptGenerator:
    def __init__(self, job_description: str):
        self.job_description = job_description

    def get_llm_prompt_work(self, experience: list[Experience]) -> str:
        experience_template = PromptTemplate.from_template(JOB_DESCRIPTION_TEMPLATE)
        experiences = []
        for job in experience:
            tasks = "\n".join("- " + task for task in job.achievements)
            impact = "\n".join("- " + imp for imp in job.impact)
            tech_stack = ", ".join(job.technologies)
            experiences.append(
                experience_template.format(
                    job_id=job.job_id,
                    summary=job.summary,
                    tasks=tasks,
                    impact=impact,
                    tech_stack=tech_stack,
                )
            )

        work_bullet_points_template = PromptTemplate.from_template(
            JOB_BULLET_POINT_GENERATOR_TEMPLATE
        )
        prompt = work_bullet_points_template.format(
            job_description=self.job_description, work_experience="\n".join(experiences)
        )
        logger.info("Job experience prompt: ", prompt)
        return prompt

    def get_llm_prompt_education(self, schools: list[Education]) -> str:
        school_description_template = PromptTemplate.from_template(
            EDUCATION_SCHOOL_DESCRIPTION_TEMPLATE
        )
        education = []
        for school in schools:
            education.append(
                school_description_template.format(
                    school_id=school.school_id,
                    relevant_courses=", ".join(school.skills),
                    irrelevant_courses=", ".join(school.irrelevant_skills),
                )
            )

        education_template = PromptTemplate.from_template(EDUCATION_SELECTION_TEMPLATE)
        prompt = education_template.format(
            job_description=self.job_description, education="\n".join(education)
        )
        logger.info("Education prompt: ", prompt)
        return prompt

    def get_llm_prompt_projects(self, projects_list: list[Project]) -> str:
        project_template = PromptTemplate.from_template(PROJECT_DESCRIPTION_TEMPLATE)
        projects = []
        for project in projects_list:
            actions = "\n".join("- " + task for task in project.actions)
            outcome = "\n".join("- " + imp for imp in project.outcome)
            metrices = "\n".join("- " + imp for imp in project.metrics)
            tech_stack = ", ".join(project.technologies)
            projects.append(
                project_template.format(
                    project_id=project.project_id,
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
        prompt = project_bullet_points_template.format(
            job_description=self.job_description,
            projects_description="\n".join(projects),
        )
        logger.info("Project prompt: ", prompt)
        return prompt
