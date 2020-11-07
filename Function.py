from Simple import Simple
from Polynomial import Polynomial

def function(name, var, equation):
    if "^" in equation:
        Polynomial.save_data([name, var], equation)
    else:
        Simple.save_data([name, var], equation)

def save(name, rest):
    try:
        name, var = name.split("(")
        var = var.strip("()")
        function(name, var, rest)
    except:
        function(name, 0, rest)
