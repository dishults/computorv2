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
            save_function(name, rest)

def process_input(user_input):
    user_input = user_input.lower()
    user_input = user_input.replace(" ", "")
    if "=" in user_input:
        name, rest = user_input.split("=")
        get_type(name, rest)
    elif "(" in user_input:
        func, var = user_input.split("(")
        var = var.strip("()")
        Data.everything[func].fix(var)
        Data.everything[func].calculate(var)
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