from Data import Data
from Number import Number, Rational, Complex, number
from SMPL.Math import Math
from SMPL.Variable import Variable

class Simple(Math, Variable):

    def __init__(self, expression, variable=0):
        self.expression = []
        self.variable = variable
        self.reserved = False
        self.negative = False
        if expression[0] == "-":
            expression = f"0{expression}"
        self.get_variables(expression)
        self.check_variables()
        self.calculate(self.expression)
        if len(self.expression) > 1:
            self.calculate_all_unreserved_vars()
        if not self.at_least_one_processed_var():
            raise SyntaxError

    def __str__(self):

        def brakets_or_not(e):
            if (isinstance(e, Complex) and e.real and e.imaginary) \
                    or isinstance(e, Simple):
                return f"({e})"
            return f"{e}"

        if len(self.expression) == 1:
            f = f"{self.expression[0]}"
        else:
            f = brakets_or_not(self.expression[0])
        for e in self.expression[1:]:
            f = f"{f} {brakets_or_not(e)}"
        f = f.replace("0 - ", "-")
        f = f.replace("+ -", "- ")
        f = f.replace("- -", "- ")
        return f

    def get_variables(self, expression):
        expression = self.fix_negatives(expression)
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
                func, var, expression = self.get_function_and_variable(expression, i)
                if func:
                    res = self.calculate_function_with_variable(func, var)
                else:
                    res = Simple(var, self.variable)
                    if len(res.expression) == 1:
                        res = res.expression[0]
                self.expression.append(res)
                i = 0
            else:
                i += 1
        if expression and expression != ")":
            self.process_variable(expression)

    def check_variables(self):
        instances = sum(1 for v in self.expression if isinstance(v, Data) or v == self.variable)
        operators = sum(1 for v in self.expression if v in ("+", "-", "/", "%", "*", "^"))
        if instances - 1 != operators:
            raise SyntaxError

    @staticmethod
    def fix_negatives(expression, i=0):
        for operation in ("^-", "*-", "/-", "%-"):
            if operation in expression:
                while i < len(expression):
                    if expression[i] in "^*/%" and expression[i+1] == "-":
                        start = i+1
                        i += 2
                        while i < len(expression) and not expression[i] in "+-^*/%":
                            i += 1
                        if i != len(expression):
                            end = expression[i:]
                        else:
                            end = ""
                        expression = f"{expression[:start]}(-{expression[start+1:i]}){end}"
                        i += 1
                    i += 1
                break
        return expression

    @staticmethod
    def what_braket(expression, braket=0):
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

    @staticmethod
    def get_function_and_variable(expression, i=None, func=0):
        if "=" in expression:
            expression = expression.split("=")[0]
        if i == None:
            i = expression.index("(")
        if i:
            braket = Simple.what_braket(expression, -1)
            func = expression[:i]
            while func and not func.isalpha():
                for c in func:
                    if not c.isalpha():
                        func = func.split(c)[-1]
                        break
        else:
            braket = Simple.what_braket(expression[1:]) + 1
        var = expression[i+1:braket]
        expression = expression[braket+1:]
        return func, var, expression