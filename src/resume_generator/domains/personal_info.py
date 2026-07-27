from pydantic import BaseModel, Field


class PersonalInfo(BaseModel):
    name: str = Field(alias="name")
    phone_number: str = Field(alias="phone")
    location: str = Field(alias="location")
    email: str = Field(alias="email")
    linkedin_preview_link: str = Field(alias="linkedin_preview")
    linkedin_actual_link: str = Field(alias="linkedin_url")
    website: str = Field(alias="website")
