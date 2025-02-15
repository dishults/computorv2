ALLOWED = ("+", "-", "/", "%", "^", "*", "@")

GREEN="\033[32m"
CYAN="\033[36m"
BLUE="\033[34m"
YELLOW="\033[33m"
MAGENTA="\033[35m"
END="\033[0m"

class Data:

    everything = {}

    def abstract(self):
        self.expression = []
        self.operations = {}

    def __pow__(self, other):
        return self.do_math(other, lambda a, b: a ** b)

    def __truediv__(self, other):
        return self.do_math(other, lambda a, b: a / b)

    def __mod__(self, other):
        return self.do_math(other, lambda a, b: a % b)

    def __mul__(self, other):
        return self.do_math(other, lambda a, b: a * b)

    def __add__(self, other):
        return self.do_math(other, lambda a, b: a + b)

    def __sub__(self, other):
        return self.do_math(other, lambda a, b: a - b)

    def __matmul__(self, other):
        """Dot product"""
        raise ArithmeticError("Can only do dot product between two matricies")


    def __rpow__(self, other):
        return self.do_math(other, lambda a, b: b ** a)

    def __rtruediv__(self, other):
        return self.do_math(other, lambda a, b: b / a)

    def __rmod__(self, other):
        return self.do_math(other, lambda a, b: b % a)

    def __rmul__(self, other):
        return self.do_math(other, lambda a, b: b * a)

    def __radd__(self, other):
        return self.do_math(other, lambda a, b: b + a)

    def __rsub__(self, other):
        return self.do_math(other, lambda a, b: b - a)

    def __neg__(self):
        return self.__mul__(-1)

    operations = {
        "^" : __pow__,
        "/" : __truediv__,
        "%" : __mod__,
        "*" : __mul__,
        "+" : __add__,
        "-" : __sub__,
        "@" : __matmul__,
    }

    def math(self, sign, other):
        return self.operations[sign](self, other)

    def do_math(self, other, f):
        pass

    @classmethod
    def show_everything(cls):
        res = "  "
        for var in sorted(cls.everything):
            res = f"{res}{var} : {cls.everything[var]}\n  "
        return res.rstrip("\n  ")

    @classmethod
    def process_data(cls, name, rest):
        if name:
            cls.everything[name] = cls.everything[rest]
        return cls.everything[rest]

    @classmethod
    def process(cls, name, *args):
        obj = cls(*args)
        if hasattr(obj, "expression") and len(obj.expression) == 1 \
                and type(obj.expression[0]) != str:
            obj = obj.expression[0]
        if name:
            cls.everything[name] = obj
        return obj

    @staticmethod
    def is_number(var):
        try:
            float(var)
            return True
        except:
            return False

    @staticmethod
    def what_braket(expression, braket=0, opening="(", closing=")"):
        braket = braket
        for i, char in enumerate(expression):
            if char == opening:
                braket += 1
            elif char == closing:
                if not braket:
                    break
                else:
                    braket -= 1
        return i

    @staticmethod
    def remove_colors(string):
        try:
            for color in GREEN, CYAN, BLUE, YELLOW, MAGENTA, END:
                string = string.replace(color, "")
        # if string is int or float
        except:
            pass
        return string