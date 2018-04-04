from .parser import Parser
import re

class Interpreter(object):
    def __init__(self):
        self.curr       = 0
        self.memory     = {}
        self.symbols    = {}
        self.parse_tree = None
        self.parser     = Parser()

    def interpret(self, program):
        self.parse_tree = self.parser(program)
        for line in self.parse_tree:
            if len(line) > 1:
                head, tail = line[0], line[1:]
                self.memory[head] = tail
        for line in self.parse_tree:
            if len(line) == 1:
                self.stmt(line)
        self.curr = 0

    def stmt(self, stmt):
        head, tail = stmt[0], stmt[1:]
        if head == "PRINT":
            self.print_stmt(tail)
        elif head == "LET":
            self.let_stmt(tail)
        elif head == "INPUT":
            self.input_stmt(tail)
        elif head == "IF":
            self.if_stmt(tail)
        elif head == "GOTO":
            self.goto_stmt(tail)
        elif head == "CLEAR":
            self.clear_stmt()
        elif head == "LIST":
            self.list_stmt()
        elif head == "RUN":
            self.run_stmt()
        elif head == "END":
            self.end_stmt()
    
    def print_stmt(self, xs):
        print(" ".join(self.expr_list(xs)))
    
    def let_stmt(self, xs):
        head, tail = xs[0], xs[1]
        self.symbols[head] = self.expr(tail)
    
    def input_stmt(self, xs):
        for x in xs:
            self.symbols[x] = str(input("? "))
    
    def if_stmt(self, xs):
        head, tail = xs[0], xs[2:]
        if self.expr(head) == "True":
            self.stmt(tail)
    
    def goto_stmt(self, xs):
        n = self.expr(xs[0])
        self.curr = n
        self.run_stmt()

    def run_stmt(self):
        stmts = self.gen_stmts()
        while(stmts):
            try:
                self.curr, line = next(stmts)
                self.stmt(line)
            except StopIteration:
                break

    def gen_stmts(self):
        for k in sorted(self.memory):
            c = int(self.curr)
            if c != -1 and int(k) >= c:
                yield (k, self.memory[k])

    def is_int_str(self, s):
        return re.search("^[0-9]+$", s) != None

    def end_stmt(self):
        self.curr = -1
    
    def list_stmt(self):
        for k in sorted(self.memory):
            print(" ".join(list(self.memory[k])))
    
    def clear_stmt(self):
        self.memory = {}
    
    def expr_list(self, xs):
        return [self.expr(x) for x in xs]

    def expr(self, x):
        if re.match("^\".*\"$", x):
            return x.replace("\"", "")
        else:
            vs = re.findall("[A-Z]", x)
            if vs:
                for v in vs:
                    x = x.replace(v, self.var(v))
            try:
                return str(eval(x))
            except:
                return x.replace("\"", "")

    def var(self, x):
        return self.symbols[x]

    def repl(self):
        try:
            line = str(input("tiny_basic> ")).upper()
            if line == "QUIT":
                exit(0)
            try: 
                self.interpret(line)
            except:
                if line:
                    print('PARSE ERROR "{}"'.format(line))
            self.repl()
        except:
            pass
