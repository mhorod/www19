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

    def __str__(self):
        return f'{self.src.name}:{self.begin}:{self.end}'
