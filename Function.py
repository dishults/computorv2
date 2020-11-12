from Simple import Simple
from Polynomial import Polynomial

def function(name, var, expression):
    if "^" in expression:
        Polynomial.save_data([name, var], expression)
    else:
        Simple.save_data([name, var], expression)

def save_function(name, rest, simple=False):
    if simple:
        function(name, 0, rest)
    else:
        name, var = name.split("(")
        var = var.strip("()")
        if var == "i":
            raise SyntaxError
        function(name, var, rest)

def calculate_function(expression):
    if "=" in expression:
        expression = expression.split("=")[0]
    if "?" in expression:
        expression = expression.strip("?")
    obj = Simple(0, expression)
    res = obj.calculate(obj.expression)
    return res

def check_if_variable_is_expression(var):
    for sign in ("/", "%", "*", "+"):
        if sign in var:
            return calculate_function(var)
    if "-" in var:
        if var[0] == "-":
            if "-" in var.strip("-"):
                return calculate_function(var)
        else:
            return calculate_function(var)
    return var