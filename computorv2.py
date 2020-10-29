#!/usr/bin/env python3

import sys
import re

everything = {}

class Numbers:

    def __init__(self, var, number):
        self.var = var
        if "." in number:
            self.number = float(number)
        else:
            self.number = int(number)

class Rational(Numbers):

    def __str__(self):
        return f"  {self.number}"
    
    @staticmethod
    def save_number(var, number):
        obj = Rational(var, number)
        everything[var] = obj
        print(obj)

class Complex(Numbers):

    def __init__(self, var, rational, sign, imaginary, reverse):
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
            return f"  {self.imaginary}i"

    @staticmethod
    def save_number(var, rest):
        for sign in ("+", "-", "/", "*", "%"):
            if sign in rest:
                reverse = False
                # every sign except "*" and plus "*" with imaginary part without "*" like 4i)
                try:
                    if sign == "-":
                        if rest[0] == "-":
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
                        reverse = True
                obj = Complex(var, rational, sign, imaginary, reverse)
                everything[var] = obj
                print(obj)
                break
class Matrices:

    def __init__(self, var, matrix):
        self.var = var
        if ";" not in matrix:
            self.dimentions = 1
            new = matrix.strip("[]").split(",")
            self.matrix = self.get_one_row(new)
        else:
            self.dimentions = 2
            # ['[[2,3]', '[4,3]]']
            matrix = matrix.split(";")
            self.matrix = []
            # [['2', '3'], ['4', '3']]
            for m in matrix:
                new = m.strip("[]").split(",")
                new = self.get_one_row(new)
                self.matrix.append(new)

    def __str__(self):
        m = "  ["
        if self.dimentions == 1:
            for c, cell in enumerate(self.matrix):
                if c > 0:
                    m += ","
                m += f" {cell} "
            m += "]"
        elif self.dimentions == 2:
            for r, row in enumerate(self.matrix):
                if r > 0:
                    m += "\n  ["
                for c, cell in enumerate(row):
                    if c > 0:
                        m += ","
                    m += f" {cell} "
                m += "]"
        return m

    def get_one_row(self, row):
        new_row = []
        for cell in row:
            try:
                obj = Rational(0, cell)
                new_row.append(obj.number)
            except:
                #Complex()
                pass
        return new_row
    
    @staticmethod
    def save_matrix(var, matrix):
        obj = Matrices(var, matrix)
        everything[var] = obj
        print(obj)




def get_type(user_input):
    without_spaces = user_input.replace(" ", "")
    var, rest = without_spaces.split("=")
    try:
        Rational.save_number(var, rest)
    except:
        if "i" in rest:
            Complex.save_number(var, rest)
        elif "[" in rest:
            Matrices.save_matrix(var, rest)
        else:
            print("not a number")

def main():
    while True:
        user_input = input("> ")
        user_input = user_input.lower()
        if user_input == "exit" or user_input == "quit":
            break
        elif "=" in user_input:
            get_type(user_input)
        elif user_input:
            print(everything[user_input])

def test_main():
    get_type(sys.argv[1])

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            test_main()
        else:
            main()
    except (KeyboardInterrupt, EOFError):
        print()