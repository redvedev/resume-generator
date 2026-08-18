from pydantic import BaseModel


class Offer(BaseModel):
    linkedin_url: str
    linkedin_id: str
    description: str
    location: str
    job_title: str
    tags: list[str]
    company_name: str
