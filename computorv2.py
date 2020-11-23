#!/usr/bin/env python3

import sys

import function as f

from Number import Rational, Complex

from Data import Data
from Simple import Simple
from Matrix import Matrix

def process_type(name, rest):
    if Data.is_number(rest):
        return Rational.process(name, rest)
    elif "[" in rest:
        return Matrix.process(name, rest)
    elif "i" in rest:
        rest = rest.replace("*i", "i")
        if Complex.is_expression(rest):
            return f.process_function(name, rest)
        else:
            return Complex.process(name, rest)
    elif rest in Data.everything:
        return Data.process_data(name, rest)
    return f.process_function(name, rest)

def check_name(name):
    if "(" in name:
        func, var, expression = Simple.get_function_and_variable(name)
        if func == "i" or var == "i" or expression:
            raise SyntaxError
        name = func + var
    for char in ".,*/%+-^[;]=0123456789":
        name = name.replace(char, "")
    if not name or name == "i":
        raise SyntaxError

def check_input(user_input, allowed_chars=".,*/%+-^()[;]=?0123456789"):
    for char in user_input:
        if not char.isalpha() and not char in allowed_chars:
            if "(" in user_input:
                if Data.is_number(char) or char in ",*/%+-^()[;]":
                    continue
            raise SyntaxError

def process_input(user_input):
    user_input = user_input.lower().replace(" ", "")
    check_input(user_input)
    if "=" in user_input and not user_input.endswith("?"):
        name, rest = user_input.split("=")
        check_input(name, "")
        check_name(name)
        return process_type(name, rest)
    user_input = user_input.strip("?")
    return process_type(0, user_input)

def main():
    while True:
        user_input = input("> ")
        if user_input == "exit" or user_input == "quit":
            raise KeyboardInterrupt
        try:
            print(" ", process_input(user_input))
        except:
            print("Wrong input")

def try_run():
    try: print(" ", process_input(sys.argv[1]))
    except: pass

def test_main():
    print(" ", process_input(sys.argv[1]))
    #try_run()

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            test_main()
        else:
            main()
    except (KeyboardInterrupt, EOFError):
        print()