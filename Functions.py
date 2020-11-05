from Data import Data
from Polynomials import Polynomials
from Numbers import Numbers

class Functions(Data):

    def __init__(self, name, equation):
        self.name, var = name.split("(")
        self.var = var.strip("()")
        self.equation = []
        if "^" in equation:
            self.polynomials(equation)
        else:
            self.simple(equation)
    
    def __str__(self):
        if self.type == "simple":
            f = " "
            for e in self.equation:
                f += f" {e}"
            return f
        else:
            return str(self.equation)

    def simple(self, equation):
        self.type = "simple"
        starts_with_minus = False
        if equation[0] == "-":
            equation = equation[1:]
            starts_with_minus = True
        for c in equation:
            if c in ("+", "-", "/", "%", "*"):
                var, equation = equation.split(c)
                try:
                    var = Numbers.convert_to_num(var)
                except:
                    if self.var != var:
                        raise ValueError
                self.equation.append(var)
                self.equation.append(c)
        try:
            equation = Numbers.convert_to_num(equation)
        except:
            if self.var != equation:
                raise ValueError
        self.equation.append(equation)
        if starts_with_minus and type(self.equation[0]) in (int, float):
            self.equation[0] *= -1

    def polynomials(self, equation):
        self.type = "polynomial"
        self.equation = Polynomials(self.var, equation)
