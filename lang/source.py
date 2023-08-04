from dataclasses import dataclass


@dataclass
class SourceCode:
    name: str
    text: str


@dataclass
class Span:
    src: SourceCode
    begin: int
    end: int
