from Data import Data
from Number import Number, Rational, Complex

class Simple(Data):

    def __init__(self, variable, equation, sub_equation=False):
        self.equation = []
        self.var = variable
        self.sub_equation = sub_equation
        starts_with_minus = False
        if equation[0] == "-":
            equation = equation[1:]
            starts_with_minus = True
        for c in equation: # change to while loop
            if c in ("+", "-", "/", "%", "*"):
                var, equation = equation.split(c, 1)
                self.proceed(var)
                self.equation.append(c)
            elif c == "(":
                equation = equation.strip("(")
                var, equation = equation.rsplit(")", 1)
                self.equation.append(Simple(variable, var, sub_equation=True))
                if not equation:
                    break
        if equation:
            self.proceed(equation)
        if starts_with_minus:
            if isinstance(self.equation[0], Number):
                self.equation[0].number *= -1
            else:
                self.equation[0] = "-" + self.equation[0]
        if not variable and not sub_equation:
            self.calculate()
    
    def __str__(self):
        f = f"{self.equation[0]}"
        for e in self.equation[1:]:
            f += f" {e}"
        if self.sub_equation:
            f = "(" + f + ")"
        return f
    
    def proceed(self, var):
        try:
            var = Rational(var)
        except:
            if var in Data.everything:
                var = Data.everything[var]
            elif not self.var or self.var != var:
                raise ValueError
        self.equation.append(var)

    def fix(self, var):
        if var:
            new_var = Rational(var)
            for i, v in enumerate(self.equation):
                if v == var:
                    self.equation[i] = new_var

    def calculate(self, var=0):        
        for i, sign in enumerate(self.equation):
            if sign in ("/", "%", "*"):
                self.equation.pop(i)
                other = self.equation.pop(i)
                if isinstance(other, Simple):
                    other.calculate()
                    other = other.equation[0]
                self.equation[i - 1].math(sign, other)

        for i, sign in enumerate(self.equation):
            if sign in ("+", "-"):
                self.equation.pop(i)
                other = self.equation.pop(i)
                self.equation[i - 1].math(sign, other)
