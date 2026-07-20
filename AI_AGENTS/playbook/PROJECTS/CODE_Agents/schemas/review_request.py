from pydantic import BaseModel


class ReviewRequest(BaseModel):
    language: str
    filename: str
    code: str