from langchain_core.prompts import PromptTemplate

from resume_generator.domains.education import Education
from resume_generator.domains.experience import Experience
from resume_generator.domains.project import Project
from resume_generator.domains.skills import Skills
from resume_generator.domains.user import User
from resume_generator.ports.job_context_generator import JobContextGenerator
from resume_generator.prompt_templates import (
    JOB_BULLET_POINT_GENERATOR_TEMPLATE,
    JOB_DESCRIPTION_TEMPLATE,
)


class JobContextGeneratorImpl(JobContextGenerator):
    def generate_job_keywords(self) -> list[str]:
        # Implement the logic to generate job keywords based on the job description
        # For example, you can use NLP techniques or keyword extraction algorithms
        # Here, we'll just return a placeholder dictionary for demonstration purposes
        return ["python"]

    def get_llm_prompt(self, user: User) -> str:
        return ""

    def get_llm_prompt_work(self, user: User) -> str:
        experience_template = PromptTemplate.from_template(JOB_DESCRIPTION_TEMPLATE)
        experiences = []
        for job_id, job in enumerate(user.experience):
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

    def filter_user_info(self) -> User:
        job_keywords = self.generate_job_keywords()
        candidate_personal = self.user.personal_info
        skills = self.filter_relevant_skills(self.user.skills, job_keywords)
        education = self.filter_relevant_education(self.user.education, job_keywords)
        experience = self.filter_relevant_experience(self.user.experience, job_keywords)
        projects = self.filter_relevant_projects(self.user.projects, job_keywords)
        return User(
            personal_info=candidate_personal,
            education=education,
            experience=experience,
            projects=projects,
            skills=skills,
        )

    def filter_relevant_skills(
        self, skills: list[Skills], keywords: list[str]
    ) -> list[Skills]:
        return skills

    def filter_relevant_education(
        self, education: list[Education], keywords: list[str]
    ) -> list[Education]:
        return education

    def filter_relevant_experience(
        self, experience: list[Experience], keywords: list[str]
    ) -> list[Experience]:
        return experience

    def filter_relevant_projects(
        self, projects: list[Project], keywords: list[str]
    ) -> list[Project]:
        return projects
