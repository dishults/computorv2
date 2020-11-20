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

    def math(self, sign, other):
        return Rational(self.operations[sign](self, other))
    
    def this(self):
        return self.number


class Complex(Number):

    def __init__(self, rest):
        self.reserved = False
        try:
            rational, imaginary = self.process_signs(rest)
        except:
            rational, imaginary = 0, self.strip_i(rest)
        self.rational = Rational(rational)
        self.imaginary = self.convert_to_num(imaginary)

    def math(self, sign, other):
        rational = self.rational.math(sign, other)
        imaginary = self.operations[sign](self, other)
        if imaginary >= 0:
            return Complex(f"{rational}+{imaginary}")
        return Complex(f"{rational}{imaginary}")
    
    def this(self):
        return self.imaginary

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

def number(number):
    try:
        assert "i" in number
        return Complex(number)
    except:
        return Rational(number)
