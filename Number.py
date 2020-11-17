from abc import abstractmethod

from Data import Data

class Number(Data):

    def __init__(self, number):
        self.number = self.convert_to_num(number)
        self.reserved = False

    def __truediv__(self, other):
        number = self.number / other
        if number * 10 % 10 == 0:
            number = int(number)
        return number

    def __lt__(self, other):
        return self.number < other

    def __gt__(self, other):
        return self.number > other


    def __mod__(self, other):
        if self.number < 0:
            return abs(self.number) % other * -1
        return self.number % other

    def __mul__(self, other):        
        return self.number * other

    def __add__(self, other):        
        return self.number + other
    
    def __sub__(self, other):     
        return self.__add__(other)

    def __pow__(self, other):        
        return self.number ** other


    def __rtruediv__(self, other):
        return other / self.number

    def __rmod__(self, other):
        return other % self.number

    def __rmul__(self, other):
        return other * self.number

    def __radd__(self, other):
        return other + self.number

    def __rsub__(self, other):
        return other - self.number

    def __rpow__(self, other):
        return other ** self.number


    operations = {
        "/" : __truediv__,
        "%" : __mod__,
        "*" : __mul__,
        "^" : __pow__,
        "+" : __add__,
        "-" : __sub__,
    }

    @abstractmethod
    def math(self, sign, other):
        pass

    def __neg__(self):
        return self.math("*", -1)

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

    def math(self, sign, other):
        return Rational(self.operations[sign](self, other))


class Complex(Number):

    def __init__(self, rest):
        sign, rational, imaginary, reverse = self.process_signs(rest)
        super().__init__(rational)
        self.sign = sign
        self.imaginary = self.convert_to_num(imaginary)
        if sign == "-" and self.imaginary > 0:
            self.sign = "+"
        if sign in ("/", "*", "%"):
            a, b = self.number, self.imaginary
            if reverse:
                a, b = b, a
            if sign == "/":
                self.imaginary = a / b
            elif sign == "*":
                self.imaginary = a * b
            elif sign == "%":
                self.imaginary = a % b
            self.number = 0

    def __str__(self):
        if self.number:
            return f"{self.number} {self.sign} {abs(self.imaginary)}i"
        else:
            if self.imaginary == 1:
                return "i"
            elif self.imaginary == 0:
                return "0"
            else:
                return f"{self.imaginary}i"

    def process_signs(self, rest):
        for sign in ("+", "-", "/", "%", "*"):
            if sign in rest:
                reverse = False
                # every sign except "*" and plus "*" with imaginary part without "*" like 4i)
                try:
                    if sign == "-":
                        if rest[0] == "-":
                            rest1 = rest[1:]
                            if "-" not in rest1:
                                continue
                            rational, imaginary = rest1.split(sign)
                            rational = "-" + rational
                        else:
                            rational, imaginary = rest.split(sign)
                        imaginary = "-" + imaginary
                    else:
                        rational, imaginary = rest.split(sign)
                    if "i" in rational:
                        rational, imaginary = imaginary, rational
                        reverse = True
                    if "*" in imaginary:
                        imaginary = imaginary.split("*")[0]
                    else:
                        imaginary = imaginary.split("i")[0]
                # "*" sign and imaginary part with "*" like 4*i
                except:
                    rational, imaginary, i = rest.split(sign)
                    if imaginary == "i":
                        imaginary, rational = rational, i
                return sign, rational, imaginary, reverse

def number(number):
    try:
        assert "i" in number
        return Complex(number)
    except:
        return Rational(number)

def save_number(name, number):
    try:
        assert "i" in number
        return Complex.save_data(name, number)
    except:
        return Rational.save_data(name, number)