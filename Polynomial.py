import sys

import POLY.formula as formula

from Data import Data
from Simple import Simple
from POLY.Term import Term

class Polynomial(Data):
    
    def __init__(self, variable, expression, inverse=False):
        self.all_terms = {}
        self.variable = variable
        expression = expression.replace("*", "")
        expression = expression.replace("^", "")
        previous = "+"
        if expression[0] == "-":
            previous = "-"
            expression = expression[1:]
        for sign in expression:
            if sign in ("+", "-"):
                term, expression = expression.split(sign, 1)
                self.proceed(term, previous, variable, inverse)
                previous = sign
        self.proceed(expression, previous, variable, inverse)
        self.get_degree()

    def __str__(self):
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

    def __isub__(self, other):
        for term in other.all_terms:
            if term in self.all_terms:
                self.all_terms[term].coefficient += other.all_terms[term].coefficient
                if term > 2 and self.all_terms[term].coefficient == 0:
                    del self.all_terms[term]
            else:
                self.all_terms[term] = other.all_terms[term].coefficient
        self.get_degree()
        return self

    def proceed(self, term, sign, variable, inverse=False):
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
            if term.exponent > 0 and self.all_terms[term.exponent].coefficient == 0:
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
            return"The polynomial degree is strictly greater than 2, I can't solve."
        
        elif self.degree == 0:
            """a * X^0 = 0""" 
            a = self.all_terms[0].coefficient
            if a != 0:
                return"The eqution has no solution"
            return"Every real number is a solution"

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

    @staticmethod
    def calculate(expression, rest):
        i = expression.index("(")
        braket = Simple.what_braket(expression, -1)
        func = expression[:i]
        var = expression[i+1:braket]
        original = Data.everything[func]
        expression = str(original)

        if var == original.variable and rest == "0":
            return expression + " = 0\n  " + original.solve()

        expression = expression.replace(" ", "")
        if Data.is_number(var):
            num = var
            var = original.variable
            copy = Simple(var, expression)
            res = copy.calculate_with_variable(num, copy.expression)
            if not rest:
                return res
            expression = str(res)

        copy = Polynomial(var, expression)
        rest = Polynomial(var, rest, inverse=True)
        copy -= rest
        return str(copy) + " = 0\n  " + copy.solve()
