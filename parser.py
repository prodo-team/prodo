import prodoParser as prodo

fin = open('testCode.prodo', 'r')
f_input = fin.read()

print str(f_input)

code = ""

code = prodo.parse('super', f_input)

fou = open('output.py', 'w')
fou.write(code)
