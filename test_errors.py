#!/usr/bin/env python3

import unittest
from computorv2 import process_input

class Tests(unittest.TestCase):

    def do(self, tests):
        for test in tests:
            with self.assertRaises(Exception):
                process_input(test)

    def test_variable_name(self):
        self.do([
            "v8 = 2",
            "f(x) = 2 * &",
        ])

if __name__ == "__main__":
    unittest.main()