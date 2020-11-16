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

    def test_polynomials(self):
        tests = {
            "f(x) = x^2 + 2x + 1":"x^2 + 2x + 1",
            "f(x) = 2 ?":         "x^2 + 2x - 1 = 0\n  The two R solutions are:\n  -2.414214\n  0.414214",
            "f(x) = 3x + 2 ?":    "x^2 - x - 1 = 0\n  The two R solutions are:\n  -0.618034\n  1.618034",
            "f(x) = 2x + 2 ?":    "x^2 - 1 = 0\n  The two R solutions are:\n  -1.0\n  1.0",
            "f(x) = x^2 + 1 ?":   "2x = 0\n  The eqution has no solution",
            "f(2) = ?":           "9",
            "f(2) = 2 ?":         "7 = 0\n  The eqution has no solution",
            "f(2) = 9 ?":         "0 = 0\n  Every real number is a solution",
        }#add tests from computorv1
        for test in tests:
            res = process_input(test)
            self.assertEqual(str(res), tests[test])

if __name__ == "__main__":
    unittest.main()