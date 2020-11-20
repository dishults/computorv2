from Data import Data
from Number import Complex
from Simple import Simple
from Polynomial import Polynomial

def check_if_variable_is_expression(var):
    copy = var.strip("-")
    for sign in ("/", "%", "*", "^", "+", "-"):
        if sign in copy:
            return str(calculate_function(var))
    return var

def process_expressions_in_variables(expression):
    copy = expression[:]
    while copy:
        try:
            func, var, copy = Simple.get_function_and_variable(copy)
        except:
            break
        new_var = check_if_variable_is_expression(var)
        if Data.is_number(new_var):
            new_func = Data.everything[func]
            res = new_func.calculate_with_variable(new_var, new_func.expression[:])
            res = str(res).replace(" ", "")
            expression = expression.replace(f"{func}({var})", res)
    return expression

def calculate_function(expression, rest=None):
    if "(" in expression:
        expression = process_expressions_in_variables(expression)
    try:
        assert not rest
        return Simple.process(0, expression)
    except:
        if rest and "(" in rest:
            rest = process_expressions_in_variables(rest)
        return Polynomial.calculate(expression, rest)

def save_function(name, rest, var=0):
    if "(" in name:
        name, var = Simple.get_function_and_variable(name)[:2]
        if "^" in rest and not "(" in rest:
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