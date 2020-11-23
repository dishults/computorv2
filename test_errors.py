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
        ])

if __name__ == "__main__":
    unittest.main()