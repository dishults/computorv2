#!/usr/bin/env python3

import sys

import function as f

from Number import Rational, Complex, save_number

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
        if rest.count("i") > 1 or any(char in "/%^*" for char in rest):
            return f.process_function(name, rest, simple=True)
        else:
            return Complex.process(name, rest)
    elif rest in Data.everything:
        return Data.process_data(name, rest)
    return f.process_function(name, rest, simple=True)

def check_name(name):
    for char in ".,*/%+-^()[;]=?0123456789":
        name = name.replace(char, "")
    if not name or name == "i":
        raise SyntaxError

def check_input(user_input, allowed_chars):
    for char in user_input:
        if not char.isalpha() and not char in allowed_chars:
            if "(" in user_input:
                if Data.is_number(char) or char in ",*/%+-^()[;]":
                    continue
            raise SyntaxError

def process_input(user_input):
    user_input = user_input.lower()
    user_input = user_input.replace(" ", "")
    check_input(user_input, (".,*/%+-^()[;]=?0123456789"))
    if "=" in user_input and not user_input.endswith("?"):
        name, rest = user_input.split("=")
        check_input(name, "")
        check_name(name)
        if "(" in name:
            return f.save_function(name, rest)
        return process_type(name, rest)
    elif "(" not in user_input:
        return process_type(0, user_input)
    return f.calculate_function(user_input)

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