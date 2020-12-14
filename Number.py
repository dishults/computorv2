from Data import Data, GREEN, CYAN, END

class Number(Data):

    def __init__(self, number):
        number = Data.remove_colors(number)
        self.number = self.convert_to_num(number)
        self.reserved = False

    @staticmethod
    def convert_to_num(number):
        if type(number) in (float, int):
            return number
        elif type(number) == str and "." in number:
            return float(number)
        else:
            return int(number)


class Rational(Number):

    def __str__(self):
        return f"{GREEN}{self.number}{END}"

    def __abs__(self):
        return abs(self.number)

    def __int__(self):
        return int(self.number)

    def __float__(self):
        return float(self.number)

    def __eq__(self, other):
        return self.number == other

    def __lt__(self, other):
        return self.number < other

    def __le__(self, other):
        return self.number <= other

    def __ne__(self, other):
        return self.number != other

    def __gt__(self, other):
        return self.number > other

    def __ge__(self, other):
        return self.number >= other

    def __neg__(self):
        return self.math("*", -1)


    def __truediv__(self, other):
        number = self.number / other
        try:
            if number * 10 % 10 == 0:
                return Rational(int(number))
        except:
            pass
        return number

    def __mod__(self, other):
        if self.number < 0:
            return abs(self.number) % other * -1
        return self.number % other

    operations = Data.operations.copy()
    operations.update({
        "/" : __truediv__,
        "%" : __mod__,
    })

    def math(self, sign, other):
        res = self.operations[sign](self, other)
        return number(res)
    
    def do_math(self, other, f):
        res = f(self.number, other)
        return number(res)


class Complex(Number):

    def __pow__(self, other):
        if not (isinstance(other, Rational) and type(other.number) == int \
                and other.number >= 0):
            raise ArithmeticError("The power should be a scalar, bigger or equal to 0")
        n = other.number
        if n == 0:
            return Rational(1)
        copy = self.get_complex_number(self.real, self.imaginary)
        while n > 1:
            copy = copy.__mul__(self)
            n -= 1
        return self.get_complex_number(copy.real, copy.imaginary)

    def __truediv__(self, other):
        real, imaginary = self.get_real_imaginary(other)
        conjugate = self.get_complex_number(real, -imaginary)
        top = self.__mul__(conjugate)
        bottom = other.__mul__(conjugate).real
        real = top.real / bottom
        imaginary = top.imaginary / bottom
        return self.get_complex_number(real, imaginary)

    def __mod__(self, other):
        raise ArithmeticError("Can't mod complex numbers")

    def __mul__(self, other):
        a, b = self.real, self.imaginary
        c, d = self.get_real_imaginary(other)
        real = a * c - b * d
        imaginary = a * d + b * c
        return self.get_complex_number(real, imaginary)


    def __rpow__(self, other):
        raise ArithmeticError("Can't raise to a complex power, try scalar instead")

    def __rtruediv__(self, other):
        if not isinstance(other, Complex):
            real, imaginary = self.get_real_imaginary(other)
            other = self.get_complex_number(real, imaginary)
        return other.__truediv__(self)

    def __rmod__(self, other):
        return self.__mod__(other)

    def __rmul__(self, other):
        if not isinstance(other, Complex):
            real, imaginary = self.get_real_imaginary(other)
            other = self.get_complex_number(real, imaginary)
        return other.__mul__(self)

    operations = Data.operations.copy()
    operations.update({
        "^" : __pow__,
        "/" : __truediv__,
        "%" : __mod__,
        "*" : __mul__,
    })

    def do_math(self, other, f):
        """Only for direct and reverse +-"""
        self_real, self_imaginary = self.get_real_imaginary(self)
        other_real, other_imaginary = self.get_real_imaginary(other)
        real = f(self_real, other_real)
        imaginary = f(self_imaginary, other_imaginary)
        return self.get_complex_number(real, imaginary)

    def __init__(self, expression):
        expression = Data.remove_colors(expression)
        expression = expression.replace("*i", "i")
        self.reserved = False
        try:
            real, imaginary = self.process_signs(expression)
        except:
            real, imaginary = 0, self.strip_i(expression)
        self.real = self.convert_to_num(real)
        try:
            self.imaginary = self.convert_to_num(imaginary)
        except:
            self.imaginary = 1

    def __str__(self):
        if self.real:
            if not self.imaginary:
                c = f"{self.real}"
            else:
                if self.imaginary > 0:
                    sign = "+"
                else:
                    sign = "-"
                c = f"{self.real} {sign} {abs(self.imaginary)}i"
        else:
            if not self.imaginary:
                c = "0"
            elif self.imaginary == 1:
                c = "i"
            elif self.imaginary == -1:
                c = "-i"
            else:
                c = f"{self.imaginary}i"
        return f"{CYAN}{c}{END}"

    def process_signs(self, expression):
        if "-" in expression[1:]:
            if expression[0] == "-":
                expression = expression[1:]
                real, imaginary = expression.split("-")
                real = "-" + real
            else:
                real, imaginary = expression.split("-")
            imaginary = "-" + imaginary
        else:
            real, imaginary = expression.split("+")
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
        else:
            raise TypeError(f"Expected R/C number, got '{other}'")
        return real, imaginary


def number(number):
    try:
        if isinstance(number, Number):
            return number
        if type(number) == str and "i" in number:
            return Complex(number)
        else:
            return Rational(number)
    except:
        return number
