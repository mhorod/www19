from dataclasses import dataclass

import logging

from lex import *
from source import Span


@dataclass
class ExpressionNode:
    pass


@dataclass
class TopLevelExpressionNode(ExpressionNode):
    expression: ExpressionNode
    span: Span


@dataclass
class IntNode(ExpressionNode):
    value: int
    span: Span


@dataclass
class ProgramNode:
    expressions: list[ExpressionNode]
    span: Span


@dataclass
class TokenNode:
    token: Token
    span: Span


class TokenCursor:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.src = tokens[0].span.src
        self.index = 0
        self.span_index = 0

    def peek_one(self) -> Token:
        return self.tokens[self.index]

    def peek(self, n) -> list[Token]:
        return self.tokens[self.index:self.index + n]

    def next(self, n) -> str:
        tokens = self.peek(n)
        self.index += n
        return tokens

    def is_empty(self):
        return self.index >= len(self.tokens)


def parse(tokens: list[Token]) -> ProgramNode:
    cursor = TokenCursor(tokens)
    expressions = []
    while not cursor.is_empty():
        expression = parse_top_level_expression(cursor)
        expressions.append(expression)
        logging.debug("Parsed top-level expression: " + str(expression))
    return ProgramNode(expressions, cursor.get_span())


def parse_top_level_expression(cursor: TokenCursor) -> ExpressionNode:
    expression = parse_expression(cursor)
    semicolon = parse_semicolon(cursor)
    span = merge_spans(expression.span, semicolon.span)
    return TopLevelExpressionNode(expression, span)


def parse_expression(cursor: TokenCursor) -> ExpressionNode:
    if cursor.peek_one().token_type == TokenType.INT:
        node = parse_int(cursor)
        logging.debug("Parsed int: " + str(node))
        return node
    else:
        raise Exception("Expected top-level expression")


def merge_spans(span1: Span, span2: Span) -> Span:
    pass


def parse_int(cursor: TokenCursor) -> IntNode:
    pass


def parse_semicolon(cursor: TokenCursor) -> TokenNode:
    pass
