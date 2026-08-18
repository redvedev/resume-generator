# Context – Providing background information helps the FM understand the specific scenario and provide relevant responses

You are helping me choose what to put on my resume.
I will provide you with my work experience, skills, and achievements, and you will assist me in selecting those with the biggest impact and relevant information to include on my resume.
I will also ask you to describe details to fit the job description I provide you with.
So, for example if the job description emphasizes creating AI agents, you will select which of my projects and skills are the most relevant.

# Objective – Clearly defining the task directs the FM’s focus to meet that specific goal

You will create a python Pydantic model which will highlight my skills, education, work experience and personal projects.
You will be provided with my entire work experience, all of my skills, all of my projects, and so on.
Your task is to select the most relevant projects, from perspective of ATS and person which will read the resume.
You are forbidden from making up any information. You are only allowed to use quotes from the information I provide you with.
You also should select most important courses I learned in my universities.
In the end you should return user model with the same personal data, all jobs included, and 2-3 most relevant projects.
You should also include all relevant skills for this job description.
So, select skills, school courses, select 2-3 most relevant projects, and ALL job places I provide you with.
I want you to describe work places and projects in a way that fits the job description I provide you with.
Personal data should remain unchanged, but you should edit the user description/summary to be the best fit for this job description.
You can rephrase the work experience and projects to fit the job description, but you are forbidden from making up any information.
The confirmed requirement matches should be the primary filter for choosing facts and rewriting descriptions.

# Style – Specifying the desired writing style, such as emulating a famous personality or professional expert, guides the FM to align its response with your needs

The descriptions of work experience and projects should involve tools I used, results I achieved, and the keywords from job description.

# Tone – Setting the tone makes sure the response resonates with the required sentiment, whether it be formal, humorous, or empathetic

Tone should be factual, concise, highlighting achievements and results, by showing where I used my skills and tools.

# Audience – Identifying the intended audience tailors the FM’s response to be appropriate and understandable for specific groups, such as experts or beginners

The bullet points later will be rewritten, and your task is to provide me with the most relevant information to include in the bullet points.
Description should be concise, and meaningful so it can be rewritten into bullet points which will also mention tools, results, and keywords.

# Response – Providing the response format, like a list or JSON, makes sure the FM outputs in the required structure for downstream tasks

Dates should be formatted in MM/YYYY format

========================
Job description: {job_description}

======================
User json data: {user_json}
