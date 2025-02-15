
from Data import Data
from Number import number, Rational, Number

class Variable:

    def abstract(self):
        self.expression = []
        self.variable = 0

    def process_variable(self, var):
        try:
            var = number(var)
            assert isinstance(var, Number)
        except:
            if self.variable and self.variable in var:
                var = self.get_the_variable(var)
            elif var in Data.everything:
                var = self.get_copy_from_data(var)
            else:
                raise TypeError(f"Incorrect or unknown variable '{var}'")
        self.expression.append(var)

    def get_the_variable(self, var):
        # 4x
        if self.variable != var:
            nb, var = var.split(self.variable)[0], self.variable
            # 4, x
            if Data.is_number(nb) and self.variable == var:
                self.expression.extend((number(nb), "*"))
        # x in ()
        else:
            self.reserved = True
        return var

    def get_copy_from_data(self, var):
        var = Data.everything[var]
        if hasattr(var, "expression"):
            if var.variable != self.variable:
                raise TypeError
            expression = str(var).replace(" ", "")
            var = self.__class__(expression, var.variable)
        return var

    def at_least_one_processed_var(self):
        for e in self.expression:
            if isinstance(e, Data) or (self.variable and e == self.variable):
                return True
        return False

    def find_variable(self, i, j=1):
        while i < len(self.expression):
            if self.expression[i] in ("+", "-"):
                if i == 1 and self.expression[i] == "-" and self.expression[i-1] == 0:
                    pass
                elif type(self.expression[i+j]) != str and not self.expression[i+j].reserved:
                    return i
            i += 1
        return -1

    def get_first(self, i):
        sign = self.expression.pop(i)
        first = self.expression.pop(i)
        if sign == "-":
            first = -first
        return first

    def get_second(self, s):
        sign = self.expression[s]
        second = self.expression[s+1]
        return sign, second

    def calculate_all_unreserved_vars(self, f=-1, s=-1):
        self.expression = [number(0), "+"] + self.expression
        f = self.find_variable(0)
        if f >= 0:
            s = self.find_variable(f+1)
        if s >= 0:
            first = self.get_first(f)
            s -= 2
            while s >= 0:
                sign, second = self.get_second(s)
                second = first.math(sign, second)
                if isinstance(second, Rational) and second < 0:
                    second = -second
                    self.expression[s] = "-"
                elif sign == "-":
                    self.expression[s] = "+"
                self.expression[s+1] = second
                f = s
                s = self.find_variable(s+2)
                if s >= 0:
                    first = self.get_first(f)
                    s -= 2
        while self.expression[0] == 0 and self.expression[1] == "+":
            del self.expression[:2]
        while self.expression[-1] == 0 and self.expression[-2] in "+-":
            del self.expression[-2:]