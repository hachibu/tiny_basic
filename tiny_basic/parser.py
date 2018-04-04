import re
import peglet

class Parser(object):
    grammar = r"""
    lines       = _ line _ lines
                | _ line
    line        = num _ stmt                        hug
                | stmt                              hug
    stmt        = print_stmt
                | let_stmt
                | input_stmt
                | if_stmt
                | goto_stmt
                | clear_stmt
                | list_stmt
                | run_stmt
                | end_stmt
                | rem_stmt

    print_stmt  = (PRINT\b) _ expr_list
    let_stmt    = (LET\b) _ var _ (?:=) _ expr
                | (LET\b) _ var _ (?:=) _ str
    input_stmt  = (INPUT\b) _ var_list
    if_stmt     = (IF\b) _ expr _ (THEN\b) _ stmt
    goto_stmt   = (GOTO\b) _ expr
    clear_stmt  = (CLEAR\b)
    list_stmt   = (LIST\b)
    run_stmt    = (RUN\b)
    end_stmt    = (END\b)
    rem_stmt    = (REM\b) _ str

    expr_list   = expr _ , _ expr_list 
                | expr 
                | str _ , _ expr_list
                | str
    expr        = term _ binop _ expr               join
                | term _ relop _ expr               join
                | term
    term        = var
                | num
                | l_paren _ expr _ r_paren          join
    var_list    = var _ , _ var_list
                | var
    var         = ([A-Z])

    str         = " chars " _                       join quote
                | ' sqchars ' _                     join
    chars       = char chars 
                |
    char        = ([^\x00-\x1f"\\]) 
                | esc_char
    sqchars     = sqchar sqchars 
                |
    sqchar      = ([^\x00-\x1f'\\]) 
                | esc_char
    esc_char    = \\(['"/\\])
                | \\([bfnrt])                       escape
    num         = (\-) num
                | (\d+)
    relop       = (<>|><|<=|<|>=|>|=)               repop
    binop       = (\+|\-|\*|\/)
    l_paren     = (\()
    r_paren     = (\)) 
    _           = \s*
    """

    def __init__(self):
        kwargs = {"hug"     : peglet.hug,
                  "join"    : peglet.join,
                  "repop"   : self.repop,
                  "quote"   : self.quote,
                  "escape"  : re.escape}
        self.parser = peglet.Parser(self.grammar, **kwargs)
    
    def __call__(self, program):
        return self.parser(program)

    def repop(self, token):
        if token == "<>" or token == "><":
            return "!="
        return token

    def quote(self, token):
        return '"%s"' % token
