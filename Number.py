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

    def __init__(self, rest):
        self.reserved = False
        try:
            rational, imaginary = self.process_signs(rest)
        except:
            rational, imaginary = 0, self.strip_i(rest)
        self.rational = self.convert_to_num(rational)
        self.imaginary = self.convert_to_num(imaginary)

    def __truediv__(self, other):
        rational, imaginary = self.get_rational_imaginary(other)
        conjugate = self.return_c_number(rational, -imaginary)
        top = self.__mul__(conjugate)
        bottom = other.__mul__(conjugate).rational
        rational = top.rational / bottom
        imaginary = top.imaginary / bottom
        return self.return_c_number(rational, imaginary)

    def __mod__(self, other):
        raise ArithmeticError

    def __mul__(self, other):
        a, b = self.rational, self.imaginary
        c, d = self.get_rational_imaginary(other)
        rational = a * c - b * d
        imaginary = a * d + b * c
        return self.return_c_number(rational, imaginary)

    def __add__(self, other):
        rational, imaginary = self.get_rational_imaginary(other)
        rational = self.rational + rational
        imaginary = self.imaginary + imaginary
        return self.return_c_number(rational, imaginary)

    def __sub__(self, other):
        rational, imaginary = self.get_rational_imaginary(other)
        rational = self.rational - rational
        imaginary = self.imaginary - imaginary
        return self.return_c_number(rational, imaginary)

    def __pow__(self, other):
        return self.do_math(other, lambda a, b: a ** b)

    def __rtruediv__(self, other):
        if not isinstance(other, Complex):
            rational, imaginary = self.get_rational_imaginary(other)
            other = self.return_c_number(rational, imaginary)
        return Complex.__truediv__(other, self)

    def __rmod__(self, other):
        raise ArithmeticError

    def __rmul__(self, other):
        if not isinstance(other, Complex):
            rational, imaginary = self.get_rational_imaginary(other)
            other = self.return_c_number(rational, imaginary)
        return Complex.__mul__(other, self)

    def __rpow__(self, other):
        return self.do_r_math(other, lambda a, b: a ** b)

    def __radd__(self, other):
        if not isinstance(other, Complex):
            rational, imaginary = self.get_rational_imaginary(other)
            other = self.return_c_number(rational, imaginary)
        return Complex.__add__(other, self)

    def __rsub__(self, other):
        if not isinstance(other, Complex):
            rational, imaginary = self.get_rational_imaginary(other)
            other = self.return_c_number(rational, imaginary)
        return Complex.__sub__(other, self)

    operations = {
        "/" : __truediv__,
        "%" : __mod__,
        "*" : __mul__,
        "^" : __pow__,
        "+" : __add__,
        "-" : __sub__,
    }

    def do_math(self, other, f):
        try:
            rational = f(self.rational, other)
        except:
            rational = self.rational
        imaginary = f(self.imaginary, other)
        return self.return_c_number(rational, imaginary)

    def do_r_math(self, other, f):
        try:
            rational = f(other, self.rational)
        except:
            rational = self.rational
        imaginary = f(other, self.imaginary)
        return self.return_c_number(rational, imaginary)

    def this(self):
        return self.rational

    def __str__(self):
        if self.rational != 0:
            if self.imaginary >= 0:
                sign = "+"
            else:
                sign = "-"
            return f"{self.rational} {sign} {abs(self.imaginary)}i"
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
                rational, imaginary = rest1.split("-")
                rational = "-" + rational
            else:
                rational, imaginary = rest.split("-")
            imaginary = "-" + imaginary
        else:
            rational, imaginary = rest.split("+")
        if "i" in rational:
            rational, imaginary = imaginary, rational
        imaginary = self.strip_i(imaginary)
        return rational, imaginary

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
    def return_c_number(rational, imaginary):
        if imaginary >= 0:
            return Complex(f"{rational}+{imaginary}")
        return Complex(f"{rational}{imaginary}")

    @staticmethod
    def get_rational_imaginary(other):
        if Data.is_number(other):
            rational = other
            imaginary = 0
        elif isinstance(other, Rational):
            rational = other.number
            imaginary = 0
        elif isinstance(other, Complex):
            rational = other.rational
            imaginary = other.imaginary
        return rational, imaginary


def number(number):
    try:
        if isinstance(number, Complex):
            return number
        assert "i" in number
        return Complex(number)
    except:
        return Rational(number)
