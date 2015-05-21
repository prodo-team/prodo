## Prodo Python Module

import sys

def fatal_err(msg): # stop execution and raise a fatal error at runtime
	msg = ":=  Oh No! Error:  " + msg
	bL = len(msg)
	print "\n"
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

def check_return_value(rt, fcn, val):
	if rt != type(val):
		fatal_err("Return value of subprogram " + fcn + "(..) is " + str(type(val)) + " but must be " + str(rt))
	else:
		return val

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

def loop_range(a, b, c = 1):
	if int(c) == 0:
		fatal_err("For loop incrementer must not be zero.")
	else:
		return range(a, b, c)

# The following are publicly accessible functions

def write_args_1(x): # print string value to screen
	check_args([str], [x], "write")
	sys.stdout.write(x)

def nl_args_0(): # print a new line
	check_args([], [], "nl")
	sys.stdout.write("\n")

def read_args_0(): # read from default system input stream (using Python)
	check_args([], [], "read")
	return raw_input("")

def length_args_1(x):
	check_args([list], [x], "length")
	return len(x)
