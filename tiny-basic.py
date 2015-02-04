#!/usr/bin/env python

import argparse
import compiler
import interpreter
import io
import os

argParser = argparse.ArgumentParser()

argParser.add_argument("input",     nargs="?")
argParser.add_argument("--compile", action="store_true")
argParser.add_argument("--repl",    action="store_true")

args        = argParser.parse_args()
interpreter = interpreter.Interpreter()
compiler    = compiler.Compiler()

if args.repl:
    interpreter.repl()
elif not args.input:
    print "Error: No input file"
    exit(1)
elif not os.path.isfile(args.input):
    print "Error: Input file not found"
    exit(1)
else:
    with io.open(args.input, "r") as f:
        program = f.read().encode("ascii", "ignore")
    if args.compile:
        compiler.compile(program)
    else:
        interpreter.interpret(program)

