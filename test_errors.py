#!/usr/bin/env python3

import unittest

from computorv2 import process_input

class Tests(unittest.TestCase):

    def do(self, tests):
        for test in tests:
            try:
                with self.assertRaises(Exception):
                    process_input(test)
            except:
                self.fail(test)

    def test_variable_name(self):
        self.do([
            "v8 = 2",
            "f(x) = 2 * &",
            "f(x) = 2 * z + x - z",
            "i = 3",
            "f(i) = 4 * i",
            "f(x) = 3*x^-1",
            "a = 1 + 4(2+3)",
            "1 + 4(2+3)",
        ])

    def test_computation(self):
        process_input("a = 2")
        process_input("f(x) = 2 + 4x")
        self.do([
            "a + 2 &", "a + 2 !",
            "f(z) = ?",
            "d = 10 % 4i", "d = 10i % 3", "d = 10*i % 3", "d = 9*i % 3", 
            "10 % 4i", "10i % 3", "10*i % 3", "9*i % 3", 
            "4 % 0 = ?", "4 % 0", "4 / 0 = ?", "4 / 0",
            "2 ^ (2 + 3i)", "(2 + 3i) ^ (2 + 3i)",
            "(2 + 3i) ^ 3.1", "(2 + 3i) ^ -1",
            "plot", "plot()", "plot(a)", "plot(b)", "plot(2)", "plot + 2",
            "2 + plot", "plot(f) + 2", "2 + plot(f)",
            "(2+3i) - [1,2]",
        ])

    def test_matricies(self):
        process_input("a = [1,2]")
        self.do([
            "a + 2 = 2 ?",
            "[3,4] ** [1,2,3]",
            "[3,4] * [1,2,3]",
            "[3,4,5] ** [1,2]",
            "[3,4,5] * [1,2]",
            "[1,2] ** [[1];[2];[3]]",
            "[[1,2];[3,4]] ** [[1];[2];[3]]",
            "[[1,2];[3,4]] ** [1,2]",
            "[[1],[2]] ** [[1];[2]]",
            "2 ** [3,4]",
            "[3,4] ** 2",
            "f(x) = [x, 2] + 2",
            "m = [x,2]",
            "[x,2]",
        ])
    
    def test_syntax(self):
        self.do([
            "s == 4",
            "s = 4x3", "s = x4", "s = 4x",
            "s = 4-", "4+", "4*", "4/", "4%", "4^",
            "*4", "/4", "%4", "^4", "+4-"
            "s = 4--2", "2++3", "3+-4", "4+-5", "4*^5", "4%/5",
            "y = 4?", "s = 4,", "s = 4;",
            "s = ?4", "s = ,4", "s = ;4",
            "s = 4[", "s = 4[]", "s = 4]", "[;]", "[1;]", "[;1]",
            "s = [[4,4]",
            "s = [4,4]]",
            "s = 4(", "s = 4)", "s = 4()", "(.)",
            "s = (4", "s = )4", "s = ()4",
            "s = ",
            " = 4",
            "3 = 4",
            "s = y",
            "s = f(x)",
            "f( = 4", "f) = 4", "f(x = 4)", "f(=)",
            "m = [[[1,2];[2,1]];[[1,2];[2,1]]]",  "[[1,2];[2,1]];[[1,2];[2,1]]",
            "[1,2] + 2 = 2 ?",
        ])
        process_input("f(x) = x * x")
        process_input("b(x) = 2 * x + 3")
        self.do([
            "c = f + b",
            "c = f(x) + b(x)",
            "c(x) = f(x) + b(x)",
            "f + b",
            "f(x) + b(x)",
            ])
        process_input("f(x) = x^2 + 2x + 1")
        process_input("b(x) = x^2 + 2x + 1")
        self.do([
            "c = f + b",
            "c = f(x) + b(x)",
            "c(x) = f(x) + b(x)",
            "f + b",
            "f(x) + b(x)",
            ])

if __name__ == "__main__":
    unittest.main()