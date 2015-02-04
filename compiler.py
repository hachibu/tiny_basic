import parser
import re

class Compiler(object):
    
    def __init__(self):
        self.parser          = parser.Parser()
        self.parse_tree      = None
        self.symbols        = {}
        self.malloc_symbols = {}

    def compile(self, program):
        self.parse_tree = self.parser(program)
        print "#include <stdio.h>"
        print "#include <stdlib.h>"
        print "#include <string.h>"
        print "int main (void) {"
        for line in self.parse_tree:
            if "LET" in line:
                id = line[2]
                if id not in self.symbols:
                    self.compile_stmt(line[1:])
            elif "INPUT" in line:
                id = line[2]
                if id not in self.symbols:
                    self.compile_var((id, '""'))
        for line in self.parse_tree:
            self.compile_stmt(line)
        print "}"
    
    def compile_stmt(self, stmt):
        head, tail = stmt[0], stmt[1:]
        if tail:
            if head == "IF":
                self.compile_if(tail)
            elif head == "LET":
                self.compile_var(tail)
            elif head == "REM":
                self.compile_comment(tail)
            elif head == "GOTO":
                self.compile_goto(tail)
            elif head == "PRINT":
                self.compile_printf(tail)
            elif head == "INPUT":
                self.compile_input(tail)
            else:
                self.compile_label(head)
                self.compile_stmt(tail)
        else:
            if head == "END":
                self.compile_return()
    
    def compile_input(self, xs):
        id, buffer = xs[0], 50
        self.malloc_symbols[id] = buffer
        print "{0} = malloc(sizeof(char) * {1}); \n\
fgets({0}, {1}, stdin); \n\
if ({0}[strlen({0}) - 1] == '\\n') {{ \n\
{0}[strlen({0}) - 1] = '\\0'; \n\
}}".format(id, buffer)

    def compile_if(self, xs):
        cond, stmt = xs[0], xs[2:]
        print "if (%s) {" % (cond)
        self.compile_stmt(stmt)
        print "}"

    def compile_goto(self, xs):
        print "goto label_%s;" % xs[0]

    def compile_var(self, xs):
        id = xs[0]
        if id in self.symbols:
            self.compile_var_set(xs)
        else:
            self.compile_var_dec(xs)
    
    def compile_var_dec(self, xs):
        t, id, v = None, xs[0], xs[1]
        if self.is_quoted(v):
            t = "char"
        else:
            t = "int"
        self.symbols[id] = (t, v)
        if t == "char":
            print "%s* %s;" % (t, id)
        elif t == "int":
            print "%s %s;" % (t, id)

    def compile_var_set(self, xs):
        id, nv = xs[0], xs[1]
        t, ov = self.symbols[id] 
        self.symbols[id] = (t, nv)
        print "%s = %s;" % (id, nv)

    def compile_comment(self, xs):
        print "// %s" % xs[0].replace('"', "")

    def compile_label(self, n):
        print "label_%s:" % n
    
    def compile_printf(self, xs):
        fmt, args = [], []
        for x in xs:
            if x in self.symbols:
                t, v = self.symbols[x]
                if t == "char":
                    fmt.append("%s")
                elif t == "int":
                    fmt.append("%d")
                args.append(x)
            else:
                try:
                    x = int(eval(x))
                    fmt.append("%d")
                    args.append(str(x))
                except:
                    fmt.append("%s")
                    args.append(x)
        if fmt and args:
            fmt = " ".join(fmt)
            args = ", ".join(args)
            print 'printf("{0}\\n", {1});'.format(fmt, args)

    def compile_return(self):
        for id in self.malloc_symbols:
            print "free(%s);" % id
        print "return 0;"

    def is_quoted(self, s):
        return re.match('^".*"$', s)

