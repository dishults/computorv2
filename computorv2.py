#!/usr/bin/env python3

import sys

import function as f

from Number import save_number

from Data import Data
from Simple import Simple
from Matrix import Matrix

def get_type(name, rest):
    check_name(name)
    if "(" in name:
        return f.save_function(name, rest)
    elif "[" in rest:
        return Matrix.save_data(name, rest)
    elif "i" in rest:
        return save_number(name, rest)
    elif rest in Data.everything:
        return Data.reassign(name, rest)
    else:
        try:
            return save_number(name, rest)
        except:
            return f.save_function(name, rest, simple=True)

def check_name(name):
    for char in ".,*/%+-^()[;]=?0123456789":
        name = name.replace(char, "")
    if not name:
        raise SyntaxError

def check_input(user_input, allowed_chars):
    for char in user_input:
        if not char.isalnum() and not char in allowed_chars:
            raise SyntaxError

def process_input(user_input):
    user_input = user_input.lower()
    user_input = user_input.replace(" ", "")
    check_input(user_input, (".,*/%+-^()[;]=?"))
    if "=" in user_input and not user_input.endswith("?"):
        name, rest = user_input.split("=")
        check_input(name, (".,*/%+-^()[;]"))
        return get_type(name, rest)
    elif "(" not in user_input:
        try:
            return Data.show(user_input)
        except:
            pass
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
    print(" ", process_input("funA(x) = x^2 + 2x + 1"))
    print(" ", process_input("y = 0"))
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