#data base models that are used to parse the code and extract the relevant information. These models are used by the code parser to understand the structure of the code and extract the necessary information for further processing.

from pydantic import BaseModel
from typing import List


class FunctionInfo(BaseModel):
    name: str
    line_number: int
    arguments: List[str]


class ClassInfo(BaseModel):
    name: str
    line_number: int


class ImportInfo(BaseModel):
    module: str


class ParseResult(BaseModel):

    language: str

    syntax_valid: bool

    functions: List[FunctionInfo]

    classes: List[ClassInfo]

    imports: List[ImportInfo]

    errors: List[str]