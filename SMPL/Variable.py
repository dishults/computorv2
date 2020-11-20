
from Data import Data
from Number import number

class Variable:

    def abstract(self):
        self.expression = []
        self.variable = 0
        self.sub_expression = None

    def process_variable(self, var):
        try:
            var = number(var)
        except:
            if self.variable and self.variable in var:
                # 4x
                if self.variable != var:
                    nb, var = var.split(self.variable)[0], self.variable
                    # 4, x
                    if Data.is_number(nb) and self.variable == var:
                        self.expression.extend((number(nb), "*"))
                # x in ()
                if self.sub_expression:
                    self.reserved = True
            elif var in Data.everything:
                var = Data.everything[var]
            else:
                raise TypeError
        try:
            if self.expression[-1] == "-":
                var = -var
        except:
            pass
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
        self.expression.pop(i)
        return self.expression.pop(i+j)

    def get_second(self, s):
        sign = self.expression[s]
        second = self.expression[s+1]
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
                f = s
                s = self.find_variable(s + 2)
                if s >= 0:
                    first = self.get_first(f)
                    s -= 2