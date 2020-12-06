from Data import Data
from Number import number, Rational, Complex
from Matrix import Matrix

class Math(Data):

    def abstract(self):
        self.variable = None
        self.reserved = None
        self.negative = None

    def math(self, sign, other):
        return number(super().math(sign, other))

    def convert_variable(self, var):
        if isinstance(var, Data):
            return var
        elif var in Data.everything:
            return Data.everything[var]
        elif Data.is_number(var):
            return number(var)
        elif var == self.variable:
            raise ValueError
        else:
            raise SyntaxError(
            f"Wrong variable '{var}', expected '{self.variable}' or number")

    def calculate_with_variable(self, expression, var):
        var = self.convert_variable(var)
        for i, v in enumerate(expression):
            if type(v) == type(self.variable) and v == self.variable:
                expression[i] = var
            elif isinstance(v, Data):
                v.reserved = False
                if isinstance(v, self.__class__):
                    expression[i] = v.calculate_with_variable(v.expression[:], var)
        return self.calculate(expression)

    @staticmethod
    def calculate_function_with_variable(func, var):
        if func == "transpose":
            T = Matrix.transpose(var)
            if len(T) == 1:
                return Matrix(T[0])
            return T
        obj = Data.everything[func]
        return obj.calculate_with_variable(obj.expression[:], var)

    @staticmethod
    def calculate_plus_minus(expression, i=1):
        while i < len(expression):
            sign = expression[i]
            if sign in ("+", "-"):
                if not type(expression[i-1]) == str and not type(expression[i+1]) == str\
                        and not expression[i+1].reserved and not expression[i-1].reserved:
                    expression[i-1] = Math.do_math(expression, i, sign)
                    continue
            i += 2
        return expression

    @staticmethod
    def calculate_high_precedence(expression, operators, i=1):
        while i < len(expression):
            operator = expression[i]
            if operator in operators:
                if not Math.set_reserved(expression, i-1, i+1)\
                        and not Math.set_reserved(expression, i+1, i-1):
                    expression[i-1] = Math.do_math(expression, i, operator)
                    continue
            i += 2

    @staticmethod
    def calculate(expression, i=1):
        Math.calculate_high_precedence(expression, ("^",))
        Math.calculate_high_precedence(expression, ("/", "%", "*", "@"))
        Math.calculate_plus_minus(expression)
        if len(expression) == 1:
            return expression[0]
        return expression

    @staticmethod
    def do_math(expression, i, sign):
        expression.pop(i)
        other = expression.pop(i)
        return expression[i-1].math(sign, other)


    @staticmethod
    def set_reserved(expression, one, two):
        if type(expression[one]) == str or expression[one].reserved:
            if type(expression[two]) != str:
                expression[two].reserved = True
            return True
        return False