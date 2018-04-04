#!/usr/bin/env python3

from tiny_basic import compiler, interpreter
import argparse
import io
import os

argParser = argparse.ArgumentParser()

argParser.add_argument("input",     nargs="?")
argParser.add_argument("--compile", action="store_true")

args        = argParser.parse_args()
interpreter = interpreter.Interpreter()
compiler    = compiler.Compiler()

if not args.input:
    interpreter.repl()
elif not os.path.isfile(args.input):
    print("Input file not found.")
    exit(1)
else:
    with io.open(args.input, "r") as f:
        program = f.read()
    if args.compile:
        compiler.compile(program)
    else:
        interpreter.interpret(program)
