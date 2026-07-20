#decides which parser to use based on the file type
from .python_parser import PythonParser


class ParserFactory:

    _parsers = {
        "python": PythonParser(),
    }

    @classmethod
    def get_parser(cls, language: str):

        parser = cls._parsers.get(language.lower())

        if parser is None:
            raise ValueError(
                f"Parser for {language} not supported."
            )

        return parser