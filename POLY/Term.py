from Data import Data

class Term:

    def __init__(self, sign, coefficient, variable, exponent, inverse=False):
        """Example -- '+', '5', 'X', '0'"""
        if not coefficient:
            coefficient = "1"
        try:
            self.coefficient = float(coefficient)
            if sign == "-" and self.coefficient > 0: # just sign == "-"?
                self.coefficient *= -1
            if inverse:
                self.coefficient *= -1
        except:
            self.coefficient = Data.everything[coefficient]
        self.variable = variable
        self.exponent = int(exponent)
    
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