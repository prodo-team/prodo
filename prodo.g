#!/usr/bin/python2
%%

# Outputs Python 3 code. Also runs in Python 2.7 after running 'pip install enum34'

parser Prodo:
    token END: r'$'                                 # end of input
    token NEWLINE: r'([\n])+'                       # new line
    token INT: r'([0-9])+|([-][0-9])+'              # int literal
    token REAL: r'[0-9]+[.][0-9]+|[-][0-9]+[.][0-9]+' # float literal
    token STRING: r'"([^\\"]+|\\.)*"'               # string literal
    token ID: r'[a-zA-Z]([a-zA-Z0-9$_@])*'          # name/identifier
    token TYPE: r'[a-zA-Z_]'                        # typenames (letters & underscore only)
    ignore: r' '                                    # ignore rogue spaces
    ignore: r'[~](.)*'                              # ignore comments

    rule super:                        {{ global header }}
                                       {{ header = '' }}
                                       {{ global indents }}
                                       {{ indents = 0 }}
                                       {{ code = '' }}
                ( statement ender      {{ code += statement }}
                )*
                END                    {{ return header + code }}

    rule ender: NEWLINE | ''

    rule type_name: 'void'                  {{ return 'void' }}
                  | 'bool'                  {{ return 'bool' }}
                  | 'int'                   {{ return 'int' }}
                  | 'real'                  {{ return 'float' }}
                  | 'str'                   {{ return 'str' }}
                  | 'array'                 {{ return 'list' }}
                  | 'structure'             {{ return 'dict' }}
                  | 'enum'                  {{ return 'enum ' }}
                  | TYPE                    {{ return TYPE }}

    rule statement : exp_statement          {{ return exp_statement }}
                   | fcn_definition         {{ return fcn_definition }}
                   | jump_statement         {{ return jump_statement }}
                   | conditional_statement  {{ return conditional_statement }}
                   | iterative_statement    {{ return iterative_statement }}
                   | r'[~](.)*'             {{ return "\n" }}

    rule exp_statement : declaration_exp              {{ return declaration_exp }} # don't add semicolon
                       | identified_exp               {{ return identified_exp }}

    rule identified_exp : identifier                  {{ A = "" }}
                          ( (assignment_op             {{ O = assignment_op }}
                                                      {{ S = [identifier] }}
                            additive_exp              {{ if (O != ""): additive_exp = identifier + assignment_op + additive_exp; }}
                                                      {{ for x in S: A += x + "=assign(" + x + "," + additive_exp + ")" }}
                                                      {{ return A + "\n" }}
                            )
                          |
                          ("\\(" list_plain "\\)")      {{ return identifier + "("+list_plain+")\n" }}
                          | r"[+][+]"                   {{ return identifier + "+=1\n" }}
                          | "--"                        {{ return identifier + "--\n" }}
                          )

    rule declaration_exp : type_name                  {{ A = "" }}
                            list_identifiers ':='     {{ A += list_identifiers }}
                            additive_exp
                                                      {{ A += "=" + type_name + "("+additive_exp+")" }}
                                                      {{ return A + "\n" }}

    rule identifier : ID                            {{ ID = ID.replace("$", "_dol_") }}
                                                    {{ ID = ID.replace("@", "_at_") }}
                                                    {{ return ID }}

    rule assignment_op : ":="                       {{ return "" }}
                       | r"[*]="                    {{ return "*" }}
                       | "/="                       {{ return "/" }}
                       | "%="                       {{ return "%" }}
                       | r"[+]="                    {{ return "+" }}
                       | "-="                       {{ return "-" }}

    rule list_literal : '\\{' list_plain '\\}'      {{ return '['+list_plain+']' }}

    rule list_plain : (additive_exp         {{ S = additive_exp }}
                      ( "," additive_exp    {{ S += "," + additive_exp }}
                      )*
                                            {{ return S }}
                      | ''                  {{ return '' }} # empty list
                      )

    rule list_identifiers : identifier      {{ S = identifier }}
                            ( ',' identifier  {{ S += "=" + identifier }}
                            )*
                                            {{ return S }}

    rule additive_exp: term                 {{ S = term }} # initial sum
                       ( r'[+]' term        {{ S += "+" + term }} # build up using partial sums
                       |  "-"  term         {{ S += "-" + term }}
                       )*                   {{ return S }}

    rule cast_exp: type_name "\\(" + additive_exp + "\\)"
                                            {{ return type_name+"("+additive_exp+")"; }}

    rule term:         factor               {{ S = factor }} # initial product
                       ( r'[*]' factor      {{ S += "*" + factor }} # build up using partial products
                       |  "/"  factor       {{ S += "/" + factor }}
                       |  "%"  factor       {{ S += "%" + factor }}
                       )*                   {{ return S }}

    # A term is either a number or an expression surrounded by parentheses
    rule factor :        INT              {{ return INT }}
                       | REAL             {{ return REAL }}
                       | list_literal     {{ return list_literal }}
                       | 'nil'            {{ return 'None' }}
                       | STRING           {{ return STRING }}
                       | ( identifier     {{ A = identifier }}
                           ( "\\(" list_plain "\\)"     {{ return A + "("+list_plain+")" }}
                           | "\\[" additive_exp "\\]"   {{ return A + "["+additive_exp+"]" }}
                           | ''                         {{ return A }}
                           )
                         )
                       | cast_exp         {{ return cast_exp }}
                       | "\\[" additive_exp "\\]" {{ return '(' + additive_exp + ')' }}
                       | '-'"\\("additive_exp"\\)" {{ return '-('+additive_exp+')' }}

    rule fcn_definition : "fcn" type_name fcn_name "\\(" param_list "\\)"
                                             {{ P1 = "" }}
                                             {{ for x in param_list: P1+=x[1] }}
                                             {{ S = "\ndef " + fcn_name + "(" + P1 + "):" }}
                          compound_statement {{ S += compound_statement }}
                                             {{ global header }}
                                             {{ header += S + "\n" }}
                                             {{ return "" }}


    rule param_list : type_name identifier          {{ S = [(type_name, identifier)] }}
                      ( "," type_name identifier    {{ S.append((type_name, identifier)) }}
                      )*
                                                    {{ return S }}
                    | ''                            {{ return [] }} # empty parameter list


    rule compound_statement : NEWLINE                  {{ S = "\n" }}
                                                       {{ global indents }}
                                                       {{ indents += 1 }}
                                                       #{{ print ("in :- ", indents, "C") }}
                              (statement NEWLINE       {{ S += "\t"*indents + statement }}
                              )+
                              'end'                    {{ indents -= 1 }}
                                                       #{{ print ("ou :- ", indents, "C") }}
                                                       {{ return S }}

    rule p_compound_statement : NEWLINE               {{ S = "\n" }}
                                                      {{ global indents }}
                                                      {{ indents += 1 }}
                                                      #{{ print ("in :- ", indents, "P") }}
                                (statement NEWLINE    {{ S += "\t"*indents + statement  }}
                                )+
                                                      {{ indents -= 1 }}
                                                      #{{ print ("ou :- ", indents, "P") }}
                                                      {{ return S }}


    rule jump_statement : 'conclude'           {{ S = "return " }}
                          ( additive_exp       {{ S += additive_exp }}
                          | boolean_literal    {{ S += boolean_literal }}
                          | ''                 {{ S += "" }}
                          )
                                               {{ return S }}
                        | 'next'               {{ return "continue" }}
                        | 'stop'               {{ return "break" }}


    rule fcn_name : identifier                       {{ return identifier }}

    rule conditional_statement: 'if''\\|'boolean_exp'\\|'     {{ S = "if "+boolean_exp+":" }}
                                p_compound_statement          {{ S += p_compound_statement }}
                                (elseif_statement      {{ S += elseif_statement }}
                                )*
                                (else_statement        {{ S += else_statement }}
                                | 'end'            {{ S += "\n" }}
                                )
                                                              {{ return S }}

    rule elseif_statement :                                 {{ global indents }}
                           'elseif''\\|'boolean_exp'\\|'    {{ S = "\t"*indents + "elif " + boolean_exp + ":" }}
                           p_compound_statement             {{ S += p_compound_statement }}
                                                            {{ return S }}

    rule else_statement :                                   {{ global indents }}
                          'else'                            {{ S = "\t"*indents + "else:" }}
                          compound_statement                {{ S += compound_statement }}
                                                            {{ return S }}

    rule boolean_exp: logical_exp                           {{ return logical_exp }}
                    | boolean_literal                       {{ return boolean_literal }}

    rule boolean_literal : 'yes'                            {{ return 'True' }}
                         | 'no'                             {{ return 'False' }}
                         | '1'                              {{ return 'True' }}
                         | '0'                              {{ return 'False' }}

    rule logical_exp : relational_exp                       {{ S = relational_exp }}
                       ( 'and' relational_exp               {{ S = 'logical_and('+S+','+relational_exp+')' }}
                       | 'or' relational_exp                {{ S = 'logical_or('+S+','+relational_exp+')' }}
                       | 'xor' relational_exp               {{ S = 'logical_xor('+S+','+relational_exp+')' }}
                       )*
                                                            {{ return S }}

    rule relational_exp: additive_exp                       {{ S = additive_exp }}
                         relational_op                      {{ S += relational_op }}
                         additive_exp                       {{ return S + additive_exp }}
                       | 'not' relational_exp               {{ return 'not ' + relational_exp }}

    rule relational_op: '=='                                {{ return '==' }}
                      | '!='                                {{ return '!=' }}
                      | '<'                                 {{ return '<' }}
                      | '>'                                 {{ return '>' }}
                      | '<='                                {{ return '<=' }}
                      | '>='                                {{ return '>=' }}

    rule iterative_statement: ('for''\\|'                   {{ S = "for " }}
                              ('int' | 'real' | '')
                              identifier                    {{ S += identifier }}
                              ':='                          {{ S += " in loop_range(" }}
                              additive_exp                  {{ S += additive_exp }}
                              'to' additive_exp             {{ S += "," + additive_exp }}
                              (('by ' additive_exp)         {{ S += "," + additive_exp }}
                                '\\|'                       {{ S += "):" }}
                              | '\\|'                       {{ S += "):" }}
                              )
                              compound_statement            {{ S += compound_statement }}
                              )                             {{ return S }}
                              |
                              ('while''\\|'                 {{ S = "while(" }}
                               boolean_exp                  {{ S += boolean_exp }}
                               '\\|'                        {{ S += "):" }}
                               compound_statement           {{ S += compound_statement }}
                                                            {{ return S }}
                              )
                              |
                              ('loop'                      {{ S = "" }}
                               compound_statement          {{ stat = compound_statement + "\t" }}
                               '\\|'
                               boolean_exp                 {{ stat += "if not (" + boolean_exp + "): break;\n" }}
                               '\\|'                       {{ S = "while(1):" + stat }}
                                                           {{ return S }}
                              )

%%
