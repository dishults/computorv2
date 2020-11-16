#!/usr/bin/env python3

import unittest
from computorv2 import process_input

class Tests(unittest.TestCase):

    def do(self, tests):
        for test, correct in tests:
            res = process_input(test)
            self.assertEqual(str(res), correct)

    def test_rational_numbers(self):
        self.do([
            ["varA = 2",     "2"],
            ["varB = 4.242", "4.242"],
            ["varC = -4.3",  "-4.3"],
        ])

    def test_imaginary_numbers(self):
        self.do([
            ["varA = 2*i + 3", "3 + 2i"],
            ["varB = -4i - 4", "-4 - 4i"],
        ])


    def test_matricies(self):
        self.do([
            ["varA = [[2,3];[4,3]]", "[ 2 , 3 ]\n  [ 4 , 3 ]"],
            ["varB = [[3,4]]",       "[ 3 , 4 ]"],
        ])

    def test_functions(self):
        self.do([
            ["funA(x) = 2*x^5 + 4x^2 - 5*x + 4", "2 * x^5 + 4 * x^2 - 5x + 4"],
            ["funB(y) = 43 * y / (4 % 2 * y)",   "43 * y / (0 * y)"],
            ["funC(z) = -2 * z - 5",             "-2 * z - 5"],
        ])

    def test_reassign_variable(self):
        self.do([
            ["x = 2",        "2"],
            ["y = x",        "2"],
            ["y = 7",        "7"],
            ["y = 2 * i - 4","-4 + 2i"],
        ])

    def test_reassign_the_result(self):
        self.do([
            ["varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)",     "27"],
            ["varB = 2 * varA - 5 %4",                   "53"],
            ["funA(x) = varA + varB * 4 - 1 / 2 + x",    "238.5 + x"],
            ["varC = 2 * varA - varB",                   "1"],
            ["varD = funA(varC)",                        "239.5"],
        ])

    def test_question_mark(self):
        self.do([
            ["a = 2 * 4 + 4",    "12"],
            ["a + 2 = ?",        "14"],
        ])

    def test_image_computation(self):
        self.do([
            ["funA(x) = 2 * 4 + x",              "8 + x"],
            ["funB(x) = 4 -5 + (x + 2)^2 - 4",   "(x + 2) ^ 2 - 5"],
            ["funC(x) = 4x + 5 - 2",             "4 * x + 3"],
            ["funA(2) + funB(4) = ?",            "41"],
            ["funC(3) = ?",                      "15"],
        ])

    def test_polynomials(self):
        self.do([
            ["funA(x) = x^2 + 2x + 1",   "x^2 + 2x + 1"],
            ["y=0",                      "0"],
            ["funA(x) = y ?",            "x^2 + 2x + 1 = 0\n  The R solution is:\n  -1.0"],
        ])


if __name__ == "__main__":
    unittest.main()