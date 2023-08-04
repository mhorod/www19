from dataclasses import dataclass

import logging

from lex import *
from source import Span
from exception import *


@dataclass
class ExpressionNode:
    pass


@dataclass
class EmptyExpression(ExpressionNode):
    span: Span

    def __str__(self) -> str:
        return f"{self.span.begin}:{self.span.end} EmptyExpression()"


@dataclass
class TopLevelExpressionNode(ExpressionNode):
    expression: ExpressionNode
    span: Span

    def __str__(self) -> str:
        return f"{self.span.begin}:{self.span.end} TopLevelExpressionNode({self.expression})"


@dataclass
class IntNode(ExpressionNode):
    value: int
    span: Span

    def __str__(self) -> str:
        return f"{self.span.begin}:{self.span.end} IntNode({self.value})"


@dataclass
class FloatNode(ExpressionNode):
    value: float
    span: Span

    def __str__(self) -> str:
        return f"{self.span.begin}:{self.span.end} FloatNode({self.value})"


@dataclass
class BoolNode(ExpressionNode):
    value: bool
    span: Span

    def __str__(self) -> str:
        return f"{self.span.begin}:{self.span.end} BoolNode({self.value})"


@dataclass
class NameNode(ExpressionNode):
    name: str
    span: Span

    def __str__(self) -> str:
        return f"{self.span.begin}:{self.span.end} NameNode({self.name})"


@dataclass
class ProgramNode:
    expressions: list[ExpressionNode]
    span: Span

    def __str__(self) -> str:
        expression_text = ", ".join([str(expression)
                                    for expression in self.expressions])
        expression_text = f"[{expression_text}]"
        return f"{self.span.begin}:{self.span.end} ProgramNode({expression_text})"


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

    def next_one(self) -> Token:
        token = self.peek_one()
        self.index += 1
        return token

    def next(self, n) -> list[Token]:
        tokens = self.peek(n)
        self.index += n
        return tokens

    def is_empty(self):
        return self.index >= len(self.tokens)


def parse(tokens: list[Token]) -> ProgramNode:
    cursor = TokenCursor(tokens)
    expressions = []
    while not cursor.is_empty():
        if cursor.peek_one().token_type == TokenType.EOF:
            break
        expression = parse_top_level_expression(cursor)
        expressions.append(expression)
        logging.debug("Parsed top-level expression: " + str(expression))
    span = merge_spans(expressions[0].span, expressions[-1].span)
    program = ProgramNode(expressions, span)
    logging.debug("Parsed program: " + str(program))
    return program


def parse_top_level_expression(cursor: TokenCursor) -> ExpressionNode:
    if cursor.peek_one().text == ";":
        semicolon = parse_semicolon(cursor)
        return EmptyExpression(semicolon.span)
    expression = parse_expression(cursor)
    semicolon = parse_semicolon(cursor)
    span = merge_spans(expression.span, semicolon.span)
    return TopLevelExpressionNode(expression, span)


def parse_expression(cursor: TokenCursor) -> ExpressionNode:
    if cursor.peek_one().token_type == TokenType.INT:
        node = parse_int(cursor)
        logging.debug("Parsed int: " + str(node))
        return node
    elif cursor.peek_one().token_type == TokenType.FLOAT:
        node = parse_float(cursor)
        logging.debug("Parsed float: " + str(node))
        return node
    elif cursor.peek_one().token_type == TokenType.BOOL:
        node = parse_bool(cursor)
        logging.debug("Parsed bool: " + str(node))
        return node
    elif cursor.peek_one().token_type == TokenType.NAME:
        node = parse_name(cursor)
        logging.debug("Parsed name: " + str(node))
        return node
    else:
        raise InterpreterException(
            f"Expected expression, found {cursor.peek_one()}")


def merge_spans(span1: Span, span2: Span) -> Span:
    return Span(span1.src, span1.begin, span2.end)


def parse_int(cursor: TokenCursor) -> IntNode:
    token = cursor.next_one()
    return IntNode(int(token.text), token.span)


def parse_float(cursor: TokenCursor) -> FloatNode:
    token = cursor.next_one()
    return FloatNode(float(token.text), token.span)


def parse_bool(cursor: TokenCursor) -> BoolNode:
    token = cursor.next_one()
    value = True if token.text == "True" else False
    return BoolNode(value, token.span)


def parse_name(cursor: TokenCursor) -> NameNode:
    token = cursor.next_one()
    return NameNode(token.text, token.span)


def parse_semicolon(cursor: TokenCursor) -> TokenNode:
    if cursor.is_empty():
        raise InterpreterException("Unexpected EOF while parsing semicolon")
    else:
        token = cursor.next_one()
        if token.text == ';':
            return TokenNode(token, token.span)
        else:
            raise InterpreterException("Expected semicolon")
