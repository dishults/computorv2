from Data import Data
from Number import Number, number

class Simple(Data):

    def __init__(self, variable, equation, sub_equation=False):
        self.equation = []
        self.var = variable
        self.sub_equation = sub_equation
        starts_with_minus = False
        if equation[0] == "-":
            equation = equation[1:]
            starts_with_minus = True
        self.get_variables(equation)
        if starts_with_minus:
            if isinstance(self.equation[0], Number):
                self.equation[0].number *= -1
            else:
                self.equation[0] = "-" + self.equation[0]
        if not variable and not sub_equation:
            self.calculate()

    def __str__(self):
        f = f"{self.equation[0]}"
        for e in self.equation[1:]:
            f += f" {e}"
        if self.sub_equation:
            f = "(" + f + ")"
        return f

    def __truediv__(self, other):
        self.calculate()
        return self.equation[0] / other

    def __mod__(self, other):
        self.calculate()
        return self.equation[0] % other

    def __mul__(self, other):
        self.calculate()
        return self.equation[0] * other

    def __add__(self, other):
        self.calculate()
        return self.equation[0] + other

    def __sub__(self, other):
        self.calculate()
        return self.equation[0] - other


    def __rtruediv__(self, other):
        self.calculate()
        return other / self.equation[0]

    def __rmod__(self, other):
        self.calculate()
        return other % self.equation[0]

    def __rmul__(self, other):
        self.calculate()
        return other * self.equation[0]

    def __radd__(self, other):
        self.calculate()
        return other + self.equation[0]

    def __rsub__(self, other):
        self.calculate()
        return other - self.equation[0]

    operations = {
        "/" : __truediv__,
        "%" : __mod__,
        "*" : __mul__,
        "+" : __add__,
        "-" : __sub__,
    }

    def math(self, sign, other):
        return number(self.operations[sign](self, other))

    def get_variables(self, equation):
        i = 0
        while i < len(equation):
            sign = equation[i]
            if sign in ("+", "-", "/", "%", "*"):
                var, equation = equation.split(sign, 1)
                if var:
                    self.proceed(var)
                    i = 0
                self.equation.append(sign)
            elif sign == "(":
                equation = equation[1:]
                braket = self.what_braket(equation)
                var = equation[:braket]
                equation = equation[braket+1:]
                self.equation.append(Simple(self.var, var, sub_equation=True))
                i = 0
            else:
                i += 1
        if equation and equation != ")":
            self.proceed(equation)

    def what_braket(self, equation):
        braket = 0
        for i, char in enumerate(equation):
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
        self.equation.append(var)

    def fix(self, var):
        if var:
            new_var = number(var)
            for i, v in enumerate(self.equation):
                if v == var:
                    self.equation[i] = new_var

    def calculate(self, var=0, signs=("/", "%", "*")):
        i = 0
        while i < len(self.equation):
            sign = self.equation[i]
            if sign in signs:
                self.equation.pop(i)
                other = self.equation.pop(i)
                self.equation[i - 1] = self.equation[i - 1].math(sign, other)
                i = 0
            else:
                i += 1
        if signs[0] == "/":
            self.calculate(signs=("+", "-"))

