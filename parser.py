import prodoParser
from prodo import *
# note: prodo imports 'sys'

DEBUG = False

if len(sys.argv) < 2:
    fatal_err("Please supply a filename. ")

fin = open(sys.argv[1], 'r')
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
    fou = open('prodo_output.py', 'w')
    fou.write(code)

e = compile(code, '<string>', 'exec')
exec(e)

#try:
#    e = compile(code, '<string>', 'exec')
#    exec(e)
#except NameError:
#    fatal_err("Cannot use undeclared identifier.")
