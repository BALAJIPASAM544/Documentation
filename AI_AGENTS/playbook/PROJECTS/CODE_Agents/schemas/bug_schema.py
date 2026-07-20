from pydantic import BaseModel
from typing import List


class BugFinding(BaseModel):
    title: str
    severity: str
    line: int
    issue: str
    recommendation: str


class BugResponse(BaseModel):
    agent: str = "bug_agent"
    status: str = "SUCCESS"
    findings: List[BugFinding]