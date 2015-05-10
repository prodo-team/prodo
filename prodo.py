## Prodo Python Module

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

def write(x): # print string value to screen
	if type(x) != type(""):
		fatal_err("Cannot write non-string value without explicit cast.")
	else:
		print x