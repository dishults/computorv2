class Data:

    everything = {}

    def __lt__(self, other):
        return self.this() < other

    def __gt__(self, other):
        return self.this() > other


    def __truediv__(self, other):
        number = self.this() / other
        if number * 10 % 10 == 0:
            number = int(number)
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
        return self.__add__(other)

    def __pow__(self, other):
        return self.this() ** other


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
    }

    def math(self, sign, other):
        pass

    def this(self):
        pass

    @classmethod
    def save_data(cls, name, rest):
        if type(name) == list:
            name, obj = name[0], cls(name[1], rest)
        else:
            obj = cls(rest)
        cls.everything[name] = obj
        return cls.show(name)
    
    @classmethod
    def show(cls, name):
        return cls.everything[name]
    
    @classmethod
    def reassign(cls, where, what):
        cls.everything[where] = cls.everything[what]
        return cls.show(where)