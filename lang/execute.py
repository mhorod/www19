from parse import *


class ExecutionContext:
    pass


def execute(node: ProgramNode):
    ctx = ExecutionContext()
    for expression in node.expressions:
        print(execute_expression(expression, ctx))


def execute_expression(expression: ExpressionNode, ctx: ExecutionContext):
    if type(expression) == TopLevelExpressionNode:
        return execute_expression(expression.expression, ctx)
    elif type(expression) == EmptyExpression:
        return None
    if type(expression) == IntNode:
        return execute_int(expression, ctx)
    elif type(expression) == FloatNode:
        return execute_float(expression, ctx)
    elif type(expression) == BoolNode:
        return execute_bool(expression, ctx)
    elif type(expression) == NameNode:
        return execute_name(expression, ctx)


def execute_int(node: IntNode, ctx: ExecutionContext):
    return node.value


def execute_float(node: FloatNode, ctx: ExecutionContext):
    return node.value


def execute_bool(node: BoolNode, ctx: ExecutionContext):
    return node.value


def execute_name(node: NameNode, ctx: ExecutionContext):
    raise InterpreterException(f'Undefined name {node.name} at {node.span}')
