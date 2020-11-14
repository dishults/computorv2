#!/usr/bin/env python3

import unittest
from computorv2 import process_input

class Tests(unittest.TestCase):

    def test_variable(self):
        tests = {
            "a = 1 + 2":                "3",
            "a = 5 - 2":                "3",
            "a = 4 / 2":                "2",
            "a = 5 % 2":                "1",
            "a = 4 * 2":                "8",
            "a = 3 / 2 + 3":            "4.5",
            "a = 2 * (4 + 5)":          "18",
            "a = 2 * (4 + 5) / 9":      "2",
            "a = (4 + 5) / 2 + 1":      "5.5",
            "a = (4 + 5) / (2 + 1) + 1":"4",
            "a = 1 + (2 + (3 * 5))":    "18",
            "a = ((3 * 5) + 2) + 1":    "18",
            "a = (2 + (3 * 5)) + 1":    "18",
        }
        for test in tests:
            res = process_input(test)
            self.assertEqual(str(res), tests[test])

    def test_image_computation(self):
        tests = {
            "varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)":         "27",
            "funA(x) = 2 * 4 + x":                          "8 + x",
            "v = (1 + 2)^2":                                "9",
            "funB(x) = 4 -5 + (x + 2)^2 - 4":               "(x + 2) ^ 2 - 5",
            "funB(x) = 4 -5 + (x + 2)^2 - 4 + (x * 2) + 7": "(x + 2) ^ 2 + (x * 2) + 2",
        }
        for test in tests:
            res = process_input(test)
            self.assertEqual(str(res), tests[test])
"""
    def test_polynomials(self):
        tests = {
            "":   "",
        }
        for test in tests:
            res = process_input(test)
            self.assertEqual(str(res), tests[test])
"""
if __name__ == "__main__":
    unittest.main()