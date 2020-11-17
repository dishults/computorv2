from Data import Data
from Number import number

class Math(Data):

    def abstract(self):
        self.expression = []
        self.var = None
        self.reserved = None
        self.negative = None

    def __neg__(self):
        if self.reserved:
            self.negative = True
            return self
        else:
            return super().__neg__()

    def math(self, sign, other):
        res = number(self.operations[sign](self, other))
        if self.negative:
            return -res
        return res

    def this(self):
        return self.expression[0]

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
                if isinstance(v, self.__class__):
                    expression[i] = v.calculate_with_variable(var, v.expression[:])
        return self.calculate(expression)

    @staticmethod
    def calculate_plus_minus(expression):
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

    @staticmethod
    def calculate(expression):
        i = 0
        while i < len(expression):
            sign = expression[i]
            if sign in ("/", "%", "*", "^"):
                if type(expression[i-1]) == str or expression[i-1].reserved:
                    if type(expression[i+1]) != str:
                        expression[i+1].reserved = True
                    i += 1
                elif type(expression[i+1]) == str or expression[i+1].reserved:
                    if type(expression[i-1]) != str:
                        expression[i-1].reserved = True
                    i += 1
                else:
                    expression.pop(i)
                    other = expression.pop(i)
                    expression[i-1] = expression[i-1].math(sign, other)
                    i = 0
            else:
                i += 1
        res = Math.calculate_plus_minus(expression)
        if len(res) == 1:
            res = res[0]
        return res

    @staticmethod
    def calculate_function_with_variable(func, var):
        obj = Data.everything[func]
        res = obj.calculate_with_variable(var, obj.expression[:])
        return res