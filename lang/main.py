import logging

from lex import *
from parse import *
from analyze import *
from execute import *

logging.getLogger().setLevel(logging.DEBUG)


def run(text: str) -> ProgramNode:
    src = SourceCode('program', text)
    try:
        execute(analyze(parse(lex(src))))
    except Exception as e:
        print(e)


src = '''
abc   let
3.14
True
False
if
then
else
;
.2137
== 2 2
'''

run(src)
