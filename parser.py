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

try:
    e = compile(code, '<string>', 'exec')
    exec(e)
except NameError:
    fatal_err("Name Error! Cannot use undeclared identifier/subprogram.")
except KeyError:
    fatal_err("Structure Member Not Found! Tried to access a non-existent member of a structure.")
except IndexError:
    fatal_err("Index Error! Tried to use an illegal index in array.")
except ValueError:
    fatal_err("Illegal Value! Detected use of illegal value in statement.")
except EOFError:
    fatal_err("Unexpected EOF! Reached EOF while looking for input.")
except SyntaxError:
    fatal_err("Syntax Error! A syntax error has caused an unexpected error in translation.")
except TypeError:
    fatal_err("Type Error! You tried to use an invalid type in assignment/operation.")
