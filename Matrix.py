from Data import Data
from Number import Rational, Complex, number

class Matrix(Data):

    def __init__(self, matrix):
        self.reserved = False
        self.dimentions = 1
        if type(matrix) != str:
            self.matrix = matrix
            for m in matrix:
                if type(m) == list:
                    self.dimentions = 2
                    break
        elif ";" in matrix:
            self.dimentions = 2
            # ['[[2,3]', '[4,3]]']
            matrix = matrix.split(";")
            self.matrix = []
            # [['2', '3'], ['4', '3']]
            for m in matrix:
                new = m.strip("[]").split(",")
                new = self.get_one_row(new)
                self.matrix.append(new)
        else:
            new = matrix.strip("[]").split(",")
            self.matrix = self.get_one_row(new)

    def __str__(self):
        m = "["
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
            new_row.append(number(cell))
        return new_row

    def __getitem__(self, item):
         return self.matrix[item]

    def __iter__(self):
        return iter(self.matrix)

    def __len__(self):
        return len(self.matrix)


    def __add__(self, other):
        return self.do_math(other, lambda a, b: a + b)

    def __sub__(self, other):
        return self.do_math(other, lambda a, b: a - b)

    def __mul__(self, other):
        return self.do_math(other, lambda a, b: a * b)

    def __truediv__(self, other):
        return self.do_math(other, lambda a, b: a / b)

    def __mod__(self, other):
        return self.do_math(other, lambda a, b: a % b)

    def __pow__(self, other):
        return self.do_math(other, lambda a, b: a ** b)

    def __matmul__(self, other):
        """Matrix-Matrix Multiplication (dot product).
        The number of columns in the first matrix must be equal to 
        the number of rows in the second matrix (self columns == other rows)
        
        For example, to calculate first cell in row 1 column 1:
            sum of [A row 1] * [B column 1]
        
        Keyword arguments:
        self - Matrix (1 or 2 dimensional)
        other - Matrix (1 or 2 dimensional)
        """

        def dot(x, y):
            return sum([x[i] * y[i] for i in range(len(y))])

        def calculate(x, Y):
            return [dot(x, y) for y in Y]

        if not isinstance(other, Matrix):
            return super().__matmul__(other)

        other_t = Matrix.transpose(other.matrix)
        if self.dimentions == 2 and len(self[0]) == len(other_t[0]):
            res = [calculate(one_row, other_t) for one_row in self]
        elif len(self) == len(other):
            if other.dimentions == 2:
                res = calculate(self, other_t)
            else:
                return Rational(dot(self, other))
        else:
            raise ArithmeticError(
            "Number of Matrix_1 columns should be equal to the number of Matrix_2 rows." \
            + "\nOr both should have one row and same length.")

        if len(res) == 1:
            return Rational(res[0])
        return Matrix(res)


    def __radd__(self, other):
        return self.do_math(other, lambda a, b: b + a)

    def __rsub__(self, other):
        return self.do_math(other, lambda a, b: b - a)

    def __rmul__(self, other):
        return self.do_math(other, lambda a, b: b * a)

    def __rtruediv__(self, other):
        return self.do_math(other, lambda a, b: b / a)

    def __rmod__(self, other):
        return self.do_math(other, lambda a, b: b % a)

    def __rpow__(self, other):
        return self.do_math(other, lambda a, b: b ** a)


    def __isub__(self, other):
        """self -= other"""
        return self.__sub__(other)
    
    def __neg__(self):
        """-self"""
        return self.__mul__(-1)

    operations = {
        "/" : __truediv__,
        "%" : __mod__,
        "*" : __mul__,
        "^" : __pow__,
        "+" : __add__,
        "-" : __sub__,
        "@" : __matmul__,
    }

    def do_math(self, other, f):
        """Peform math operation [f] (+ - * / ^) on [self] and [other].

        Keyword arguments:
        other -- Matrix (2D or 1D) or scalar
        f -- function with operation (+ - * / ^) to perform
        """

        def calc_diff_dimentions(two_d, one_d):
            for row in two_d:
                res.append([f(item, one_d) for item in row])

        res = []
        # Both are Matricies of same dimentions (2D or 1D)
        if isinstance(other, Matrix) and self.dimentions == other.dimentions:
            if len(self) != len(other):
                raise ArithmeticError(
                "Matricies should be of the same length to do that operation")
            # Both 2D (multiple columns) or 1D (one row)
            try:
                for i in range(len(other)):
                    res.append(f(self[i], other[i]))
            # Both 2D with just one column
            except:
                for i in range(len(other)):
                    row = f(self[i][0], other[i][0])
                    res.append([Rational(row)])
        else:
            # self 2D and other 1D or scalar
            try:
                if self.dimentions == 2:
                    calc_diff_dimentions(self, other)
                # self 1D and other 2D
                else:
                    calc_diff_dimentions(other, self)
            except:
                # self 1D and other scalar
                for item in self:
                    res.append(f(item, other))
    
        if type(res[0]) == list and len(res[0]) == 1 and isinstance(res[0][0], Matrix):
            for i in range(len(res)):
                res[i] = res[i][0].matrix
        return Matrix(res)

    @staticmethod
    def transpose(matrix):
        T = []
        try:
            for j in range(len(matrix[0])):
                new = []
                for i in range(len(matrix)):
                    new.append(matrix[i][j])
                T.append(new)
        # if only one row
        except:
            for i in range(len(matrix)):
                T.append([matrix[i]])
        return T

    @staticmethod
    def is_expression(expression):
        if expression[0] != "[":
            return True
        rest = Matrix.get_matrix_from_expression(expression)[1]
        if rest:
            return True
        return False

    @staticmethod
    def get_matrix_from_expression(expression):
        braket = Data.what_braket(expression, -1, "[", "]") + 1
        matrix = expression[:braket]
        expression = expression[braket:]
        return matrix, expression
