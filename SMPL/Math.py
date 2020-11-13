from abc import abstractmethod

from Number import number

class Math:

    @abstractmethod
    def abstract(self):
        self.expression = None
        self.reserved = None
        self.negative = None

    def __truediv__(self, other):
        return self.expression[0] / other

    def __mod__(self, other):
        return self.expression[0] % other

    def __mul__(self, other):
        return self.expression[0] * other

    def __add__(self, other):
        return self.expression[0] + other

    def __sub__(self, other):
        if self.expression[0] < 0 and other < 0:
            return self.expression[0] + other
        return self.expression[0] - other

    def __pow__(self, other):
        return self.expression[0] ** other


    def __rtruediv__(self, other):
        return other / self.expression[0]

    def __rmod__(self, other):
        return other % self.expression[0]

    def __rmul__(self, other):
        return other * self.expression[0]

    def __radd__(self, other):
        return other + self.expression[0]

    def __rsub__(self, other):
        return other - self.expression[0]

    def __rpow__(self, other):
        return other ** self.expression[0]

    operations = {
        "/" : __truediv__,
        "%" : __mod__,
        "*" : __mul__,
        "^" : __pow__,
        "+" : __add__,
        "-" : __sub__,
    }

    def math(self, sign, other):
        res = number(self.operations[sign](self, other))
        if self.negative:
            return -res
        return res

    def __neg__(self):
        if self.reserved:
            self.negative = True
            return self
        else:
            return self.math("*", -1)

    def calculate_plus_minus(self, expression):
        i = 0
        while i < len(expression):
            sign = expression[i]
            if sign in ("+", "-"):
                if type(expression[i-1]) == str or type(expression[i+1]) == str or\
                    expression[i+1].reserved or expression[i-1].reserved:
                    i += 1
                else:
                    expression.pop(i)
                    other = expression.pop(i)
                    expression[i-1] = expression[i-1].math(sign, other)
                    i = 0
            else:
                i += 1
        return expression

    def calculate(self, expression):
        i = 0
        while i < len(expression):
            sign = expression[i]
            if sign in ("/", "%", "*", "^"):
                if type(expression[i-1]) == str or expression[i-1].reserved:
                    expression[i+1].reserved = True
                    i += 1
                elif type(expression[i+1]) == str or expression[i+1].reserved:
                    expression[i-1].reserved = True
                    i += 1
                else:
                    expression.pop(i)
                    other = expression.pop(i)
                    expression[i-1] = expression[i-1].math(sign, other)
                    i = 0
            else:
                i += 1
        res = self.calculate_plus_minus(expression)
        if len(res) == 1:
            res = res[0]
        return res