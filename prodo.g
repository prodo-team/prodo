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
    token TYPE: r'[a-zA-Z]'                         # typenames (letters & underscore only)
    ignore: r' '                                    # ignore rogue spaces
    ignore: r'[~](.)*'                              # ignore comments

    rule super:                              {{ global header }}
                                             {{ global indents }}
                                             {{ global listCount }}
                                             {{ header = '' }}
                                             {{ indents = 0 }}
                                             {{ listCount = 0 }}
                                             {{ code = '' }}
                ( statement_upper ender      {{ code += statement_upper }}
                )*
                END                    {{ return header + code }}

    rule ender: NEWLINE | ''

    rule type_name: 'void'                  {{ return 'type(None)' }}
                  | 'bool'                  {{ return 'bool' }}
                  | 'int'                   {{ return 'int' }}
                  | 'real'                  {{ return 'float' }}
                  | 'str'                   {{ return 'str' }}
                  | 'array'                 {{ return 'list' }}
                 # | TYPE                    {{ return TYPE }}

    rule statement_upper: exp_statement         {{ return exp_statement }}
                       | fcn_definition         {{ return fcn_definition }}
                       | conditional_statement  {{ return conditional_statement }}
                       | iterative_statement    {{ return iterative_statement }}
                       | structure_declaration  {{ return structure_declaration }}
                       | r'[~](.)*'             {{ return "\n" }}

    rule statement : exp_statement          {{ return exp_statement }}
                   | jump_statement         {{ return jump_statement }}
                   | conditional_statement  {{ return conditional_statement }}
                   | iterative_statement    {{ return iterative_statement }}
                   | structure_declaration  {{ return structure_declaration }}
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
                          ("\\(" list_plain "\\)")      {{ global listCount }}
                          {{ return identifier + "_args_" + str(listCount) + "("+list_plain+")\n" }}
                          | r"[+][+]"                   {{ return identifier + "+=1\n" }}
                          | "--"                        {{ return identifier + "--\n" }}
                          )

    rule declaration_exp : type_name                  {{ A = "" }}
                            list_identifiers ':='     {{ A += list_identifiers }}
                            additive_exp
                                                      {{ A += "=" + type_name + "("+additive_exp+")" }}
                                                      {{ return A + "\n" }}

    rule structure_declaration : 'structure' list_identifiers   {{ A = list_identifiers }}
                                                                {{ A += " = dict(" }}
                                 struct_compound_stat           {{ A += struct_compound_stat.replace("\n",",") + ")\n" }}
                                                                {{ return A }}

    rule identifier : ID                            {{ S = ID.replace("$", "_dol_") }}
                                                    {{ S = S.replace("@", "_at_") }}
                      ( "\\." ID              {{ S += "['"+ID.replace("$", "_dol_").replace("@","_at_")+"']" }}
                      | "\\[" additive_exp "\\]"      {{ S += "["+additive_exp+"]" }}
                      | ''
                      )                             {{ return S }}

    rule assignment_op : ":="                       {{ return "" }}
                       | r"[*]="                    {{ return "*" }}
                       | "/="                       {{ return "/" }}
                       | "%="                       {{ return "%" }}
                       | r"[+]="                    {{ return "+" }}
                       | "-="                       {{ return "-" }}

    rule list_literal : '\\{' list_plain '\\}'      {{ return '['+list_plain+']' }}

    rule list_plain :                       {{ global listCount }}
                                            {{ listCount = 0 }}
                                            {{ my_listCount = 0 }}
                      (additive_exp         {{ S = additive_exp; my_listCount += 1 }}
                      ( "," additive_exp    {{ S += "," + additive_exp; my_listCount += 1 }}
                      )*
                                            {{ listCount = my_listCount }}
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
                       | boolean_literal  {{ return boolean_literal }}
                       | 'nil'            {{ return 'None' }}
                       | STRING           {{ return STRING }}
                       | ( identifier     {{ A = identifier }}
                           ( "\\(" list_plain "\\)"     {{ global listCount }}
                           {{ return A + "_args_" + str(listCount) + "("+list_plain+")" }}
                           | ''                         {{ return A }}
                           )
                         )
                       | cast_exp         {{ return cast_exp }}
                       | "\\[" additive_exp "\\]" {{ return '(' + additive_exp + ')' }}
                       | '-'additive_exp          {{ return '-('+additive_exp+')' }}

    rule fcn_definition : "fcn" type_name fcn_name "\\(" param_list "\\)"
                                             {{ P1, P2, P3 = "", "", "" }}
                                             {{ for x in param_list: P1+=x[0] + ","; P2 += x[1] + ","; }}
                                             {{ S = "\ndef " + fcn_name + "_args_" + str(P2.count(",")) + "("+P2+"):" }}
                                            # note that function definitions can't be nested, so a toplevel indentation of 1 tab is always guaranteed inside functions
                                             {{ S += "\n\tcheck_args(["+P1+"], ["+P2+"], \""+fcn_name+"\")" }} # check argument types
                                             {{ S += "\n\tconclude = " + type_name }} # return type
                                             {{ S += "\n\t_fcn = \"" + fcn_name + "\"" }} # function name
                          compound_statement {{ S += compound_statement }}
                                             {{ global header }}
                                             {{ header += S }}
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

    rule struct_compound_stat : NEWLINE            {{ S = "" }}
                          (declaration_exp NEWLINE {{ S += declaration_exp }}
                          )+
                          'end'                    {{ return S }}


    rule jump_statement : 'conclude'           {{ S = "return check_return_value(conclude, _fcn, " }}
                          ( additive_exp       {{ S += additive_exp }}
                          | ''                 {{ S += "None" }}
                          )
                                               {{ return S + ")\n" }}
                        | 'next'               {{ return "continue\n" }}
                        | 'stop'               {{ return "break\n" }}


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

    rule boolean_literal : 'yes'                            {{ return 'True' }}
                         | 'no'                             {{ return 'False' }}

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
                              ('int'                        {{ t = 'int(' }}
                              |'real'                       {{ t = 'float(' }}
                              |''                           {{ t = 'assign(' }}
                              )
                              identifier                    {{ S += identifier }}
                                                            {{ if t == 'assign(': t += identifier + ',' }}
                              ':='                          {{ S += " in loop_range(" }}
                              additive_exp                  {{ S += t + additive_exp + ")" }}
                              'to' additive_exp             {{ S += "," + t + additive_exp + ")" }}
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
