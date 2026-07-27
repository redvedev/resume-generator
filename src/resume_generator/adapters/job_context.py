from resume_generator.domains.education import Education
from resume_generator.domains.experience import Experience
from resume_generator.domains.project import Project
from resume_generator.domains.skills import Skills
from resume_generator.domains.user import User
from resume_generator.ports.job_context_generator import JobContextGenerator


class JobContextGeneratorImpl(JobContextGenerator):
    def generate_job_keywords(self) -> list[str]:
        # Implement the logic to generate job keywords based on the job description
        # For example, you can use NLP techniques or keyword extraction algorithms
        # Here, we'll just return a placeholder dictionary for demonstration purposes
        return ["python"]

    def get_llm_prompt(self, user: User) -> str:
        return ""

    def filter_user_info(self, user: User) -> User:
        job_keywords = self.generate_job_keywords()
        candidate_personal = user.personal_info
        skills = self.filter_relevant_skills(user.skills, job_keywords)
        education = self.filter_relevant_education(user.education, job_keywords)
        experience = self.filter_relevant_experience(user.experience, job_keywords)
        projects = self.filter_relevant_projects(user.projects, job_keywords)
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

