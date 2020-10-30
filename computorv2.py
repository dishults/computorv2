#!/usr/bin/env python3

import sys
import re

from Numbers import Rational, Complex
from Matrices import Matrices

everything = {}

def get_type(user_input):
    without_spaces = user_input.replace(" ", "")
    var, rest = without_spaces.split("=")
    try:
        Rational.save_number(var, rest, everything)
    except:
        if "i" in rest:
            Complex.save_number(var, rest, everything)
        elif "[" in rest:
            Matrices.save_matrix(var, rest, everything)
        else:
            print("not a number")

def main():
    while True:
        user_input = input("> ")
        user_input = user_input.lower()
        if user_input == "exit" or user_input == "quit":
            break
        elif "=" in user_input:
            get_type(user_input)
        elif user_input:
            print(everything[user_input])

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