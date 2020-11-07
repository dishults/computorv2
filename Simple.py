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
        for c in equation:
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
                self.equation[0] *= -1
            else:
                self.equation[0] = "-" + self.equation[0]
    
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
            #var = Number.convert_to_num(var)
        except:
            if var in Data.everything:
                var = Data.everything[var]
            elif not self.var or self.var != var:
                raise ValueError
        self.equation.append(var)
    
    #def calculate(self, var=0):
