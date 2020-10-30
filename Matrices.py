from Data import Data
from Numbers import Rational, Complex

class Matrices(Data):

    def __init__(self, name, matrix):
        self.name = name
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
                obj = Complex(0, cell)
                new_row.append(obj)
        return new_row
