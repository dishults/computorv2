#!/usr/bin/env python3

import sys
import re

from Data import Data
from Numbers import Rational, Complex
from Matrices import Matrices
from Function import Function

def get_type(user_input):
    user_input = user_input.lower()
    without_spaces = user_input.replace(" ", "")
    name, rest = without_spaces.split("=")
    try:
        Rational.save_data(name, rest)
    except:
        if "(" in name:
            Function.save_data(name, rest)
        elif "[" in rest:
            Matrices.save_data(name, rest)
        elif "i" in rest:
            Complex.save_data(name, rest)
        else:
            print("not a number")

def main():
    while True:
        user_input = input("> ")
        if user_input == "exit" or user_input == "quit":
            break
        elif "=" in user_input:
            get_type(user_input)
        elif user_input:
            Data.show(user_input)

def test_main():
    get_type(sys.argv[1])

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            test_main()
        else:
            main()
    except (KeyboardInterrupt, EOFError):
        print()