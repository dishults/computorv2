from Data import Data
from Simple import Simple
from Polynomial import Polynomial

class Function(Data):

    def __init__(self, name, equation):
        self.name, var = name.split("(")
        self.var = var.strip("()")
        if "^" in equation:
            self.equation = Polynomial(self.var, equation)
        else:
            self.equation = Simple(self.var, equation)
    
    def __str__(self):
        return " " + str(self.equation)
