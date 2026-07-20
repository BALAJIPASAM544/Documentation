from pydantic import BaseModel
from typing import List

from .bug_schema import BugFinding
from .optimization_schema import OptimizationFinding
from .best_practices_schema import BestPracticeFinding
from .documentation_schema import DocumentationResponse


class ReviewSummary(BaseModel):
    overall_score: int
    bugs_found: int
    optimization_count: int
    best_practice_count: int


class ReviewResponse(BaseModel):

    summary: ReviewSummary

    bugs: List[BugFinding]

    optimizations: List[OptimizationFinding]

    best_practices: List[BestPracticeFinding]

    documentation: DocumentationResponse