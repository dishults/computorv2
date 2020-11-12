from Data import Data
from Number import Number, number

class Simple(Data):

    def __init__(self, variable, expression, sub_expression=False):
        self.expression = []
        self.var = variable
        self.sub_expression = sub_expression
        starts_with_minus = False
        if expression[0] == "-":
            expression = expression[1:]
            starts_with_minus = True
        self.get_variables(expression)
        if starts_with_minus:
            if isinstance(self.expression[0], Number):
                self.expression[0].number *= -1
            else:
                self.expression[0] = "-" + self.expression[0]
        if not variable and not sub_expression:
            self.calculate(self.expression)
        if not self.at_least_one_processed_var():
            raise SyntaxError

    def __str__(self):
        f = f"{self.expression[0]}"
        for e in self.expression[1:]:
            f += f" {e}"
        if self.sub_expression:
            f = "(" + f + ")"
        return f

    def __truediv__(self, other):
        res = self.calculate(self.expression[:])
        return res / other

    def __mod__(self, other):
        res = self.calculate(self.expression[:])
        return res % other

    def __mul__(self, other):
        res = self.calculate(self.expression[:])
        return res * other

    def __add__(self, other):
        res = self.calculate(self.expression[:])
        return res + other

    def __sub__(self, other):
        res = self.calculate(self.expression[:])
        return res - other


    def __rtruediv__(self, other):
        res = self.calculate(self.expression[:])
        return other / res

    def __rmod__(self, other):
        res = self.calculate(self.expression[:])
        return other % res

    def __rmul__(self, other):
        res = self.calculate(self.expression[:])
        return other * res

    def __radd__(self, other):
        res = self.calculate(self.expression[:])
        return other + res

    def __rsub__(self, other):
        res = self.calculate(self.expression[:])
        return other - res

    operations = {
        "/" : __truediv__,
        "%" : __mod__,
        "*" : __mul__,
        "+" : __add__,
        "-" : __sub__,
    }

    def math(self, sign, other):
        return number(self.operations[sign](self, other))

    def get_variables(self, expression):
        i = 0
        while i < len(expression):
            sign = expression[i]
            if sign in ("+", "-", "/", "%", "*"):
                var, expression = expression.split(sign, 1)
                if var:
                    self.proceed(var)
                    i = 0
                self.expression.append(sign)
            elif sign == "(":
                if expression[0] == "(":
                    expression = expression[1:]
                    braket = self.what_braket(expression)
                    var = expression[:braket]
                    expression = expression[braket+1:]
                    res = Simple(self.var, var, sub_expression=True)
                else:
                    braket = self.what_braket(expression, -1)
                    func = expression[:i]
                    var = expression[i+1:braket]
                    expression = expression[braket+1:]
                    res = Data.calculate(func, var)
                self.expression.append(res)
                i = 0
            else:
                i += 1
        if expression and expression != ")":
            self.proceed(expression)

    def what_braket(self, expression, braket=0):
        braket = braket
        for i, char in enumerate(expression):
            if char == "(":
                braket += 1
            elif char == ")":
                if not braket:
                    break
                else:
                    braket -= 1
        return i

    def proceed(self, var):
        try:
            var = number(var)
        except:
            if var in Data.everything:
                var = Data.everything[var]
            elif not self.var or self.var != var:
                raise ValueError
        self.expression.append(var)

    def at_least_one_processed_var(self):
        for e in self.expression:
            if isinstance(e, Data):
                return True
        return False

    def calculate(self, expression, signs=("/", "%", "*")):
        i = 0
        while i < len(expression):
            sign = expression[i]
            if sign in signs:
                expression.pop(i)
                other = expression.pop(i)
                expression[i - 1] = expression[i - 1].math(sign, other)
                i = 0
            else:
                i += 1
        if signs[0] == "/":
            return self.calculate(expression, signs=("+", "-"))[0]
        return expression

    def calculate_with_variable(self, var, expression):
        negative_var = "-" + self.var
        if isinstance(var, Data):
            new_var = var
        elif var in Data.everything:
            new_var = Data.everything[var]
        else:
            new_var = number(var) #get_type()
        for i, v in enumerate(expression):
            if v == self.var:
                expression[i] = new_var
            elif v == negative_var:
                expression[i] = -new_var
        return self.calculate(expression)