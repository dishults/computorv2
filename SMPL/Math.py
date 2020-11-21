from Data import Data
from Number import number, Rational, Complex

class Math(Data):

    def abstract(self):
        self.expression = []
        self.variable = None
        self.reserved = None
        self.negative = None

    def math(self, sign, other):
        return number(self.operations[sign](self, other))

    def this(self):
        return self.expression[0]

    def calculate_with_variable(self, expression, var):
        if isinstance(var, Data):
            new_var = var
        elif var in Data.everything:
            new_var = Data.everything[var]
        else:
            new_var = number(var)
        for i, v in enumerate(expression):
            if v == self.variable:
                expression[i] = new_var
            elif isinstance(v, Data):
                v.reserved = False
                if isinstance(v, self.__class__):
                    expression[i] = v.calculate_with_variable(v.expression[:], var)
        return self.calculate(expression)

    @staticmethod
    def calculate_function_with_variable(func, var):
        obj = Data.everything[func]
        return obj.calculate_with_variable(obj.expression[:], var)

    @staticmethod
    def calculate_plus_minus(expression, i=0):
        while i < len(expression):
            sign = expression[i]
            if sign in ("+", "-"):
                if not type(expression[i-1]) == str and not type(expression[i+1]) == str\
                        and not expression[i+1].reserved and not expression[i-1].reserved:
                    expression[i-1] = Math.do_math(expression, i, sign)
                    i = 0 ; continue
            i += 1
        return expression

    @staticmethod
    def merge_rational_and_complex(expression, one, two, i):
        if isinstance(expression[one], Complex) \
            and isinstance(expression[two], Rational):
            expression.pop(i)
            other = expression.pop(i if one < two else i-1)
            expression[i-1].rational = other
            return True
        return False


    @staticmethod
    def fix_complex_numbers(expression, i=0):
        while i < len(expression):
            if expression[i] in ("+", "-"):
                if Math.merge_rational_and_complex(expression, i-1, i+1, i) or\
                    Math.merge_rational_and_complex(expression, i+1, i-1, i):
                    continue
            i += 1

    @staticmethod
    def calculate(expression, i=0):
        while i < len(expression):
            sign = expression[i]
            if sign in ("/", "%", "*", "^"):
                if not Math.set_reserved(expression, i-1, i+1)\
                        and not Math.set_reserved(expression, i+1, i-1):
                    expression[i-1] = Math.do_math(expression, i, sign)
                    i = 0 ; continue
            i += 1
        Math.fix_complex_numbers(expression)
        Math.calculate_plus_minus(expression)
        if len(expression) == 1:
            return expression[0]
        return expression

    @staticmethod
    def do_math(expression, i, sign):
        expression.pop(i)
        other = expression.pop(i)
        res = expression[i-1].math(sign, other)
        if isinstance(other, Complex):
            return Complex(str(res))
        return res


    @staticmethod
    def set_reserved(expression, one, two):
        if type(expression[one]) == str or expression[one].reserved:
            if type(expression[two]) != str:
                expression[two].reserved = True
                return True
        return False