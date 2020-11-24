import sys

import POLY.formula as formula

from Data import Data
from Simple import Simple
from POLY.Term import Term

class Polynomial(Data):
    
    def __init__(self, expression, variable, rest=None, inverse=False):
        self.check_expression(expression)
        self.all_terms = {}
        self.variable = variable
        expression = expression.replace("*", "").replace("^", "")
        self.get_terms(expression, variable, inverse)
        if rest:
            rest = rest.replace("*", "").replace("^", "")
            self.get_terms(rest, variable, inverse=True)
        self.get_degree()
        self.expression = str(self)
        self.solution = self.expression + " = 0\n  " + self.solve()

    def __str__(self):
        if hasattr(self, 'expression'):
            return self.expression
        p = ""
        terms_in_reverse__order = sorted(self.all_terms, reverse=True)
        term = self.all_terms[terms_in_reverse__order[0]]
        if term.coefficient < 0:
            p += "-"
        if term.exponent >= 0 and term.coefficient != 0:
            p += str(term)
        for t in terms_in_reverse__order[1:]:
            term = self.all_terms[t]
            if term.coefficient > 0:
                p += f" + {term}"
            elif term.coefficient < 0:
                p += f" - {term}"
        if p.startswith(" +"):
            return p.strip(" +")
        elif p.startswith(" -"):
            return "-" + p.strip(" - ")
        if not p:
            return "0"
        return p

    def get_terms(self, expression, variable, inverse=False):
        previous = "+"
        if expression[0] == "-":
            expression = f"0{expression}"
        for sign in expression:
            if sign in ("+", "-"):
                term, expression = expression.split(sign, 1)
                self.proceed(term, previous, variable, inverse)
                previous = sign
        self.proceed(expression, previous, variable, inverse)

    def proceed(self, term, sign, variable, inverse):
        try: # 5x^2
            coefficient, exponent = term.split(variable) 
            assert exponent
        except AssertionError: # 5x
            coefficient = term.strip(variable) 
            exponent = 1
        except ValueError: # 5
            coefficient = term
            exponent = 0
        term = Term(sign, coefficient, variable, exponent, inverse)
        if term.exponent in self.all_terms:
            self.all_terms[term.exponent].coefficient += term.coefficient
            if term.exponent > 2 and self.all_terms[term.exponent].coefficient == 0:
                del self.all_terms[term.exponent]
        else:
            self.all_terms[term.exponent] = term

    def get_degree(self):
        terms = self.all_terms
        try:
            exponents = [terms[t].exponent for t in terms.keys() if terms[t].coefficient != 0]
            self.degree = max(exponents)
        except:
            self.degree = 0
    
    def solve(self):
        """Solve Linear and Quadratic expressions."""

        if self.degree > 2:
            return "The polynomial degree is strictly greater than 2, I can't solve."
        
        elif self.degree == 0:
            """a * X^0 = 0""" 
            a = self.all_terms[0].coefficient
            if a != 0:
                return "The eqution has no solution"
            else:
                return "Every real number is a solution"

        elif self.degree == 1:
            """a * X^1 + b * X^0 = 0"""
            a = self.all_terms[1].coefficient
            b = self.all_terms[0].coefficient
            return formula.linear(a, b)

        elif self.degree == 2:
            """a * X^2 + b * X^1 + c * X^0 = 0"""
            a = self.all_terms[2].coefficient
            b = self.all_terms[1].coefficient
            c = self.all_terms[0].coefficient
            discriminant = (b ** 2) - (4 * a * c)
            two_a = 2 * a
            if discriminant == 0:
                return formula.linear(two_a, b)
            else:
                if discriminant > 0:
                    return formula.quadratic(two_a, b, discriminant)
                else:
                    return formula.quadratic(two_a, b, discriminant, simple=False)

    def calculate_with_variable(self, expression, variable):
        copy = Simple(expression, self.variable)
        return copy.calculate_with_variable(copy.expression, variable)

    @staticmethod
    def calculate(expression, rest):
        try:
            name, var = Simple.get_function_and_variable(expression)[:2]
        except:
            return Polynomial(expression, "x", rest).solution

        original = Data.everything[name]
        if var == original.variable:
            if rest == "0" and isinstance(original, Polynomial):
                return original.solution
            elif not rest:
                return str(original)

        expression = str(original).replace(" ", "")
        return Polynomial(expression, var, rest).solution

    @staticmethod
    def check_expression(expression):
        copy = expression.split("^")[1:]
        for c in copy:
            if not c[0].isdigit():
                raise SyntaxError