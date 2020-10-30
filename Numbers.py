class Numbers:

    def __init__(self, var, number):
        self.var = var
        if "." in number:
            self.number = float(number)
        else:
            self.number = int(number)

    @classmethod
    def save_number(cls, var, rest, everything):
        obj = cls(var, rest)
        everything[var] = obj
        print(obj)

class Rational(Numbers):

    def __str__(self):
        return f"  {self.number}"    

class Complex(Numbers):

    def __init__(self, var, rest):
        for sign in ("+", "-", "/", "%", "*"):
            if sign in rest:
                reverse = False
                # every sign except "*" and plus "*" with imaginary part without "*" like 4i)
                try:
                    if sign == "-":
                        if rest[0] == "-":
                            if "-" not in rest[1:]:
                                continue
                            rational, imaginary = rest[1:].split(sign)
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
                    if imaginary == "*":
                        imaginary, i = i, imaginary
                        #reverse = True
                    elif imaginary == "i":
                        imaginary = rational
                        rational = i
                break
        super().__init__(var, rational)
        self.sign = sign
        if "." in imaginary:
            self.imaginary = float(imaginary)
        else:
            self.imaginary = int(imaginary)
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
