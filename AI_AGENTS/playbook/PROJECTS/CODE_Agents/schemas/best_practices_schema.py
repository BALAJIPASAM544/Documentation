from pydantic import BaseModel
from typing import List


class BestPracticeFinding(BaseModel):
    title: str
    category: str
    severity: str
    line: int
    issue: str
    recommendation: str
    reference: str


class BestPracticeResponse(BaseModel):
    agent: str = "best_practice_agent"
    status: str = "SUCCESS"
    findings: List[BestPracticeFinding]