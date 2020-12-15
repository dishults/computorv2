from Data import Data
from Number import Number, Rational, Complex
from Matrix import Matrix
from Simple import Simple
from Polynomial import Polynomial

def check_if_variable_is_expression(var):
    copy = var.strip("-")
    for sign in ("/", "%", "*", "^", "+", "-"):
        if sign in copy:
            return calculate_function(var)
    if Matrix.is_matrix(var):
        return Matrix(var)
    return var

def process_expressions_in_variables(expression):
    copy = expression[:]
    while copy:
        try:
            func, var, copy = Simple.get_function_and_variable(copy)
        except:
            break
        new_var = check_if_variable_is_expression(var)
        if func and (isinstance(new_var, (Number, Matrix)) or Data.is_number(new_var)):
            res = Simple.calculate_function_with_variable(func, new_var)
            if isinstance(res, Matrix):
                res = res.alt_str().replace(" ", "")
            else:
                res = str(res).replace(" ", "")
            expression = expression.replace(f"{func}({var})", res)
    return expression

def calculate_function(expression, rest=None):
    if "(" in expression:
        expression = process_expressions_in_variables(expression)
    try:
        assert not rest
        return Simple.process(0, expression)
    except (AssertionError, ValueError) as ex:
        if rest and "(" in rest:
            rest = process_expressions_in_variables(rest)
        try:
            return Polynomial.calculate(expression, rest)
        except ValueError:
            raise ValueError(ex)

def save_function(func, rest, var=0):
    assert rest
    if "(" in func:
        func, var = Simple.get_function_and_variable(func)[:2]
        if "^" in rest and var in rest and not "(" in rest:
            return Polynomial.process(func, rest, var)
    return Simple.process(func, rest, var)

def process_function(func, rest):
    if func:
        return save_function(func, rest)
    else:
        if "=" in rest:
            rest, func = rest.split("=")
            if func in Data.everything:
                func = Data.everything[func]
                func = str(func).replace(" ", "")
        return calculate_function(rest, func)