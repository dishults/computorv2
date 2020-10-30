from Data import Data

class Numbers(Data):

    def __init__(self, name, number):
        self.name = name
        self.number = self.convert_to_num(number)

    @staticmethod
    def convert_to_num(number):
        if "." in number:
            return float(number)
        else:
            return int(number)


class Rational(Numbers):

    def __str__(self):
        return f"  {self.number}"    


class Complex(Numbers):

    def __init__(self, name, rest):
        sign, rational, imaginary, reverse = self.process_signs(rest)
        super().__init__(name, rational)
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
            return f"  {self.number} {self.sign} {abs(self.imaginary)}i"
        else:
            if self.imaginary == 1:
                return "  i"
            elif self.imaginary == 0:
                return "  0"
            else:
                return f"  {self.imaginary}i"

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