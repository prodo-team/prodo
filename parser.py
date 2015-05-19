import prodoParser
from prodo import *

DEBUG = False

fin = open('testCode.prodo', 'r')
f_input = fin.read()

if DEBUG:
    print str(f_input)

code = ""

try:
    code = prodoParser.parse('super', f_input)
except TypeError:
    fatal_err("A syntactic error has been encountered.")

if DEBUG:
    print code

fou = open('output.py', 'w')
fou.write(code)

try:
    e = compile(code, '<string>', 'exec')
    exec(e)
except NameError:
    fatal_err("Cannot use undeclared identifier.")
