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
            self.calculate(self.equation)
        if not self.at_least_one_processed_var():
            raise SyntaxError

    def __str__(self):
        f = f"{self.equation[0]}"
        for e in self.equation[1:]:
            f += f" {e}"
        if self.sub_equation:
            f = "(" + f + ")"
        return f

    def __truediv__(self, other):
        res = self.calculate(self.equation[:])
        return res / other

    def __mod__(self, other):
        res = self.calculate(self.equation[:])
        return res % other

    def __mul__(self, other):
        res = self.calculate(self.equation[:])
        return res * other

    def __add__(self, other):
        res = self.calculate(self.equation[:])
        return res + other

    def __sub__(self, other):
        res = self.calculate(self.equation[:])
        return res - other


    def __rtruediv__(self, other):
        res = self.calculate(self.equation[:])
        return other / res

    def __rmod__(self, other):
        res = self.calculate(self.equation[:])
        return other % res

    def __rmul__(self, other):
        res = self.calculate(self.equation[:])
        return other * res

    def __radd__(self, other):
        res = self.calculate(self.equation[:])
        return other + res

    def __rsub__(self, other):
        res = self.calculate(self.equation[:])
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
                if equation[0] == "(":
                    equation = equation[1:]
                    braket = self.what_braket(equation)
                    var = equation[:braket]
                    equation = equation[braket+1:]
                    res = Simple(self.var, var, sub_equation=True)
                else:
                    braket = self.what_braket(equation, -1)
                    func = equation[:i]
                    var = equation[i+1:braket]
                    equation = equation[braket+1:]
                    res = Data.calculate(func, var)
                self.equation.append(res)
                i = 0
            else:
                i += 1
        if equation and equation != ")":
            self.proceed(equation)

    def what_braket(self, equation, braket=0):
        braket = braket
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

    def at_least_one_processed_var(self):
        for e in self.equation:
            if isinstance(e, Data):
                return True
        return False

    def calculate(self, equation, signs=("/", "%", "*")):
        i = 0
        while i < len(equation):
            sign = equation[i]
            if sign in signs:
                equation.pop(i)
                other = equation.pop(i)
                equation[i - 1] = equation[i - 1].math(sign, other)
                i = 0
            else:
                i += 1
        if signs[0] == "/":
            return self.calculate(equation, signs=("+", "-"))[0]
        return equation

    def calculate_with_variable(self, var, equation):
        negative_var = "-" + self.var
        if var in Data.everything:
            new_var = Data.everything[var]
        else:
            new_var = number(var) #get_type()
        for i, v in enumerate(equation):
            if v == self.var:
                equation[i] = new_var
            elif v == negative_var:
                equation[i] = -new_var
        return self.calculate(equation)