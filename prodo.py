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

def check_args(types, args, name):
	if len(types) != len(args):
		fatal_err("Subprogram " + name + "(..) expects " + str(len(types)) + " arguments but got " + str(len(args)))
	else:
		for i in range(0, len(types)):
			if types[i] != type(args[i]):
				fatal_err("Argument # " + str(i+1) + " in subprogram " + name + "(..) is " + str(type(args[i])) + " but " + str(types[i]) + " was expected.")


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

def write(args): # print string value to screen
	check_args([str], args, "write")
	[x] = args
	sys.stdout.write(x)

def nl(args): # print a new line
	check_args([], args, "nl")
	sys.stdout.write("\n")

def read(args): # read from default system input stream (using Python)
	check_args([], args, "read")
	return str(input(""))

def loop_range(a, b, c = 1):
	if int(c) == 0:
		fatal_err("For loop incrementer must not be zero.")
	else:
		return range(a, b, c)

def length(args):
	check_args([list], args, "length")
	[x] = args
	return len(x)
