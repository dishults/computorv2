from Data import Data
from Number import Number, Rational, Complex
from Simple import Simple
from Polynomial import Polynomial

def check_if_variable_is_expression(var):
    copy = var.strip("-")
    for sign in ("/", "%", "*", "^", "+", "-"):
        if sign in copy:
            return calculate_function(var).expression[0]
    return var

def process_expressions_in_variables(expression):
    copy = expression[:]
    while copy:
        try:
            func, var, copy = Simple.get_function_and_variable(copy)
        except:
            break
        new_var = check_if_variable_is_expression(var)
        if func and (isinstance(new_var, Number) or Data.is_number(new_var)):
            res = Simple.calculate_function_with_variable(func, new_var)
            res = str(res).replace(" ", "")
            expression = expression.replace(f"{func}({var})", res)
    return expression

def calculate_function(expression, rest=None):
    if "(" in expression:
        expression = process_expressions_in_variables(expression)
    try:
        assert not rest
        return Simple.process(0, expression)
    except (AssertionError, ValueError):
        if rest and "(" in rest:
            rest = process_expressions_in_variables(rest)
        return Polynomial.calculate(expression, rest)

def save_function(name, rest, var=0):
    if "(" in name:
        name, var = Simple.get_function_and_variable(name)[:2]
        if "^" in rest and var in rest and not "(" in rest:
            return Polynomial.process(name, rest, var)
    return Simple.process(name, rest, var)


def process_function(name, rest):
    if name:
        return save_function(name, rest)
    else:
        if "=" in rest:
            rest, name = rest.split("=")
            if name in Data.everything:
                name = Data.everything[name]
                name = str(name).replace(" ", "")
        return calculate_function(rest, name)