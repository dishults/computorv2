from Data import Data, YELLOW, BLUE, END
from Number import Rational, Complex, Number, number

class Matrix(Data):

    def __init__(self, matrix):
        matrix = Data.remove_colors(matrix)
        self.reserved = False
        self.dimentions = 1
        if type(matrix) != str:
            self.matrix = matrix
            if isinstance(self.matrix[0], Matrix):
                self.dimentions = 2
                self.check_matrix_shape()
            elif type(self.matrix[0]) == list:
                self.dimentions = 2
                for i, m in enumerate(matrix):
                    self.matrix[i] = Matrix(m)
                self.check_matrix_shape()
        elif ";" in matrix:
            self.dimentions = 2
            # ['[[2,3]', '[4,3]]']
            matrix = matrix.split(";")
            self.matrix = []
            # [['2', '3'], ['4', '3']]
            for m in matrix:
                m = m.replace("[[", "[").replace("]]", "]")
                self.matrix.append(Matrix(m))
        else:
            new = matrix.strip("[]").split(",")
            self.matrix = self.get_one_row(new)

    def __str__(self):
        m = f"{BLUE}[{END}"
        if self.dimentions == 1:
            for c, cell in enumerate(self.matrix):
                if c > 0:
                    m += ","
                m += f" {cell} "
            m += f"{BLUE}]{END}"
        elif self.dimentions == 2:
            for r, row in enumerate(self.matrix):
                if r > 0:
                    m += f"\n  {BLUE}[{END}"
                for c, cell in enumerate(row):
                    if c > 0:
                        m += ","
                    m += f" {cell} "
                m += f"{BLUE}]{END}"
        return m

    def alt_str(self):
        if self.dimentions == 2:
            return f"{BLUE}[{END}" + self.__str__().replace("\n  ", f"{YELLOW};{END}") + f"{BLUE}]{END}"
        return self.__str__()

    def check_matrix_shape(self):
        if sum([len(m) for m in self.matrix]) % len(self.matrix) != 0:
            raise TypeError("Each matrix row should be of the same size")

    def get_one_row(self, row):
        new_row = []
        for cell in row:
            try:
                num = number(cell)
                assert isinstance(num, Number)
                new_row.append(num)
            except:
                from Simple import Simple
                try:
                    res = Simple.process(0, cell)
                    new_row.append(res)
                except:
                    raise TypeError(f"Wrong cell '{cell}' in the matrix's row")
        return new_row

    def __getitem__(self, item):
         return self.matrix[item]

    def __iter__(self):
        return iter(self.matrix)

    def __len__(self):
        return len(self.matrix)


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

        try:
            other_t = Matrix.transpose(other)
            # if self >= 1 columns and other >= 1 rows, and self nb columns == other nb rows
            if self.dimentions == 2 and len(self[0]) == len(other_t[0]):
                res = [calculate(one_row, other_t) for one_row in self]
            elif self.dimentions == 1 and len(self) == len(other):
                # if self 1 row and other 1 colomn, and both same length
                if other.dimentions == 2:
                    res = calculate(self, other_t)
                # if self 1 row and other 1 row, and both same length
                else:
                    return Rational(dot(self, other))
            else:
                raise ArithmeticError
        except:
            raise ArithmeticError(
            "Number of Matrix_1 columns should be equal to the number of Matrix_2 rows." \
            + "\nOr both should have one row and same length.")

        if len(res) == 1:
            return Rational(res[0])
        return Matrix(res)

    operations = Data.operations.copy()
    operations.update({
        "@" : __matmul__,
    })

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
        if not isinstance(matrix, Matrix):
            if matrix in Data.everything:
                matrix = Data.everything[matrix]
            else:
                try:
                    matrix = Matrix(matrix)
                except:
                    raise TypeError("Can only transpose a matrix")
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
        return Matrix(T)

    @staticmethod
    def get_matrix_from_expression(expression):
        braket = Data.what_braket(expression, -1, "[", "]") + 1
        matrix = expression[:braket]
        expression = expression[braket:]
        return matrix, expression

    @staticmethod
    def is_expression(expression):
        if expression[0] != "[":
            return True
        rest = Matrix.get_matrix_from_expression(expression)[1]
        if rest:
            return True
        return False

    @staticmethod
    def is_matrix(expression):
        return "[" in expression and not Matrix.is_expression(expression)