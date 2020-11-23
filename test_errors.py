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
        ])

    def test_computation(self):
        process_input("a = 2")
        process_input("f(x) = 2 + 4x")
        self.do([
            "a + 2 &",
            "a + 2 !",
            "f(z) = ?",
            "d = 10 % 4i", 
            "d = 10 % 4*i",
            "d = 10i % 3", 
            "d = 10*i % 3",
            "d = 9*i % 3", 
            "10 % 4i", 
            "10 % 4*i",
            "10i % 3", 
            "10*i % 3",
            "9*i % 3", 
            "4 % 0 = ?",
            "4 % 0",
            "4 / 0 = ?",
            "4 / 0",
        ])
    
    def test_syntax(self):
        self.do([
            "s == 4",
            "s = 4x3",
            "s = x4",
            "s = 4x",
            "s = 4+",
            "s = 4-",
            #"s = --4",
            "s = 4*",
            "s = 4/",
            "s = 4%",
            "s = 4^",
            "s = 4?",
            "s = 4,",
            "s = 4;",
            #"s = 4[",
            "s = 4]",
            #"s = [[4,4]",
            #"s = [4,4]]",
            "s = 4(",
            "s = 4)",
            "s = ",
            " = 4",
            "3 = 4",
            "s = y",
            "s = f(x)",
            #"f( = 4",
            "f) = 4",
            "f(x = 4)",
            "f(=)",
        ])

if __name__ == "__main__":
    unittest.main()