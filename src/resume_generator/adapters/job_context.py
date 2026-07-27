class JobKeywordFilter:
    def __init__(self, job_description: str, user: User):
        self.job_description = job_description
        self.user = user

    def filter_user_info(self, job_keywords: list[str]) -> User:
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
