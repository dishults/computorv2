#!/usr/bin/env python3

import unittest
from computorv2 import process_input

class Tests(unittest.TestCase):

    def do(self, tests):
        for test, correct in tests:
            try:
                res = process_input(test)
                self.assertEqual(str(res), correct)
            except:
                self.fail(test)

    def test_variable(self):
        self.do([
            ["v = 42.", "42.0"],
            ["v = ?",   "42.0"],
            ["v",       "42.0"],
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
            ["d = 3 / 4*i",  "-0.75i"],
            ["d = 4i / 3",   "1.3333333333333333i"],
            ["d = 4*i / 3",  "1.3333333333333333i"],
            ["e = -2i",      "-2i"],
            ["e = 2i",       "2i"],
            ["e = ?",        "2i"],
            ["e",            "2i"],
        ])

    def test_matricies(self):
        self.do([
            ["m = [[[1,2];[2,1]];[[1,2];[2,1]]]",
                "[ 1 , 2 ]\n  [ 2 , 1 ]\n  [ 1 , 2 ]\n  [ 2 , 1 ]"],
            ["m = [[3+4i, 2-3i]]", "[ 3 + 4i , 2 - 3i ]"],
            ["m = ?",              "[ 3 + 4i , 2 - 3i ]"],
            ["m"    ,              "[ 3 + 4i , 2 - 3i ]"],
        ])

    def test_functions(self):
        self.do([
            ["f(z) = -z * 2 + 1",                    "-z * 2 + 1"],
            ["f(x) = 2 * x - 5",                     "2 * x - 5"],
            ["f(x) = 4x^2 - 5*x^1 + 4x^0",           "4 * x^2 - 5x + 4"],
            ["f(x) = -4x^2 - 5*x^1 + 4x^0",          "-4 * x^2 - 5x + 4"],
            ["f(x) = 2*x^5 + 4x^2 - 2x^5 - 5*x + 4", "4 * x^2 - 5x + 4"],
            ["f(x) = 4x + 1",                        "4 * x + 1"],
            ["f(x) = (x + 2) / 2",                   "(x + 2) / 2"],
            ["f(x) = ?",                             "(x + 2) / 2"],
            ["f(x)",                                 "(x + 2) / 2"],
        ])


if __name__ == "__main__":
    unittest.main()