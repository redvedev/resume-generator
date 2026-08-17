from pydantic import BaseModel


class UserFitResponse(BaseModel):
    fit_score: float


class JobNotesResponse(BaseModel):
    notes: str
