from Data import Data
from Number import Number, number
from SMPL.Math import Math
from SMPL.Variable import Variable

class Simple(Math, Variable, Data):

    def __init__(self, variable, expression, sub_expression=False):
        self.expression = []
        self.var = variable
        self.sub_expression = sub_expression
        self.reserved = False
        self.negative = False
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
        self.calculate(self.expression)
        self.calculate_all_unreserved_vars()
        if not self.at_least_one_processed_var():
            raise SyntaxError

    def __str__(self):
        f = f"{self.expression[0]}"
        for e in self.expression[1:]:
            f += f" {e}"
        if self.sub_expression:
            f = "(" + f + ")"
        return f

    def get_variables(self, expression):
        i = 0
        while i < len(expression):
            sign = expression[i]
            if sign in ("+", "-", "/", "%", "*", "^"):
                var, expression = expression.split(sign, 1)
                if var:
                    self.process_variable(var)
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
            self.process_variable(expression)

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
            elif isinstance(v, Data):
                v.reserved = False
                if isinstance(v, Simple):
                    expression[i] = v.calculate_with_variable(var, v.expression[:])
        return self.calculate(expression)