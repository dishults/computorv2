ALLOWED = ("+", "-", "/", "%", "^", "*", "@")

class Data:

    everything = {}

    def abstract(self):
        self.expression = []

    def __lt__(self, other):
        return self.this() < other

    def __ne__(self, other):
        return self.this() != other

    def __gt__(self, other):
        return self.this() > other


    def __truediv__(self, other):
        number = self.this() / other
        try:
            if number * 10 % 10 == 0:
                number = int(number)
        except:
            pass
        return number

    def __mod__(self, other):
        if self.this() < 0:
            return abs(self.this()) % other * -1
        return self.this() % other

    def __mul__(self, other):
        return self.this() * other

    def __add__(self, other):
        return self.this() + other

    def __sub__(self, other):
        return self.this() - other

    def __pow__(self, other):
        return self.this() ** other

    def __matmul__(self, other):
        """Dot product"""
        raise ArithmeticError("Can only do dot product between two matricies")


    def __rtruediv__(self, other):
        return other / self.this()

    def __rmod__(self, other):
        return other % self.this()

    def __rmul__(self, other):
        return other * self.this()

    def __radd__(self, other):
        return other + self.this()

    def __rsub__(self, other):
        return other - self.this()

    def __rpow__(self, other):
        return other ** self.this()


    def __neg__(self):
        return self.math("*", -1)

    operations = {
        "/" : __truediv__,
        "%" : __mod__,
        "*" : __mul__,
        "^" : __pow__,
        "+" : __add__,
        "-" : __sub__,
        "@" : __matmul__,
    }

    def math(self, sign, other):
        return self.operations[sign](self, other)

    def this(self):
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