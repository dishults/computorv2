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
            "i = 3",
            "f(i) = 4 * i",
        ])

    def test_computation(self):
        process_input("a = 2")
        process_input("f(x) = 2 + 4x")
        self.do([
            "a + 2 &",
            "a + 2 !",
            "f(z) = ?",
        ])

if __name__ == "__main__":
    unittest.main()