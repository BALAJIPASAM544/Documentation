from pydantic import BaseModel
from typing import List


class FunctionDoc(BaseModel):
    name: str
    description: str
    parameters: List[str]
    returns: str


class DocumentationResponse(BaseModel):
    agent: str = "documentation_agent"
    status: str = "SUCCESS"

    summary: str

    functions: List[FunctionDoc]

    time_complexity: str

    space_complexity: str

    usage_example: str