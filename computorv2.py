#!/usr/bin/env python3

import sys
import readline

import function as f

from Number import Rational, Complex

from Data import Data, ALLOWED
from Simple import Simple
from Matrix import Matrix

def process_type(name, rest):
    if Data.is_number(rest):
        return Rational.process(name, rest)
    elif "[" in rest:
        if not Matrix.is_expression(rest):        
            return Matrix.process(name, rest)
    elif "i" in rest:
        if not Complex.is_expression(rest):
            return Complex.process(name, rest)
    elif rest in Data.everything:
        return Data.process_data(name, rest)
    return f.process_function(name, rest)

def check_name(name):
    if "(" in name:
        func, var, expression = Simple.get_function_and_variable(name)
        if func == "i" or var == "i" or expression:
            raise SyntaxError("You can't use 'i' as a function/variable name")
        name = func + var
    for char in ".,[;]=0123456789" or ALLOWED:
        name = name.replace(char, "")
    if name == "i":
        raise SyntaxError("You can't use 'i' as a function/variable name")
    if not name:
        raise SyntaxError("Incorrect syntax")

def check_input(user_input, allowed_chars=".,()[;]=?0123456789"):
    if allowed_chars:
        allowed_chars = allowed_chars + "".join(ALLOWED)
    for char in user_input:
        if not char.isalpha() and not char in allowed_chars:
            if "(" in user_input:
                if Data.is_number(char) or char in ",()[;]" or ALLOWED:
                    continue
            raise SyntaxError(f"Forbidden character '{char}'")
    if allowed_chars:
        bad_combos = {"[]", "()", ",,", "[;]", "[;", ";]", "[,", ",]", "[[[", "]]]", \
            ";[[", "]];"}
        if any(bad_combo in user_input for bad_combo in bad_combos) \
                or user_input.count("(") != user_input.count(")") \
                or user_input.count("[") != user_input.count("]"):
            raise SyntaxError("Incorrect syntax")


def process_input(user_input):
    user_input = user_input.lower().replace(" ", "").replace("**", "@")
    check_input(user_input)
    if "=" in user_input and not user_input.endswith("?"):
        name, rest = user_input.split("=")
        check_input(name, "")
        check_name(name)
        return process_type(name, rest)
    user_input = user_input.strip("?")
    return process_type(0, user_input)

def plot(expression):
    import matplotlib.pyplot as plt    
    expression = expression.lower().replace(" ", "")
    func, var, rest = Simple.get_function_and_variable(expression)
    if not expression.startswith("plot") or func != "plot" or rest:
        raise SyntaxError("Usage: plot(function_name) and nothing else")
    obj = Data.everything[var]
    if not hasattr(obj, "expression"):
        raise TypeError("Can only plot a function")
    func = f"{var}({obj.variable}) = {obj}"
    curve = [Simple.calculate_function_with_variable(var, v).number for v in range(-49, 50)]
    plt.plot(range(-49, 50), curve)
    plt.suptitle(f"Function curve for:\n{func}")
    plt.ylabel("Results range")
    plt.xlabel(f"{obj.variable} range")
    plt.show()

def main():
    history = []
    while True:
        try:
            user_input = input("> ")
            if user_input == "exit" or user_input == "quit":
                raise KeyboardInterrupt
            elif user_input == "all":
                print(Data.show_everything())
            elif user_input == "history":
                [print(entry) for entry in history]
            elif "reset" in user_input:
                if "variables" in user_input:
                    Data.everything = {}
                elif "history" in user_input:
                    history = []
                else:
                    print("choose between [variables] or [history]")
            elif "plot(" in user_input:
                plot(user_input)
                history.append(f"\n  {user_input}")
            else:
                res = f"  {process_input(user_input)}"
                history.append(f"\n  {user_input}\n{res}")
                print(res)
        except Exception as ex:
            error_msg = f"Wrong input!\n{ex}"
            history.append(f"\n  {user_input}\n{error_msg}")
            print(error_msg)

def test_main():
    if "plot(" in sys.argv[1]:
        plot(sys.argv[1])
    else:
        print(" ", process_input(sys.argv[1]))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        test_main()
    else:
        try:
            main()
        except (KeyboardInterrupt, EOFError):
            print("Byeeeee")