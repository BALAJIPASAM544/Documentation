from .parser_factory import ParserFactory


class ParserService:

    @staticmethod
    def parse(language: str, code: str):

        parser = ParserFactory.get_parser(language)

        return parser.parse(code)