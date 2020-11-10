#!/usr/bin/env python3

import sys

from function import save_function
from Number import save_number

from Data import Data
from Matrix import Matrix

def get_type(name, rest):
    if "(" in name:
        save_function(name, rest)
    elif "[" in rest:
        Matrix.save_data(name, rest)
    elif "i" in rest:
        save_number(name, rest)
    elif rest in Data.everything:
        Data.reassign(name, rest)
    else:
        try:
            save_number(name, rest)
        except:
            save_function(name, rest, simple=True)

def check_input(user_input, allowed_chars):
    for char in user_input:
        if not char.isalnum() and not char in allowed_chars:
            raise SyntaxError

def process_input(user_input):
    user_input = user_input.lower()
    user_input = user_input.replace(" ", "")
    check_input(user_input, (".,*/%+-()[;]^=?"))
    if "=" in user_input and not user_input.endswith("?"):
        name, rest = user_input.split("=")
        check_input(name, (".,*/%+-()[;]"))
        get_type(name, rest)
    elif "(" in user_input:
        func, var = user_input.split("(")
        var, rest = var.split(")", 1)
        if (rest and not rest.endswith("?")):
            raise SyntaxError
        Data.everything[func].calculate(var)
        Data.show(func)
    elif user_input:
        Data.show(user_input)


def main():
    while True:
        user_input = input("> ")
        if user_input == "exit" or user_input == "quit":
            raise KeyboardInterrupt
        try:
            process_input(user_input)
        except:
            print("Wrong input")


def test_main():
    #process_input("funA(x) = 2 * x - 5")
    #process_input("varC = 3")
    #process_input("funA(varC)")
    process_input(sys.argv[1])
    
    #try: process_input(sys.argv[1])
    #except: pass

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            test_main()
        else:
            main()
    except (KeyboardInterrupt, EOFError):
        print()