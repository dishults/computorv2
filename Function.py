from Simple import Simple
from Polynomial import Polynomial

def function(name, var, equation):
    if "^" in equation:
        Polynomial.save_data([name, var], equation)
    else:
        Simple.save_data([name, var], equation)

def save_function(name, rest, simple=False):
    if simple:
        function(name, 0, rest)
    else:
        name, var = name.split("(")
        var = var.strip("()")
        if var == "i":
            raise SyntaxError
        function(name, var, rest)
