from abc import abstractmethod

from Data import Data
from Number import number

class Variable:

    @abstractmethod
    def abstract(self):
        self.expression = None
        self.var = None
        self.sub_expression = None

    def process_variable(self, var):
        try:
            var = number(var)
        except:
            if var in Data.everything:
                var = Data.everything[var]
            elif self.var in var:
                if self.var != var:
                    nb, var = var.split(self.var)[0], self.var
                    if nb.isdigit():
                        self.expression.extend((number(nb), "*"))
                    else:
                        raise TypeError
                if self.sub_expression:
                    self.reserved = True
            else:
                raise TypeError
        self.expression.append(var)

    def at_least_one_processed_var(self):
        for e in self.expression:
            if isinstance(e, Data):
                return True
        return False

    def find_variable(self, i, j=1):
        while i < len(self.expression):
            if self.expression[i] in ("+", "-"):
                if type(self.expression[i+j]) != str and not self.expression[i+j].reserved:
                    return i
            i += 1
        return -1

    def get_first(self, i, j=0):
        sign = self.expression[i]
        self.expression.pop(i)
        if sign == "-":
            self.expression[i] = -self.expression[i]
        return self.expression.pop(i+j)

    def get_second(self, s):
        sign = self.expression[s]
        second = self.expression[s+1]
        if sign == "-":
            second = -second
        return sign, second

    def calculate_all_unreserved_vars(self, f=-1, s=-1):
        f = self.find_variable(0, -1)
        if f >= 0:
            s = self.find_variable(f + 1)
        if s >= 0:
            first = self.get_first(f, -1)
            s -= 2
            while s >= 0:
                sign, second = self.get_second(s)
                second = first.math(sign, second)
                self.expression[s+1] = second
                if self.expression[s+1] < 0:
                    self.expression[s+1] = -self.expression[s+1]
                    self.expression[s] = "-"
                f = s
                s = self.find_variable(s + 2)
                if s >= 0:
                    first = self.get_first(f)
                    s -= 2