ALLOWED = ("+", "-", "/", "%", "^", "*", "@")

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
        if hasattr(obj, "expression") and len(obj.expression) == 1:
            obj = obj.expression[0]
        if name:
            cls.everything[name] = obj
        return obj

    @staticmethod
    def is_number(var):
        try:
            assert var.isdigit()
        except:
            try:
                assert type(float(var)) == float
            except:
                try:
                    assert type(int(var)) == int
                except:
                    return False
        return True

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