from Data import Data
from Number import Number

class Term:

    def __init__(self, sign, coefficient, variable, exponent, inverse=False):
        """Example -- '+', '5', 'X', '0'"""
        if not coefficient:
            coefficient = "1"
        try:
            self.coefficient = Number.convert_to_num(coefficient)
            if sign == "-" and self.coefficient > 0:
                self.coefficient *= -1
            if inverse:
                self.coefficient *= -1
        except:
            try:
                self.coefficient = Data.everything[coefficient]
                assert Data.is_number(self.coefficient)
            except AssertionError:
                raise TypeError(f"Expected number, got '{self.coefficient}'")
            except:
                raise TypeError(f"Wrong coefficient '{coefficient}'")
        self.variable = variable
        self.exponent = int(exponent)
    
    def __str__(self):
        num = abs(self.coefficient)
        if self.exponent == 0:
            return f"{num}"
        elif self.exponent == 1:
            if num == 1:
                return f"{self.variable}"
            else:
                return f"{num}{self.variable}"
        elif self.exponent > 1:
            if num == 1:
                return f"{self.variable}^{self.exponent}"
            else:
                return f"{num} * {self.variable}^{self.exponent}"