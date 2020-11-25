from Data import Data

class Number(Data):

    def __init__(self, number):
        self.number = self.convert_to_num(number)
        self.reserved = False

    @staticmethod
    def convert_to_num(number):
        if type(number) in (float, int):
            return number
        elif "." in number:
            return float(number)
        else:
            return int(number)


class Rational(Number):

    def __str__(self):
        return f"{self.number}"

    def __eq__(self, other):
        return self.number == other

    def math(self, sign, other):
        return number(super().math(sign, other))
    
    def this(self):
        return self.number


class Complex(Number):

    def __truediv__(self, other):
        real, imaginary = self.get_real_imaginary(other)
        conjugate = self.get_complex_number(real, -imaginary)
        top = self.__mul__(conjugate)
        bottom = other.__mul__(conjugate).real
        real = top.real / bottom
        imaginary = top.imaginary / bottom
        return self.get_complex_number(real, imaginary)

    def __mod__(self, other):
        raise ArithmeticError

    def __mul__(self, other):
        a, b = self.real, self.imaginary
        c, d = self.get_real_imaginary(other)
        real = a * c - b * d
        imaginary = a * d + b * c
        return self.get_complex_number(real, imaginary)

    def __add__(self, other):
        real, imaginary = self.get_real_imaginary(other)
        real = self.real + real
        imaginary = self.imaginary + imaginary
        return self.get_complex_number(real, imaginary)

    def __sub__(self, other):
        real, imaginary = self.get_real_imaginary(other)
        real = self.real - real
        imaginary = self.imaginary - imaginary
        return self.get_complex_number(real, imaginary)

    def __pow__(self, other):
        if not (isinstance(other, Rational) and type(other.number) == int):
            raise ArithmeticError
        n = other.number
        if n == 0:
            return Rational(1)
        copy = self.get_complex_number(self.real, self.imaginary)
        while n > 1:
            copy = copy.__mul__(self)
            n -= 1
        return self.get_complex_number(copy.real, copy.imaginary)

    def __rtruediv__(self, other):
        if not isinstance(other, Complex):
            real, imaginary = self.get_real_imaginary(other)
            other = self.get_complex_number(real, imaginary)
        return Complex.__truediv__(other, self)

    def __rmod__(self, other):
        raise ArithmeticError

    def __rmul__(self, other):
        if not isinstance(other, Complex):
            real, imaginary = self.get_real_imaginary(other)
            other = self.get_complex_number(real, imaginary)
        return Complex.__mul__(other, self)

    def __rpow__(self, other):
        raise ArithmeticError

    def __radd__(self, other):
        if not isinstance(other, Complex):
            real, imaginary = self.get_real_imaginary(other)
            other = self.get_complex_number(real, imaginary)
        return Complex.__add__(other, self)

    def __rsub__(self, other):
        if not isinstance(other, Complex):
            real, imaginary = self.get_real_imaginary(other)
            other = self.get_complex_number(real, imaginary)
        return Complex.__sub__(other, self)

    operations = {
        "/" : __truediv__,
        "%" : __mod__,
        "*" : __mul__,
        "^" : __pow__,
        "+" : __add__,
        "-" : __sub__,
    }

    def __init__(self, rest):
        self.reserved = False
        try:
            real, imaginary = self.process_signs(rest)
        except:
            real, imaginary = 0, self.strip_i(rest)
        self.real = self.convert_to_num(real)
        self.imaginary = self.convert_to_num(imaginary)

    def __str__(self):
        if self.real != 0:
            if self.imaginary >= 0:
                sign = "+"
            else:
                sign = "-"
            return f"{self.real} {sign} {abs(self.imaginary)}i"
        else:
            if self.imaginary == 1:
                return "i"
            elif self.imaginary == 0:
                return "0"
            else:
                return f"{self.imaginary}i"

    def process_signs(self, rest):
        if "-" in rest[1:]:
            if rest[0] == "-":
                rest1 = rest[1:]
                real, imaginary = rest1.split("-")
                real = "-" + real
            else:
                real, imaginary = rest.split("-")
            imaginary = "-" + imaginary
        else:
            real, imaginary = rest.split("+")
        if "i" in real:
            real, imaginary = imaginary, real
        imaginary = self.strip_i(imaginary)
        return real, imaginary

    @staticmethod
    def strip_i(imaginary):
        if "*" in imaginary:
            imaginary = imaginary.split("*")[0]
        else:
            imaginary = imaginary.split("i")[0]
        return imaginary

    @staticmethod
    def is_expression(expression):
        if expression.count("i") > 1 or any(char in "/%^*(" for char in expression):
            return True
        plus = expression.count("+")
        minus = expression.lstrip("-").count("-")
        if plus == 1 and plus == minus:
            return True
        elif plus > 1 or minus > 1:
            return True
        return False

    @staticmethod
    def get_complex_number(real, imaginary):
        if imaginary >= 0:
            return Complex(f"{real}+{imaginary}")
        return Complex(f"{real}{imaginary}")

    @staticmethod
    def get_real_imaginary(other):
        if Data.is_number(other):
            real = other
            imaginary = 0
        elif isinstance(other, Rational):
            real = other.number
            imaginary = 0
        elif isinstance(other, Complex):
            real = other.real
            imaginary = other.imaginary
        return real, imaginary


def number(number):
    try:
        if isinstance(number, Complex):
            return number
        assert "i" in number
        return Complex(number)
    except:
        return Rational(number)
