from pydantic import BaseModel
from typing import List


class ResearchOutput(BaseModel):
    industry: str
    target_audience: List[str]
    pain_points: List[str]
    opportunities: List[str]