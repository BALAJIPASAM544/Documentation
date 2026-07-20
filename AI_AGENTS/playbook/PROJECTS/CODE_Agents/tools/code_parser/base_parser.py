from abc import ABC, abstractmethod

from .parser_models import ParseResult


class BaseParser(ABC):

    @abstractmethod
    def parse(self, code: str) -> ParseResult:
        pass