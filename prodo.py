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

def prodo_type(t):
	if t == int:
		return "int"
	elif t == float:
		return "real"
	elif t == str:
		return "str"
	elif t == list:
		return "array"
	elif t == type(None):
		return "void"
	elif t == bool:
		return "bool"
	else:
		return "<?>"

def assign(l, r): # assign r to l, returns r if type is correct
	if (type(r) == type(l)):
		return r
	else:
		fatal_err("Assignment Error! Cannot assign " + prodo_type(type(r)) + " to " + prodo_type(type(l)) + ".")

def check_args(types, args, name):
	if len(types) != len(args):
		fatal_err("Argument Error! Subprogram " + name + "(..) expects " + str(len(types)) + " arguments but got " + str(len(args)))
	else:
		for i in range(0, len(types)):
			if types[i] != type(args[i]):
				fatal_err("Argument Error! Argument # " + str(i+1) + " in subprogram " + name + "(..) is " + prodo_type(type(args[i])) + " but " + prodo_type(types[i]) + " was expected.")

def check_return_value(rt, fcn, val):
	if rt != type(val):
		fatal_err("Conclusion Error! Return value of subprogram " + fcn + "(..) is " + prodo_type(type(val)) + " but must be " + prodo_type(rt))
	else:
		return val

def logical_and(x, y):
	if (type(x) != type(True) or type(y) != type(True)):
		fatal_err("Logical Operator Error! Cannot logically and non-boolean expressions. Cast to bool first.")
	else:
		return (x and y)

def logical_or(x, y):
	if (type(x) != type(True) or type(y) != type(True)):
		fatal_err("Logical Operator Error! Cannot logically (inclusive) or non-boolean expressions. Cast to bool first.")
	else:
		return (x or y)

def logical_xor(x, y):
	if (type(x) != type(True) or type(y) != type(True)):
		fatal_err("Logical Operator Error! Cannot logically xor non-boolean expressions. Cast to bool first.")
	else:
		return (x != y)

def loop_range(a, b, c = 1):
	#check_args([int, int, int], [a, b, c], "or structure for")
	if c == 0:
		fatal_err("For Loop Increment Error! For loop incrementer must not be zero.")
	else:
		 while a < b or b > a:
		    yield a
		    a += c
	return

# The following are publicly accessible functions

def write_args_1(x): # print string value to screen
	check_args([str], [x], "write")
	sys.stdout.write(x)

def nl_args_0(): # print a new line
	check_args([], [], "nl")
	sys.stdout.write("\n")

def read_args_0(): # read from default system input stream (using Python)
	check_args([], [], "read")
	return raw_input("") # returns a string

def length_args_1(x): # get the length of an array
	check_args([list], [x], "length")
	return len(x)

def affix_args_2(array, element): # affix element to the end of array
	check_args([list], [array], "affix")
	new_array = array + [element]
	return new_array

def f_read_args_1(filename):
	check_args([str], [filename], "f_read")
	lines = []
	try:
		f = open(filename)
		lines = f.readlines()
	except:
		fatal_err("File Read Error! The file \"" + filename + "\" could not be read.")
	else:
		return lines

def f_write_args_2(filename, contents):
	check_args([str,str], [filename,contents], "f_write")
	try:
		f = open(filename, "w")
		f.write(contents)
	except:
		fatal_err("File Write Error! The file \"" + filename + "\" could not be written into.")
