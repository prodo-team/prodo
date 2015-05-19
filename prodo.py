## Prodo Python Module

import sys

def fatal_err(msg): # stop execution and raise a fatal error at runtime
	msg = ":=  Oh No! Error:  " + msg
	bL = len(msg)
	print "-" * bL
	print msg
	print "-" * bL
	exit()

def assign(l, r): # assign r to l, returns r if type is correct
	if (type(r) == type(l)):
		return r
	else:
		fatal_err("Cannot assign " + type(l) + " to " + type(r) + ".")

def logical_and(x, y):
	if (type(x) != type(True) or type(y) != type(True)):
		fatal_err("Cannot logically and non-boolean expressions. Cast to bool first.")
	else:
		return (x and y)

def logical_or(x, y):
	if (type(x) != type(True) or type(y) != type(True)):
		fatal_err("Cannot logically (inclusive) or non-boolean expressions. Cast to bool first.")
	else:
		return (x or y)

def logical_xor(x, y):
	if (type(x) != type(True) or type(y) != type(True)):
		fatal_err("Cannot logically xor non-boolean expressions. Cast to bool first.")
	else:
		return (x != y)

def write(x): # print string value to screen
	if type(x) != type(""):
		fatal_err("Cannot write non-string value without explicit cast.")
	else:
		sys.stdout.write(x)

def nl(): # print a new line
	sys.stdout.write("\n")

def read(): # read from default system input stream (using Python)
	return input("")

def loop_range(a, b, c = 1):
	if int(c) == 0:
		fatal_err("For loop incrementer must not be zero.")
	else:
		return range(a, b, c)

def length(x):
	if type(x) != type([]):
		fatal_err("Cannot find length of non-array value")
	else:
		return len(x)
