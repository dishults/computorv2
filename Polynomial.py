import sys

from Data import Data

class Polynomial(Data):
    
    def __init__(self, variable, expression, inverse=False):
        self.all_terms = {}
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
        if term.exponent > 0 and term.coefficient != 0:
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
        return p

    def __isub__(self, other):
        for term in other.all_terms:
            if term in self.all_terms:
                self.all_terms[term].coefficient += other.all_terms[term].coefficient
                if term > 2 and self.all_terms[term].coefficient == 0:
                    del self.all_terms[term]
            else:
                self.all_terms[term] = other.all_terms[term].coefficient
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
        term = Terms(sign, coefficient, variable, exponent, inverse)
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
            n = self.all_terms[0].coefficient
            if n != 0:
                return"The eqution has no solution"
            return"Every real number is a solution"

        elif self.degree == 1:
            a = self.all_terms[1].coefficient
            b = self.all_terms[0].coefficient
            return linear_formula(a, b)

        elif self.degree == 2:
            a = self.all_terms[2].coefficient
            b = self.all_terms[1].coefficient
            c = self.all_terms[0].coefficient
            discriminant = (b ** 2) - (4 * a * c)
            two_a = 2 * a
            if discriminant == 0:
                return linear_formula(two_a, b)
            else:
                if discriminant > 0:
                    return quadratic_formula(two_a, b, discriminant)
                else:
                    return quadratic_formula(two_a, b, discriminant, simple=False)

    @staticmethod
    def calculate(expression, rest):
        i = expression.index("(")
        braket = Polynomial.what_braket(expression, -1)
        func = expression[:i]
        var = expression[i+1:braket]

        original = str(Data.everything[func])
        original = original.replace(" ", "")
        copy = Polynomial(var, original)
        rest = Polynomial(var, rest, inverse=True)
        copy -= rest
        return str(copy) + " = 0\n  " + copy.solve()

    @staticmethod
    def what_braket(expression, braket=0):
        braket = braket
        for i, char in enumerate(expression):
            if char == "(":
                braket += 1
            elif char == ")":
                if not braket:
                    break
                else:
                    braket -= 1
        return i


def linear_formula(a, b):
    """
    x = -b / a
    """

    res = "The solution is:\n"
    if b == 0 and a == 0:
        return res + "  Every real number is a solution"
    elif a == 0:
        return res + "  The eqution has no solution"
    elif b == 0:
        return res + "  0"
    else:
        return res + f"  {-b / a}"
    
def quadratic_formula(two_a, b, discriminant, simple=True):
    """
        -b +- sqrt(b^2 - 4ac)
    x = —————————————————————
                2a
    """
    if two_a == 0:
        return "The eqution has no solution"
    elif simple:
        sqrt = discriminant ** 0.5
        x1 = (-b - sqrt) / two_a
        x2 = (-b + sqrt) / two_a
        res = "The two R solutions are:\n"
        res += f"  {round(x1, 6)}\n"
        res += f"  {round(x2, 6)}"
    else:
        discriminant *= -1
        sqrt = discriminant ** 0.5
        real = -b / two_a
        imaginary = sqrt / two_a
        res = "The two C solutions are:\n"
        res += f"  {round(real, 6)} - {round(imaginary, 6)}i\n"
        res += f"  {round(real, 6)} + {round(imaginary, 6)}i"
    return res

class Terms:

    def __init__(self, sign, coefficient, variable, exponent, inverse=False):
        """Example -- '+', '5', 'X', '0'"""
        if not coefficient:
            coefficient = "1"
        try:
            self.coefficient = float(sign + coefficient)
        except:
            self.coefficient = float(coefficient)
        self.variable = variable
        self.exponent = int(exponent)
        if inverse:
            self.coefficient *= -1
    
    def __str__(self):
        num = abs(self.coefficient)
        if num % 1 == 0:
            num = int(num)
        if self.exponent > 1:
            if num == 1:
                return f"{self.variable}^{self.exponent}"
            else:
                return f"{num} * {self.variable}^{self.exponent}"
        elif self.exponent == 1:
            if num == 1:
                return f"{self.variable}"
            else:
                return f"{num}{self.variable}"
        elif self.exponent == 0:
            return f"{num}"
