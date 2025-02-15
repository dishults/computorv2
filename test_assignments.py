#!/usr/bin/env python3

import unittest

from computorv2 import process_input
from Data import Data
remove_colors = Data.remove_colors

class Tests(unittest.TestCase):

    def do(self, tests):
        for test, correct in tests:
            try:
                res = process_input(test)
                res = remove_colors(str(res))
                self.assertEqual(res, correct)
            except:
                self.fail(test)

    def test_variable(self):
        self.do([
            ["v = 42.", "42.0"],
            ["v = ?",   "42.0"],
            ["v",       "42.0"],
            ["s = +4",  "4"],
        ])

    def test_imaginary_numbers(self):
        self.do([
            ["a = 4i + 4",   "4 + 4i"],
            ["a = 4*i + 4",  "4 + 4i"],
            ["a = 4 + 4i",   "4 + 4i"],
            ["a = 4 + 4*i",  "4 + 4i"],
            ["b = 4i - 4",   "-4 + 4i"],
            ["b = 4*i - 4",  "-4 + 4i"],
            ["b = 4 - 4i",   "4 - 4i"],
            ["b = 4 - 4*i",  "4 - 4i"],
            ["c = 3 * 4i",   "12i"],
            ["c = 3 * 4*i",  "12i"],
            ["c = 4i * 3",   "12i"],
            ["c = 4*i * 3",  "12i"],
            ["c = -4*i * 3", "-12i"],
            ["d = 3 / 4i",   "-0.75i"],
            ["d = 3 / 4 * i", "0.75i"],
            ["d = 4i / 3",   "1.3333333333333333i"],
            ["d = 4*i / 3",  "1.3333333333333333i"],
            ["d = 10 % 4 * i", "2i"],
            ["e = -2i",      "-2i"],
            ["e = 2i",       "2i"],
            ["e = ?",        "2i"],
            ["e",            "2i"],
            ["2 4i",         "24i"],
        ])

    def test_matricies(self):
        self.do([
            ["m = [[3+4i, 2-3i]]", "[ 3 + 4i , 2 - 3i ]"],
            ["m = ?",              "[ 3 + 4i , 2 - 3i ]"],
            ["m"    ,              "[ 3 + 4i , 2 - 3i ]"],
        ])

    def test_functions(self):
        self.do([
            ["f(x) = 0 + x",                         "x"],
            ["f(x) = 0 - x",                         "-x"],
            ["f(x) = x + 0",                         "x"],
            ["f(x) = x - 0",                         "x"],
            ["f(z) = -z * 2 + 1",                    "-z * 2 + 1"],
            ["f(x) = 2 * x - 5",                     "2 * x - 5"],
            ["f(x) = 4x^2 - 5*x^1 + 4x^0",           "4 * x^2 - 5x + 4"],
            ["f(x) = -4x^2 - 5*x^1 + 4x^0",          "-4 * x^2 - 5x + 4"],
            ["f(x) = 2*x^5 + 4x^2 - 2x^5 - 5*x + 4", "4 * x^2 - 5x + 4"],
            ["f(x) = 4x + 1",                        "4 * x + 1"],
            ["f(x) = (x + 2) / 2",                   "(x + 2) / 2"],
            ["f(x) = ?",                             "(x + 2) / 2"],
            ["f(x)",                                 "(x + 2) / 2"],
            ["f(x) = x * x",                         "x * x"],
            ["b(x) = 2 * x + 3",                     "2 * x + 3"],
            ["c(x) = f + b",                         "(x * x) + (2 * x + 3)"],
            ["c(2)",                                 "11"],
            ["c(x) = f + b",                         "(x * x) + (2 * x + 3)"],
            ["c(2)",                                 "11"],
            ["f(x) = x^2 + 2x + 1",                  "x^2 + 2x + 1"],
            ["b(x) = x^2 + 2x + 1",                  "x^2 + 2x + 1"],
            ["c(x) = f + b",                         "(x ^ 2 + 2 * x + 1) + (x ^ 2 + 2 * x + 1)"],
            ["f(x) = x^2 + 3x",                      "x^2 + 3x"],
            ["f(x) = x^2 + 1",                       "x^2 + 1"],
            ["f(x) = x^2",                           "x^2"],
            ["f(x) = x",                             "x"],
            ["f(2)",                                 "2"],
            ["f(x) = 3 + x - 2",                     "x + 1"],
            ["f(x) = 3 + x - 3i",                    "x + (3 - 3i)"],
            ["f(x) = -3i + x + 3",                   "x + (3 - 3i)"],
            ["f(x) = 3 + x - (4 + 3i)",              "x + (-1 - 3i)"],
            ["f(x) = -(4 + 3i) + x + 3",             "x + (-1 - 3i)"],
            ["f(x) = 3 + x - [4,5]",                 "x + [ -1 , -2 ]"],
            ["f(x) = -[4,5] + x + 3",                "x + [ -1 , -2 ]"],
        ])


if __name__ == "__main__":
    unittest.main()