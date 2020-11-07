#!/usr/bin/env python3

import sys

import function

from Data import Data
from Number import Rational, Complex
from Matrix import Matrix

def get_type(name, rest):
    if "(" in name:
        function.save(name, rest)
    elif "[" in rest:
        Matrix.save_data(name, rest)
    elif "i" in rest:
        Complex.save_data(name, rest)
    elif rest in Data.everything:
        Data.reassign(name, rest)
    else:
        try:
            Rational.save_data(name, rest)
        except:
            function.save(name, rest)

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
        try:
            process_input(user_input)
        except:
            print("Wrong input")


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