import logging
from dataclasses import dataclass
from enum import Enum, auto

from source import *


class TokenType(Enum):
    NUMBER_OR_NAME = auto()
    WHITESPACE = auto()
    SYMBOL = auto()
    OPERATOR = auto()
    UNKNOWN = auto()

    KEYWORD = auto()
    INT = auto()
    FLOAT = auto()
    NAME = auto()
    BOOL = auto()


@dataclass
class Token:
    span: Span
    text: str
    token_type: TokenType

    def __str__(self):
        return f"{self.span.begin}:{self.span.end} {self.token_type.name}({self.text})"


class TextCursor:
    def __init__(self, src: SourceCode):
        self.src = src
        self.index = 0
        self.span_index = 0

    def peek(self, n) -> str:
        return self.src.text[self.index:self.index + n]

    def next(self, n) -> str:
        text = self.peek(n)
        self.index += n
        return text

    def get_span(self):
        span = Span(self.src, self.span_index, self.index)
        self.span_index = self.index
        return span

    def is_empty(self):
        return self.index >= len(self.src.text)


def lex(src: SourceCode) -> list[Token]:
    tokens = []
    cursor = TextCursor(src)
    while not cursor.is_empty():
        if is_number_or_name_char(cursor.peek(1)):
            token = lex_number_or_name(cursor)
            tokens.append(token)
            logging.debug("Lexed number: " + str(token))
        elif is_whitespace(cursor.peek(1)):
            lex_whitespace(cursor)
        elif is_symbol(cursor.peek(1)):
            token = lex_symbol(cursor)
            tokens.append(token)
            logging.debug("Lexed symbol: " + str(token))
        elif is_operator(cursor.peek(1)):
            token = lex_operator(cursor)
            tokens.append(token)
            logging.debug("Lexed operator: " + str(token))
        else:
            token = lex_unknown(cursor)
            tokens.append(token)
            logging.debug("Lexed unknown: " + str(token))
    return validate(tokens)


def is_number_or_name_char(c):
    return c != "" and (c in "_.0123456789" or c.isalpha())


def lex_number_or_name(cursor):
    text = ""
    while is_number_or_name_char(cursor.peek(1)):
        text += cursor.next(1)
    return Token(cursor.get_span(), text, TokenType.NUMBER_OR_NAME)


def is_whitespace(c):
    return c.isspace()


def lex_whitespace(cursor):
    text = ""
    while is_whitespace(cursor.peek(1)):
        text += cursor.next(1)
    return Token(cursor.get_span(), text, TokenType.WHITESPACE)


def is_symbol(c):
    return c != "" and c in "()[]{},;"


def lex_symbol(cursor):
    text = cursor.next(1)
    return Token(cursor.get_span(), text, TokenType.SYMBOL)


def is_operator(c):
    return c != "" and c in "+-*/%="


def lex_operator(cursor):
    text = ""
    while is_operator(cursor.peek(1)):
        text += cursor.next(1)
    return Token(cursor.get_span(), text, TokenType.OPERATOR)


def lex_unknown(cursor):
    text = cursor.next(1)
    return Token(cursor.get_span(), text, TokenType.UNKNOWN)


def validate(tokens: list[Token]) -> list[Token]:
    return [validate_token(token) for token in tokens]


def validate_token(token: Token) -> Token:
    if token.token_type == TokenType.NUMBER_OR_NAME:
        token = validate_number_or_name(token)
    elif token.token_type == TokenType.UNKNOWN:
        token = validate_unknown(token)
    logging.debug("Validated token: " + str(token))
    return token


def validate_number_or_name(token: Token):
    if token.text in {"let", "if", "then", "else"}:
        return Token(token.span, token.text, TokenType.KEYWORD)
    elif token.text in {"True", "False"}:
        return Token(token.span, token.text, TokenType.BOOL)
    elif is_int(token.text):
        return Token(token.span, token.text, TokenType.INT)
    elif is_float(token.text):
        return Token(token.span, token.text, TokenType.FLOAT)
    elif is_name(token.text):
        return Token(token.span, token.text, TokenType.NAME)
    else:
        raise Exception(f"Invalid token: {token}")


def validate_unknown(token: Token):
    raise Exception(f"Invalid token: {token}")


def is_float(text: str) -> bool:
    try:
        float(text)
        return True
    except ValueError:
        return False


def is_int(text: str) -> bool:
    try:
        int(text)
        return True
    except ValueError:
        return False


def is_name(text: str) -> bool:
    return text.isidentifier()
