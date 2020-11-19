from Data import Data
from Number import Complex
from Simple import Simple
from Polynomial import Polynomial

def function(func, var, expression):
    if "^" in expression and not "(" in expression:
        return Polynomial.save_data([func, var], expression)
    else:
        return Simple.save_data([func, var], expression)

def save_function(func, rest):
    func, var = Simple.get_function_and_variable(func)[:2]
    if var == "i":
        raise SyntaxError
    return function(func, var, rest)

def process_expressions_in_variables(expression):
    copy = expression[:]
    while copy:
        var, copy = Simple.get_function_and_variable(copy)[1:]
        new_var = check_if_variable_is_expression(var)
        if new_var != var:
            expression = expression.replace(f"({var})", f"({new_var})")
        else:
            break
    return expression

def calculate_function(expression, rest=None):
    expression = expression.strip("?")
    if "=" in expression:
        expression, rest = expression.split("=")
    if "(" in expression:
        expression = process_expressions_in_variables(expression)
    try:
        assert not rest
        obj = Simple(expression)
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

def process_function(name, rest, simple=False):
    if name:
        return Simple.process(name, rest)
    else:
        return calculate_function(rest)