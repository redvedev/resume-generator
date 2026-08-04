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


class LatexRenderer:
    def __init__(self) -> None:
        self.row_break = "\\\\"

    def render_skill(self, skill: LatexSkill) -> str:
        return f"{skill.category} & {", ".join(skill.skills)}"

    def render_skills(self, skills: LatexSkills) -> str:
        header = r"\begin{tabularx}{\textwidth}{@{}>{\bfseries}l@{\hspace{2ex}}>{\RaggedRight\arraybackslash}X@{}}"
        separator = f"{self.row_break}\n"
        skills_list = separator.join([self.render_skill(s) for s in skills.skills])
        end = r"\end{tabularx}"
        return f"{header}\n{skills_list}\n{end}\n"

    def render_school(self, school: LatexSchool) -> str:
        block_lines = [
            "\\noindent",
            "\\begin{tabular*}{\\textwidth}{@{}l@{\\extracolsep{\\fill}}r@{}}",
            f"\\textbf{{{school.degree}}} & {school.dates} {self.row_break}",
            "\\end{tabular*}",
            "\\noindent",
            "\\begin{tabular*}{\\textwidth}{@{}l@{\\extracolsep{\\fill}}r@{}}",
            f"\\textit{{{school.name}}} {self.row_break}",
            "\\end{tabular*}",
            "\\noindent",
            f"Relevant Coursework: {", ".join(school.courses)}",
        ]
        return "\n".join(block_lines) + "\n\n"

    def render_schools(self, schools: LatexSchools) -> str:
        return "".join(self.render_school(s) for s in schools.schools)

    def render_job(self, job: LatexJob) -> str:
        block_lines = [
            "\\noindent",
            "\\begin{tabular*}{\\textwidth}{@{}l@{\\extracolsep{\\fill}}r@{}}",
            f"\\textbf{{{job.position}}} & {job.dates} {self.row_break}",
            "\\end{tabular*}",
            "\\noindent",
            "\\begin{tabular*}{\\textwidth}{@{}l@{\\extracolsep{\\fill}}r@{}}",
            f"\\textit{{{job.company}}} & \\textit{{{job.location}}} {self.row_break}",
            "\\end{tabular*}",
        ]

        bullet_block_lines = [
            "\\begin{itemize}[leftmargin=*,labelsep=0.5em,itemsep=-0.5em,topsep=0pt]",
        ]
        for bullet in job.bullet_points:
            bullet_block_lines.append(f"\\item {bullet}")

        bullet_block_lines.append("\\end{itemize}")
        block = "\n".join(block_lines)
        bullets = "\n".join(bullet_block_lines)
        return f"{block}\n{bullets}"

    def render_jobs(self, jobs: LatexJobs) -> str:
        separator = "\n\n"
        return separator.join(self.render_job(j) for j in jobs.jobs)

    def render_project(self, project: LatexProject) -> str:
        block_lines = [
            f"\\noindent \\textbf{{{project.name}}} - {project.project_type} \\hfill {project.year}{self.row_break}",
            f"\\textbf{{Description}}: {project.description}{self.row_break}",
            f"\\textbf{{Technologies}}: {project.technologies}",
        ]
        bullet_lines = [
            "\\begin{itemize}[leftmargin=*,labelsep=0.5em,itemsep=-0.5em,topsep=0pt]",
        ]
        bullet_lines.extend([f"\\item {bullet}" for bullet in project.bullet_points])
        bullet_lines.append("\\end{itemize}")

        block = "\n".join(block_lines)
        bullets = "\n".join(bullet_lines)
        return f"{block}\n{bullets}"

    def render_projects(self, projects: LatexProjects) -> str:
        separator = "\n\n"
        return separator.join(self.render_project(p) for p in projects.projects)
