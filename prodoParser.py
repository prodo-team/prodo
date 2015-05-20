#!/usr/bin/python2

# Begin -- grammar generated by Yapps
from __future__ import print_function
import sys, re
from yapps import runtime

class ProdoScanner(runtime.Scanner):
    patterns = [
        ("'loop'", re.compile('loop')),
        ("'while'", re.compile('while')),
        ("'by '", re.compile('by ')),
        ("'to'", re.compile('to')),
        ("'for'", re.compile('for')),
        ("'>='", re.compile('>=')),
        ("'<='", re.compile('<=')),
        ("'>'", re.compile('>')),
        ("'<'", re.compile('<')),
        ("'!='", re.compile('!=')),
        ("'=='", re.compile('==')),
        ("'not'", re.compile('not')),
        ("'xor'", re.compile('xor')),
        ("'or'", re.compile('or')),
        ("'and'", re.compile('and')),
        ("'0'", re.compile('0')),
        ("'1'", re.compile('1')),
        ("'no'", re.compile('no')),
        ("'yes'", re.compile('yes')),
        ("'else'", re.compile('else')),
        ("'elseif'", re.compile('elseif')),
        ("'\\\\|'", re.compile('\\|')),
        ("'if'", re.compile('if')),
        ("'stop'", re.compile('stop')),
        ("'next'", re.compile('next')),
        ("'conclude'", re.compile('conclude')),
        ("'end'", re.compile('end')),
        ('"fcn"', re.compile('fcn')),
        ("'-'", re.compile('-')),
        ('"\\\\]"', re.compile('\\]')),
        ('"\\\\["', re.compile('\\[')),
        ("'nil'", re.compile('nil')),
        ('"%"', re.compile('%')),
        ('"/"', re.compile('/')),
        ("r'[*]'", re.compile('[*]')),
        ('"-"', re.compile('-')),
        ("r'[+]'", re.compile('[+]')),
        ("','", re.compile(',')),
        ('","', re.compile(',')),
        ("'\\\\}'", re.compile('\\}')),
        ("'\\\\{'", re.compile('\\{')),
        ('"-="', re.compile('-=')),
        ('r"[+]="', re.compile('[+]=')),
        ('"%="', re.compile('%=')),
        ('"/="', re.compile('/=')),
        ('r"[*]="', re.compile('[*]=')),
        ('":="', re.compile(':=')),
        ("':='", re.compile(':=')),
        ('"--"', re.compile('--')),
        ('r"[+][+]"', re.compile('[+][+]')),
        ('"\\\\)"', re.compile('\\)')),
        ('"\\\\("', re.compile('\\(')),
        ("r'[~](.)*'", re.compile('[~](.)*')),
        ("'enum'", re.compile('enum')),
        ("'structure'", re.compile('structure')),
        ("'array'", re.compile('array')),
        ("'str'", re.compile('str')),
        ("'real'", re.compile('real')),
        ("'int'", re.compile('int')),
        ("'bool'", re.compile('bool')),
        ("'void'", re.compile('void')),
        ("''", re.compile('')),
        ('END', re.compile('$')),
        ('NEWLINE', re.compile('([\\n])+')),
        ('INT', re.compile('([0-9])+|([-][0-9])+')),
        ('REAL', re.compile('[0-9]+[.][0-9]+|[-][0-9]+[.][0-9]+')),
        ('STRING', re.compile('"([^\\\\"]+|\\\\.)*"')),
        ('ID', re.compile('[a-zA-Z]([a-zA-Z0-9$_@])*')),
        ('TYPE', re.compile('[a-zA-Z_]')),
        (' ', re.compile(' ')),
        ('[~](.)*', re.compile('[~](.)*')),
    ]
    def __init__(self, str,*args,**kw):
        runtime.Scanner.__init__(self,None,{' ':None,'[~](.)*':None,},str,*args,**kw)

class Prodo(runtime.Parser):
    Context = runtime.Context
    def super(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'super', [])
        global header
        global indents
        global listCount
        header = ''
        indents = 0
        listCount = 0
        code = ''
        while self._peek('END', "r'[~](.)*'", '"fcn"', "'conclude'", "'next'", "'stop'", "'if'", "'for'", "'while'", "'loop'", "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', 'ID', context=_context) != 'END':
            statement_upper = self.statement_upper(_context)
            ender = self.ender(_context)
            code += statement_upper
        END = self._scan('END', context=_context)
        return header + code

    def ender(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'ender', [])
        _token = self._peek('NEWLINE', "''", context=_context)
        if _token == 'NEWLINE':
            NEWLINE = self._scan('NEWLINE', context=_context)
        else: # == "''"
            self._scan("''", context=_context)

    def type_name(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'type_name', [])
        _token = self._peek("'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', context=_context)
        if _token == "'void'":
            self._scan("'void'", context=_context)
            return 'void'
        elif _token == "'bool'":
            self._scan("'bool'", context=_context)
            return 'bool'
        elif _token == "'int'":
            self._scan("'int'", context=_context)
            return 'int'
        elif _token == "'real'":
            self._scan("'real'", context=_context)
            return 'float'
        elif _token == "'str'":
            self._scan("'str'", context=_context)
            return 'str'
        elif _token == "'array'":
            self._scan("'array'", context=_context)
            return 'list'
        elif _token == "'structure'":
            self._scan("'structure'", context=_context)
            return 'dict'
        elif _token == "'enum'":
            self._scan("'enum'", context=_context)
            return 'enum '
        else: # == 'TYPE'
            TYPE = self._scan('TYPE', context=_context)
            return TYPE

    def statement_upper(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'statement_upper', [])
        _token = self._peek("r'[~](.)*'", '"fcn"', "'conclude'", "'next'", "'stop'", "'if'", "'for'", "'while'", "'loop'", "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', 'ID', context=_context)
        if _token not in ["r'[~](.)*'", '"fcn"', "'conclude'", "'next'", "'stop'", "'if'", "'for'", "'while'", "'loop'"]:
            exp_statement = self.exp_statement(_context)
            return exp_statement
        elif _token == '"fcn"':
            fcn_definition = self.fcn_definition(_context)
            return fcn_definition
        elif _token not in ["r'[~](.)*'", "'if'", "'for'", "'while'", "'loop'"]:
            jump_statement = self.jump_statement(_context)
            return jump_statement
        elif _token == "'if'":
            conditional_statement = self.conditional_statement(_context)
            return conditional_statement
        elif _token != "r'[~](.)*'":
            iterative_statement = self.iterative_statement(_context)
            return iterative_statement
        else: # == "r'[~](.)*'"
            self._scan("r'[~](.)*'", context=_context)
            return "\n"

    def statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'statement', [])
        _token = self._peek("r'[~](.)*'", "'conclude'", "'next'", "'stop'", "'if'", "'for'", "'while'", "'loop'", "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', 'ID', context=_context)
        if _token not in ["r'[~](.)*'", "'conclude'", "'next'", "'stop'", "'if'", "'for'", "'while'", "'loop'"]:
            exp_statement = self.exp_statement(_context)
            return exp_statement
        elif _token not in ["r'[~](.)*'", "'if'", "'for'", "'while'", "'loop'"]:
            jump_statement = self.jump_statement(_context)
            return jump_statement
        elif _token == "'if'":
            conditional_statement = self.conditional_statement(_context)
            return conditional_statement
        elif _token != "r'[~](.)*'":
            iterative_statement = self.iterative_statement(_context)
            return iterative_statement
        else: # == "r'[~](.)*'"
            self._scan("r'[~](.)*'", context=_context)
            return "\n"

    def exp_statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'exp_statement', [])
        _token = self._peek("'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', 'ID', context=_context)
        if _token != 'ID':
            declaration_exp = self.declaration_exp(_context)
            return declaration_exp
        else: # == 'ID'
            identified_exp = self.identified_exp(_context)
            return identified_exp

    def identified_exp(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'identified_exp', [])
        identifier = self.identifier(_context)
        A = ""
        _token = self._peek('"\\\\("', 'r"[+][+]"', '"--"', '":="', 'r"[*]="', '"/="', '"%="', 'r"[+]="', '"-="', context=_context)
        if _token not in ['"\\\\("', 'r"[+][+]"', '"--"']:
            assignment_op = self.assignment_op(_context)
            O = assignment_op
            S = [identifier]
            additive_exp = self.additive_exp(_context)
            if (O != ""): additive_exp = identifier + assignment_op + additive_exp;
            for x in S: A += x + "=assign(" + x + "," + additive_exp + ")"
            return A + "\n"
        elif _token == '"\\\\("':
            self._scan('"\\\\("', context=_context)
            list_plain = self.list_plain(_context)
            self._scan('"\\\\)"', context=_context)
            global listCount
            return identifier + "_args_" + str(listCount) + "("+list_plain+")\n"
        elif _token == 'r"[+][+]"':
            self._scan('r"[+][+]"', context=_context)
            return identifier + "+=1\n"
        else: # == '"--"'
            self._scan('"--"', context=_context)
            return identifier + "--\n"

    def declaration_exp(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'declaration_exp', [])
        type_name = self.type_name(_context)
        A = ""
        list_identifiers = self.list_identifiers(_context)
        self._scan("':='", context=_context)
        A += list_identifiers
        additive_exp = self.additive_exp(_context)
        A += "=" + type_name + "("+additive_exp+")"
        return A + "\n"

    def identifier(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'identifier', [])
        ID = self._scan('ID', context=_context)
        ID = ID.replace("$", "_dol_")
        ID = ID.replace("@", "_at_")
        return ID

    def assignment_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'assignment_op', [])
        _token = self._peek('":="', 'r"[*]="', '"/="', '"%="', 'r"[+]="', '"-="', context=_context)
        if _token == '":="':
            self._scan('":="', context=_context)
            return ""
        elif _token == 'r"[*]="':
            self._scan('r"[*]="', context=_context)
            return "*"
        elif _token == '"/="':
            self._scan('"/="', context=_context)
            return "/"
        elif _token == '"%="':
            self._scan('"%="', context=_context)
            return "%"
        elif _token == 'r"[+]="':
            self._scan('r"[+]="', context=_context)
            return "+"
        else: # == '"-="'
            self._scan('"-="', context=_context)
            return "-"

    def list_literal(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'list_literal', [])
        self._scan("'\\\\{'", context=_context)
        list_plain = self.list_plain(_context)
        self._scan("'\\\\}'", context=_context)
        return '['+list_plain+']'

    def list_plain(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'list_plain', [])
        global listCount
        listCount = 0
        _token = self._peek("''", 'INT', 'REAL', "'\\\\{'", "'nil'", 'STRING', 'ID', "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', '"\\\\["', "'-'", context=_context)
        if _token != "''":
            additive_exp = self.additive_exp(_context)
            S = additive_exp; listCount += 1
            while self._peek('","', '"\\\\)"', "'\\\\}'", context=_context) == '","':
                self._scan('","', context=_context)
                additive_exp = self.additive_exp(_context)
                S += "," + additive_exp; listCount += 1
            return S
        else: # == "''"
            self._scan("''", context=_context)
            return ''

    def list_identifiers(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'list_identifiers', [])
        identifier = self.identifier(_context)
        S = identifier
        while self._peek("','", "':='", context=_context) == "','":
            self._scan("','", context=_context)
            identifier = self.identifier(_context)
            S += "=" + identifier
        return S

    def additive_exp(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'additive_exp', [])
        term = self.term(_context)
        S = term
        while self._peek("r'[+]'", '"-"', '"\\\\]"', '"\\\\)"', '","', "'to'", "'by '", "'\\\\|'", 'INT', 'REAL', "'\\\\{'", "'nil'", 'STRING', 'ID', "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', '"\\\\["', "'-'", "'=='", "'!='", "'<'", "'>'", "'<='", "'>='", "'and'", "'or'", "'xor'", "'\\\\}'", 'NEWLINE', "''", context=_context) in ["r'[+]'", '"-"']:
            _token = self._peek("r'[+]'", '"-"', context=_context)
            if _token == "r'[+]'":
                self._scan("r'[+]'", context=_context)
                term = self.term(_context)
                S += "+" + term
            else: # == '"-"'
                self._scan('"-"', context=_context)
                term = self.term(_context)
                S += "-" + term
        return S

    def cast_exp(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'cast_exp', [])
        type_name = self.type_name(_context)
        while 1:
            self._scan('"\\\\("', context=_context)
            if self._peek('"\\\\("', 'INT', 'REAL', "'\\\\{'", "'nil'", 'STRING', 'ID', "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', '"\\\\["', "'-'", context=_context) != '"\\\\("': break
        while 1:
            additive_exp = self.additive_exp(_context)
            if self._peek('INT', 'REAL', "'\\\\{'", "'nil'", 'STRING', 'ID', "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', '"\\\\["', "'-'", '"\\\\)"', '"\\\\]"', '","', "'to'", "'by '", "'\\\\|'", "'=='", "'!='", "'<'", "'>'", "'<='", "'>='", "'and'", "'or'", "'xor'", "'\\\\}'", 'NEWLINE', "''", context=_context) not in ['INT', 'REAL', "'\\\\{'", "'nil'", 'STRING', 'ID', "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', '"\\\\["', "'-'"]: break
        self._scan('"\\\\)"', context=_context)
        return type_name+"("+additive_exp+")";

    def term(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'term', [])
        factor = self.factor(_context)
        S = factor
        while self._peek("r'[*]'", '"/"', '"%"', "r'[+]'", '"-"', '"\\\\]"', '"\\\\)"', '","', "'to'", "'by '", "'\\\\|'", 'INT', 'REAL', "'\\\\{'", "'nil'", 'STRING', 'ID', "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', '"\\\\["', "'-'", "'=='", "'!='", "'<'", "'>'", "'<='", "'>='", "'and'", "'or'", "'xor'", "'\\\\}'", 'NEWLINE', "''", context=_context) in ["r'[*]'", '"/"', '"%"']:
            _token = self._peek("r'[*]'", '"/"', '"%"', context=_context)
            if _token == "r'[*]'":
                self._scan("r'[*]'", context=_context)
                factor = self.factor(_context)
                S += "*" + factor
            elif _token == '"/"':
                self._scan('"/"', context=_context)
                factor = self.factor(_context)
                S += "/" + factor
            else: # == '"%"'
                self._scan('"%"', context=_context)
                factor = self.factor(_context)
                S += "%" + factor
        return S

    def factor(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'factor', [])
        _token = self._peek('INT', 'REAL', "'\\\\{'", "'nil'", 'STRING', 'ID', "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', '"\\\\["', "'-'", context=_context)
        if _token == 'INT':
            INT = self._scan('INT', context=_context)
            return INT
        elif _token == 'REAL':
            REAL = self._scan('REAL', context=_context)
            return REAL
        elif _token == "'\\\\{'":
            list_literal = self.list_literal(_context)
            return list_literal
        elif _token == "'nil'":
            self._scan("'nil'", context=_context)
            return 'None'
        elif _token == 'STRING':
            STRING = self._scan('STRING', context=_context)
            return STRING
        elif _token == 'ID':
            identifier = self.identifier(_context)
            A = identifier
            _token = self._peek('"\\\\("', '"\\\\["', "''", context=_context)
            if _token == '"\\\\("':
                self._scan('"\\\\("', context=_context)
                list_plain = self.list_plain(_context)
                self._scan('"\\\\)"', context=_context)
                global listCount
                return A + "_args_" + str(listCount) + "("+list_plain+")"
            elif _token == '"\\\\["':
                self._scan('"\\\\["', context=_context)
                additive_exp = self.additive_exp(_context)
                self._scan('"\\\\]"', context=_context)
                return A + "["+additive_exp+"]"
            else: # == "''"
                self._scan("''", context=_context)
                return A
        elif _token not in ['"\\\\["', "'-'"]:
            cast_exp = self.cast_exp(_context)
            return cast_exp
        elif _token == '"\\\\["':
            self._scan('"\\\\["', context=_context)
            additive_exp = self.additive_exp(_context)
            self._scan('"\\\\]"', context=_context)
            return '(' + additive_exp + ')'
        else: # == "'-'"
            self._scan("'-'", context=_context)
            self._scan('"\\\\("', context=_context)
            additive_exp = self.additive_exp(_context)
            self._scan('"\\\\)"', context=_context)
            return '-('+additive_exp+')'

    def fcn_definition(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'fcn_definition', [])
        self._scan('"fcn"', context=_context)
        type_name = self.type_name(_context)
        fcn_name = self.fcn_name(_context)
        self._scan('"\\\\("', context=_context)
        param_list = self.param_list(_context)
        self._scan('"\\\\)"', context=_context)
        P1, P2, P3 = "", "", ""
        for x in param_list: P1+=x[0] + ","; P2 += x[1] + ",";
        S = "\ndef " + fcn_name + "_args_" + str(P2.count(",")) + "("+P2+"):"
        S += "\n\tcheck_args(["+P1+"], ["+P2+"], \""+fcn_name+"\")"
        compound_statement = self.compound_statement(_context)
        S += compound_statement
        global header
        header += S
        return ""

    def param_list(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'param_list', [])
        _token = self._peek("'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', "''", context=_context)
        if _token != "''":
            type_name = self.type_name(_context)
            identifier = self.identifier(_context)
            S = [(type_name, identifier)]
            while self._peek('","', '"\\\\)"', context=_context) == '","':
                self._scan('","', context=_context)
                type_name = self.type_name(_context)
                identifier = self.identifier(_context)
                S.append((type_name, identifier))
            return S
        else: # == "''"
            self._scan("''", context=_context)
            return []

    def compound_statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'compound_statement', [])
        NEWLINE = self._scan('NEWLINE', context=_context)
        S = "\n"
        global indents
        indents += 1
        while 1:
            statement = self.statement(_context)
            NEWLINE = self._scan('NEWLINE', context=_context)
            S += "\t"*indents + statement
            if self._peek("r'[~](.)*'", "'conclude'", "'next'", "'stop'", "'if'", "'for'", "'while'", "'loop'", "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', 'ID', "'end'", context=_context) not in ["r'[~](.)*'", "'conclude'", "'next'", "'stop'", "'if'", "'for'", "'while'", "'loop'", "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', 'ID']: break
        self._scan("'end'", context=_context)
        indents -= 1
        return S

    def p_compound_statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'p_compound_statement', [])
        NEWLINE = self._scan('NEWLINE', context=_context)
        S = "\n"
        global indents
        indents += 1
        while 1:
            statement = self.statement(_context)
            NEWLINE = self._scan('NEWLINE', context=_context)
            S += "\t"*indents + statement
            if self._peek("r'[~](.)*'", "'conclude'", "'next'", "'stop'", "'if'", "'for'", "'while'", "'loop'", "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', 'ID', "'end'", "'elseif'", "'else'", context=_context) not in ["r'[~](.)*'", "'conclude'", "'next'", "'stop'", "'if'", "'for'", "'while'", "'loop'", "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', 'ID']: break
        indents -= 1
        return S

    def jump_statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'jump_statement', [])
        _token = self._peek("'conclude'", "'next'", "'stop'", context=_context)
        if _token == "'conclude'":
            self._scan("'conclude'", context=_context)
            S = "return "
            _token = self._peek("''", "'yes'", "'no'", "'1'", "'0'", 'INT', 'REAL', "'\\\\{'", "'nil'", 'STRING', 'ID', "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', '"\\\\["', "'-'", context=_context)
            if _token not in ["''", "'yes'", "'no'", "'1'", "'0'"]:
                additive_exp = self.additive_exp(_context)
                S += additive_exp
            elif _token != "''":
                boolean_literal = self.boolean_literal(_context)
                S += boolean_literal
            else: # == "''"
                self._scan("''", context=_context)
                S += ""
            return S
        elif _token == "'next'":
            self._scan("'next'", context=_context)
            return "continue"
        else: # == "'stop'"
            self._scan("'stop'", context=_context)
            return "break"

    def fcn_name(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'fcn_name', [])
        identifier = self.identifier(_context)
        return identifier

    def conditional_statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'conditional_statement', [])
        self._scan("'if'", context=_context)
        self._scan("'\\\\|'", context=_context)
        boolean_exp = self.boolean_exp(_context)
        self._scan("'\\\\|'", context=_context)
        S = "if "+boolean_exp+":"
        p_compound_statement = self.p_compound_statement(_context)
        S += p_compound_statement
        while self._peek("'end'", "'else'", "'elseif'", context=_context) == "'elseif'":
            elseif_statement = self.elseif_statement(_context)
            S += elseif_statement
        _token = self._peek("'end'", "'else'", context=_context)
        if _token == "'else'":
            else_statement = self.else_statement(_context)
            S += else_statement
        else: # == "'end'"
            self._scan("'end'", context=_context)
            S += "\n"
        return S

    def elseif_statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'elseif_statement', [])
        global indents
        self._scan("'elseif'", context=_context)
        self._scan("'\\\\|'", context=_context)
        boolean_exp = self.boolean_exp(_context)
        self._scan("'\\\\|'", context=_context)
        S = "\t"*indents + "elif " + boolean_exp + ":"
        p_compound_statement = self.p_compound_statement(_context)
        S += p_compound_statement
        return S

    def else_statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'else_statement', [])
        global indents
        self._scan("'else'", context=_context)
        S = "\t"*indents + "else:"
        compound_statement = self.compound_statement(_context)
        S += compound_statement
        return S

    def boolean_exp(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'boolean_exp', [])
        _token = self._peek("'yes'", "'no'", "'1'", "'0'", "'not'", 'INT', 'REAL', "'\\\\{'", "'nil'", 'STRING', 'ID', "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', '"\\\\["', "'-'", context=_context)
        if _token not in ["'yes'", "'no'", "'1'", "'0'"]:
            logical_exp = self.logical_exp(_context)
            return logical_exp
        else: # in ["'yes'", "'no'", "'1'", "'0'"]
            boolean_literal = self.boolean_literal(_context)
            return boolean_literal

    def boolean_literal(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'boolean_literal', [])
        _token = self._peek("'yes'", "'no'", "'1'", "'0'", context=_context)
        if _token == "'yes'":
            self._scan("'yes'", context=_context)
            return 'True'
        elif _token == "'no'":
            self._scan("'no'", context=_context)
            return 'False'
        elif _token == "'1'":
            self._scan("'1'", context=_context)
            return 'True'
        else: # == "'0'"
            self._scan("'0'", context=_context)
            return 'False'

    def logical_exp(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'logical_exp', [])
        relational_exp = self.relational_exp(_context)
        S = relational_exp
        while self._peek("'and'", "'or'", "'xor'", "'\\\\|'", context=_context) != "'\\\\|'":
            _token = self._peek("'and'", "'or'", "'xor'", context=_context)
            if _token == "'and'":
                self._scan("'and'", context=_context)
                relational_exp = self.relational_exp(_context)
                S = 'logical_and('+S+','+relational_exp+')'
            elif _token == "'or'":
                self._scan("'or'", context=_context)
                relational_exp = self.relational_exp(_context)
                S = 'logical_or('+S+','+relational_exp+')'
            else: # == "'xor'"
                self._scan("'xor'", context=_context)
                relational_exp = self.relational_exp(_context)
                S = 'logical_xor('+S+','+relational_exp+')'
        return S

    def relational_exp(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'relational_exp', [])
        _token = self._peek("'not'", 'INT', 'REAL', "'\\\\{'", "'nil'", 'STRING', 'ID', "'void'", "'bool'", "'int'", "'real'", "'str'", "'array'", "'structure'", "'enum'", 'TYPE', '"\\\\["', "'-'", context=_context)
        if _token != "'not'":
            additive_exp = self.additive_exp(_context)
            S = additive_exp
            relational_op = self.relational_op(_context)
            S += relational_op
            additive_exp = self.additive_exp(_context)
            return S + additive_exp
        else: # == "'not'"
            self._scan("'not'", context=_context)
            relational_exp = self.relational_exp(_context)
            return 'not ' + relational_exp

    def relational_op(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'relational_op', [])
        _token = self._peek("'=='", "'!='", "'<'", "'>'", "'<='", "'>='", context=_context)
        if _token == "'=='":
            self._scan("'=='", context=_context)
            return '=='
        elif _token == "'!='":
            self._scan("'!='", context=_context)
            return '!='
        elif _token == "'<'":
            self._scan("'<'", context=_context)
            return '<'
        elif _token == "'>'":
            self._scan("'>'", context=_context)
            return '>'
        elif _token == "'<='":
            self._scan("'<='", context=_context)
            return '<='
        else: # == "'>='"
            self._scan("'>='", context=_context)
            return '>='

    def iterative_statement(self, _parent=None):
        _context = self.Context(_parent, self._scanner, 'iterative_statement', [])
        _token = self._peek("'for'", "'while'", "'loop'", context=_context)
        if _token == "'for'":
            self._scan("'for'", context=_context)
            self._scan("'\\\\|'", context=_context)
            S = "for "
            _token = self._peek("'int'", "'real'", "''", context=_context)
            if _token == "'int'":
                self._scan("'int'", context=_context)
            elif _token == "'real'":
                self._scan("'real'", context=_context)
            else: # == "''"
                self._scan("''", context=_context)
            identifier = self.identifier(_context)
            S += identifier
            self._scan("':='", context=_context)
            S += " in loop_range("
            additive_exp = self.additive_exp(_context)
            S += additive_exp
            self._scan("'to'", context=_context)
            additive_exp = self.additive_exp(_context)
            S += "," + additive_exp
            _token = self._peek("'by '", "'\\\\|'", context=_context)
            if _token == "'by '":
                self._scan("'by '", context=_context)
                additive_exp = self.additive_exp(_context)
                S += "," + additive_exp
                self._scan("'\\\\|'", context=_context)
                S += "):"
            else: # == "'\\\\|'"
                self._scan("'\\\\|'", context=_context)
                S += "):"
            compound_statement = self.compound_statement(_context)
            S += compound_statement
            return S
        elif _token == "'while'":
            self._scan("'while'", context=_context)
            self._scan("'\\\\|'", context=_context)
            S = "while("
            boolean_exp = self.boolean_exp(_context)
            S += boolean_exp
            self._scan("'\\\\|'", context=_context)
            S += "):"
            compound_statement = self.compound_statement(_context)
            S += compound_statement
            return S
        else: # == "'loop'"
            self._scan("'loop'", context=_context)
            S = ""
            compound_statement = self.compound_statement(_context)
            stat = compound_statement + "\t"
            self._scan("'\\\\|'", context=_context)
            boolean_exp = self.boolean_exp(_context)
            stat += "if not (" + boolean_exp + "): break;\n"
            self._scan("'\\\\|'", context=_context)
            S = "while(1):" + stat
            return S


def parse(rule, text):
    P = Prodo(ProdoScanner(text))
    return runtime.wrap_error_reporter(P, rule)

# End -- grammar generated by Yapps


