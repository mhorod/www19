import logging

from lex import *
from parse import *
from analyze import *
from execute import *
from exception import *

logging.getLogger().setLevel(logging.DEBUG)


def run(text: str) -> ProgramNode:
    src = SourceCode('program', text)
    try:
        execute(analyze(parse(lex(src))))
    except InterpreterException as e:
        print(e)


src = '''
123; True; False; 3.14;;;;

'''

run(src)
