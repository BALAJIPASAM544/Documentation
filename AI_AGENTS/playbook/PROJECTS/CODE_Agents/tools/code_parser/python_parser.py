import ast

from .base_parser import BaseParser
from .parser_models import (
    ParseResult,
    FunctionInfo,
    ClassInfo,
    ImportInfo,
)


class PythonParser(BaseParser):

    def parse(self, code: str) -> ParseResult:

        try:
            tree = ast.parse(code)

        except SyntaxError as e:

            return ParseResult(
                language="python",
                syntax_valid=False,
                functions=[],
                classes=[],
                imports=[],
                errors=[
                    f"Line {e.lineno}: {e.msg}"
                ]
            )

        functions = []
        classes = []
        imports = []

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                functions.append(
                    FunctionInfo(
                        name=node.name,
                        line_number=node.lineno,
                        arguments=[
                            arg.arg for arg in node.args.args
                        ]
                    )
                )

            elif isinstance(node, ast.ClassDef):

                classes.append(
                    ClassInfo(
                        name=node.name,
                        line_number=node.lineno
                    )
                )

            elif isinstance(node, ast.Import):

                for alias in node.names:
                    imports.append(
                        ImportInfo(
                            module=alias.name
                        )
                    )

            elif isinstance(node, ast.ImportFrom):

                module = node.module or ""

                for alias in node.names:
                    imports.append(
                        ImportInfo(
                            module=f"{module}.{alias.name}"
                        )
                    )

        return ParseResult(
            language="python",
            syntax_valid=True,
            functions=functions,
            classes=classes,
            imports=imports,
            errors=[]
        )