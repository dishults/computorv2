#!/usr/bin/env python3

import sys
import re

from Data import Data
from Numbers import Rational, Complex
from Matrices import Matrices
from Function import Function

def get_type(name, rest):
    try:
        Rational.save_data(name, rest)
    except:
        if "(" in name:
            Function.save_data(name, rest)
        elif "[" in rest:
            Matrices.save_data(name, rest)
        elif "i" in rest:
            Complex.save_data(name, rest)
        elif rest in Data.everything:
            Data.reassign(name, rest)
        else:
            print("Wrong input")

def process_input(user_input):
    user_input = user_input.lower()
    user_input = user_input.replace(" ", "")
    if "=" in user_input:
        name, rest = user_input.split("=")
        get_type(name, rest)
    elif user_input:
        Data.show(user_input)


def main():
    while True:
        user_input = input("> ")
        if user_input == "exit" or user_input == "quit":
            raise KeyboardInterrupt
        process_input(user_input)

def test_main():
    process_input(sys.argv[1])

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            test_main()
        else:
            main()
    except (KeyboardInterrupt, EOFError):
        print()