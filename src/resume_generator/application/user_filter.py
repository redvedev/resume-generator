from resume_generator.application.agent_invoker import AgentInvoker
from resume_generator.domains.experience import Experience
from resume_generator.domains.project import Project
from resume_generator.domains.user import User


class UserFilter:
    def __init__(self, agent: AgentInvoker) -> None:
        self.keywords: list[str] = []
        self.agent = agent

    def _extract_keywords(self, job_description: str):
        self.keywords = []

    def _select_projects(self, source_projects: list[Project]) -> list[Project]:
        projects = []
        for project in source_projects:
            for keyword in self.keywords:
                for bullet_point in project.actions:
                    if keyword.lower() in bullet_point.lower():
                        projects.append(project)
        projects_summary = self.agent.get_user_projects_summary(projects)
        result_projects: list[Project] = [p for p in projects]
        for p_origin in result_projects:
            for p_summary in projects_summary.projects:
                if p_origin.project_id != p_summary.project_id:
                    continue
                p_origin.description = p_summary.description
                p_origin.actions = p_summary.bullets

        return result_projects
