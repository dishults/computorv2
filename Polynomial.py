import sys

from Data import Data

class Polynomial(Data):
    
    def __init__(self, variable, equation):       
        self.all_terms = {}
        equation = equation.replace("*", "")
        equation = equation.replace("^", "")
        previous = "+"
        if equation[0] == "-":
            previous = "-"
            equation = equation[1:]
        for sign in equation:
            if sign in ("+", "-"):
                term, equation = equation.split(sign, 1)
                self.proceed(term, previous, variable)
                previous = sign
        self.proceed(equation, previous, variable)
        #self.get_degree()

    def __str__(self):
        p = ""
        terms_in_reverse__order = sorted(self.all_terms, reverse=True)
        term = self.all_terms[terms_in_reverse__order[0]]
        if term.coefficient < 0:
            p += "-"
        p += str(term)
        for t in terms_in_reverse__order[1:]:
            term = self.all_terms[t]
            if term.coefficient > 0:
                sign = " +"
            else:
                sign = " -"
            p += f"{sign} {term}"
        return p

    def proceed(self, term, sign, variable):
        try: # 5x^2
            coefficient, exponent = term.split(variable) 
            assert exponent
        except AssertionError: # 5x
            coefficient = term.strip(variable) 
            exponent = 1
        except ValueError: # 5
            coefficient = term
            exponent = 0
        term = Terms(sign, coefficient, variable, exponent)
        if term.exponent in self.all_terms:
            self.all_terms[term.exponent].coefficient += term.coefficient
            if self.all_terms[term.exponent].coefficient == 0:
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
    
    @classmethod
    def solve(cls):
        """Solve Linear and Quadratic equations."""

        if cls.degree > 2:
            sys.exit("The polynomial degree is strictly greater than 2, I can't solve.")
        
        if cls.degree == 0:
            """n * X^0 = 0"""            
            n = all_terms[0].coefficient
            if n != 0:
                sys.exit("The eqution has no solution")
            print("Every real number is a solution")

        elif cls.degree == 1:
            print("b * X^0 + a * X^1 = 0")
            a = all_terms[1].coefficient
            b = all_terms[0].coefficient
            print("\nLinear Formula:")
            print(linear_formula.__doc__)
            print("a = ", a)
            print("b = ", b)
            linear_formula(a, b)

        elif cls.degree == 2:
            print("c * X^0 + b * X^1 + a * X^2 = 0")
            a = all_terms[2].coefficient
            b = all_terms[1].coefficient
            c = all_terms[0].coefficient
            discriminant = (b ** 2) - (4 * a * c)
            two_a = 2 * a

            print("\nQuadratic Formula:")
            print(quadratic_formula.__doc__)
            print("a = ", a)
            print("b = ", b)
            print("c = ", c)
            print("2a = ", two_a)
            print("discriminant (b^2 - 4ac) = ", discriminant)
            if discriminant == 0:
                print("\n\033[1mDiscriminant is 0\033[0m")
                print("To solve we would have to do: x = -b / 2a")
                linear_formula(two_a, b)
            else:
                if discriminant > 0:
                    print("\n\033[1mDiscriminant is strictly positive.\033[0m")
                    quadratic_formula(two_a, b, discriminant)
                else:
                    print("\n\033[1mDiscriminant is strictly negative.\033[0m",
                          "\nSo we would have to calculate complex solutions",
                          "with real and imaginary parts")
                    quadratic_formula(two_a, b, discriminant, simple=False)


def linear_formula(a, b):
    """
    x = -b / a
    """

    print("\nThe solution is:")
    if b == 0 and a == 0:
        print("Every real number is a solution")
    elif a == 0:
        sys.exit("The eqution has no solution")
    elif b == 0:
        print(0)
    else:
        print(f"\033[1m{-b / a}\033[0m")
    
def quadratic_formula(two_a, b, discriminant, simple=True):
    """
        -b +- sqrt(b^2 - 4ac)
    x = —————————————————————
                2a
    """
    if simple:
        sqrt = discriminant ** 0.5
        print("sqrt (discriminant ** 0.5) =", sqrt)
        x1 = (-b - sqrt) / two_a
        x2 = (-b + sqrt) / two_a
        print("\nThe two solutions are:")
        print("x1 (-b - sqrt) / 2a =\033[1m", round(x1, 6), "\033[0m")
        print("x2 (-b + sqrt) / 2a =\033[1m", round(x2, 6), "\033[0m")
    else:
        discriminant *= -1
        print(f"\n=> convert discriminant (b^2 - 4ac) to positive = {discriminant}")
        sqrt = discriminant ** 0.5
        print("=> calculate sqrt (discriminant ** 0.5) =", sqrt)
        real = -b / two_a
        print("=> calculate real part (-b / two_a) = ", real)
        imaginary = sqrt / two_a
        print("=> calculate imaginary part (sqrt / 2a) = ", imaginary)
        print("\nThe two complex solutions are:")
        print(f"real - imaginary = \033[1m{round(real, 6)} - {round(imaginary, 6)}i\033[0m")
        print(f"real + imaginary = \033[1m{round(real, 6)} + {round(imaginary, 6)}i\033[0m")

class Terms:

    def __init__(self, sign, coefficient, variable, exponent, inverse=False):
        """Example -- '+', '5', 'X', '0'"""
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
            return f"{num} * {self.variable}^{self.exponent}"
        elif self.exponent == 1:
            return f"{num}*{self.variable}"
        elif self.exponent == 0:
            return f"{num}"
