from pydantic import BaseModel
from typing import List


class OptimizationFinding(BaseModel):
    title: str
    category: str
    severity: str
    line: int
    issue: str
    suggestion: str
    benefit: str


class OptimizationResponse(BaseModel):
    agent: str = "optimization_agent"
    status: str = "SUCCESS"
    findings: List[OptimizationFinding]