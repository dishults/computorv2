from Simple import Simple
from Polynomial import Polynomial

def function(name, var, expression):
    if "^" in expression and not "(" in expression:
        return Polynomial.save_data([name, var], expression)
    else:
        return Simple.save_data([name, var], expression)

def save_function(name, rest, simple=False):
    if simple:
        return Simple.save_data([name, 0], rest)
    else:
        name, var = name.split("(")
        var = var.strip("()")
        if var == "i":
            raise SyntaxError
        return function(name, var, rest)

def calculate_function(expression):
    if "=" in expression:
        expression, rest = expression.split("=")
    expression = expression.strip("?")
    rest = rest.strip("?")
    try:
        obj = Simple(0, expression)
        return obj.expression[0]
    except:
        return Polynomial.calculate(expression, rest)


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