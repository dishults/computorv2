#!/usr/bin/env python3

import unittest
from computorv2 import process_input, Data

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
            ["a = 1 + 2",                "3"],
            ["1 + 2 = ?",                "3"],
            ["1 + 2",                    "3"],
            ["a = 7 - 2",                "5"],
            ["7 - 2 = ?",                "5"],
            ["7 - 2",                    "5"],
            ["a = 4 / 2",                "2"],
            ["4 / 2 = ?",                "2"],
            ["4 / 2",                    "2"],
            ["a = 5 % 2",                "1"],
            ["5 % 2 = ?",                "1"],
            ["5 % 2",                    "1"],
            ["a = 4 * 2",                "8"],
            ["4 * 2 = ?",                "8"],
            ["4 * 2",                    "8"],
            ["a = 3^2-2",                "7"],
            ["3^2-2 = ?",                "7"],
            ["3^2-2",                    "7"],
            ["a = 3 / 2 + 3",            "4.5"],
            ["a = 2 * (4 + 5)",          "18"],
            ["a = 2 * (4 + 5) / 9",      "2"],
            ["a = (4 + 5) / 2 + 1",      "5.5"],
            ["a = (4 + 5) / (2 + 1) + 1","4"],
            ["a = 1 + (2 + (3 * 5))",    "18"],
            ["a = ((3 * 5) + 2) + 1",    "18"],
            ["a = (2 + (3 * 5)) + 1",    "18"],
        ])

    def test_computation(self):
        self.do([
            ["a = 2",                         "2"],
            ["a + 2 = ?",                     "4"],
            ["a + 2 ?",                       "4"],
            ["a + 2",                         "4"],
            ["a * 0",                         "0"],
            ["fa(x) = 2 + x",                 "2 + x"],
            ["fb(x) = 3 + x",                 "3 + x"],
            ["v = 3",                         "3"],
            ["fa(2) + v + fb(4) + 2 = ?",     "16"],
            ["fa(2 * 3) = ?",                 "8"],
            ["fa(2 * 2) + fa(3 * 3) = ?",     "17"],
            ["f(x) = 1.2x",                   "1.2 * x"],
            ["f(1.2 * 4) = ?",                "5.76"],
            ["x = 4",                         "4"],
            ["f(x) = ?",                      "4.8"],
            ["f(x)",                          "4.8"],
            ["4 ^ 3.1",                       "73.51669471981025"],
            ["4 ^ -2",                        "0.0625"],
            ["4 * -2",                        "-8"],
            ["4 / -2",                        "-2"],
            ["5 % -2",                        "-1"],
            ["5%-2 + 3*-1 - 4/-2 + 2^-2",     "-1.75"],
            ["(-15) ^ 2",                     "225"],
            ["-15 ^ 2",                       "-225"],
        ])
        del Data.everything["x"]

    def test_calculation_priority(self):
        self.do([
            ["3 * 5 ^ 2",                       "75"],
            ["2 - 3 * 5 ^ 2",                   "-73"],
            ["2 + 3 * 5 ^ 2 + 4 * 2 ^ 3 - 1",   "108"],
            ["2 - (3 * 5) ^ 2",                 "-223"],
            ["7 + 0 - 4 - 0 * 8",               "3"],
        ])

    def test_imaginary_numbers(self):
        process_input("f(x) = 4x")
        process_input("c = 3 + 4i")
        self.do([
            ["2 - c", "-1 - 4i"],
            ["f(2 + 4i) = ?", "8 + 16i"],
            ["2i + 3", "3 + 2i"],
            ["2i+3 + 4i+4", "7 + 6i"],
            ["c = 2i+3 + 4i+4", "7 + 6i"],
            ["2 + 4i * 2", "2 + 8i"],
            ["4i - 4i + 2", "2"],
            ["2 - (3 + 4i)", "-1 - 4i"],
            ["f(x) = x * (2 + 4i)", "x * (2 + 4i)"],
            ["f(2) = ?", "4 + 8i"],
            ["(3 + 2i)*(1 + 7i)", "-11 + 23i"],
            ["(2+3i)/(4 - 5i)", "-0.17073170731707318 + 0.5365853658536586i"],
            ["2 - 2 + 3i", "3i"],
            ["2 - (2 + 3i)", "-3i"],
            ["2 - 4i + 2", "4 - 4i"],
            ["f(x) = 42 * x * i",   "42 * x * i"],
            ["f(4)",                "168i"],
            ["42i^0",                  "1"],
            ["42i^1",                  "42i"],
            ["42i^2",                  "-1764"],
            ["42i^3",                  "-74088i"],
            ["42i^4",                  "3111696"],
            ["(2 + 3i) ^ 0",             "1"],
            ["(2 + 3i) ^ 1",             "2 + 3i"],
            ["(2 + 3i) ^ 2",             "-5 + 12i"],
            ["(2 + 3i) ^ 3",             "-46 + 9i"],
            ["(2 + 3i) ^ 4",             "-119 - 120i"],
            ["(2 + 3i) ^ 5",             "122 - 597i"],
            ["i^0",                  "1"],
            ["i^1",                  "i"],
            ["i^2",                  "-1"],
            ["i^3",                  "-i"],
            ["i^4",                  "1"],
        ])

    def test_image_computation(self):
        self.do([
            ["varA = 2 + 4 *2 - 5 %4 + 2 * (4 + 5)",         "27"],
            ["funA(x) = 2 * 4 + x",                          "8 + x"],
            ["v = (1 + 2)^2",                                "9"],
            ["funB(x) = 4 -5 + (x + 2)^2 - 4",               "(x + 2) ^ 2 - 5"],
            ["funB(x) = 4 -5 + (x + 2)^2 - 4 + (x * 2) + 7", "(x + 2) ^ 2 + (x * 2) + 2"],
            ["v = 2^2",                                      "4"],
        ])

    def test_polynomials(self):
        self.do([
            ["f(x) = x^2 + 2x + 1", "x^2 + 2x + 1"],
            ["f(x) = ?",            "x^2 + 2x + 1"],
            ["f(x) = 2 ?",
                "x^2 + 2x - 1 = 0\n  The two R solutions are:\n  -2.414214\n  0.414214"],
            ["f(x) = 3x + 2 ?",
                "x^2 - x - 1 = 0\n  The two R solutions are:\n  -0.618034\n  1.618034"],

            ["b(x) = 3x + 2", "3 * x + 2"],
            ["f(x) = b ?",
                "x^2 - x - 1 = 0\n  The two R solutions are:\n  -0.618034\n  1.618034"],            
            ["f(x) = b(2) ?",
                "x^2 + 2x - 7 = 0\n  The two R solutions are:\n  -3.828427\n  1.828427"],
            ["f(x) = b(2) + 4x?",
                "x^2 - 2x - 7 = 0\n  The two R solutions are:\n  -1.828427\n  3.828427"],
            ["f(x) = b(2) + 4*x^2 + f(3)?",
                "-3 * x^2 + 2x - 23 = 0\n  The two C solutions are:\n  0.333333 - -2.748737i\n  0.333333 + -2.748737i"],
            ["f(x) = b(2) + 4*x^2 - f(3) + 2x - 2?",
                "-3 * x^2 + 11 = 0\n  The two R solutions are:\n  1.914854\n  -1.914854"],

            ["f(x) = 2x + 2 ?",
                "x^2 - 1 = 0\n  The two R solutions are:\n  -1.0\n  1.0"],
            ["f(x) = x^2 + 1 ?",   "2x = 0\n  The R solution is:\n  0"],
            ["f(2) = ?",           "9"],
            ["f(2) = 2 ?",         "7 = 0\n  The eqution has no solution"],
            ["f(2) = 9 ?",         "0 = 0\n  Every real number is a solution"],
            ["f(x) = -4*x^2 + 3x + 2 ?",
                "5 * x^2 - x - 1 = 0\n  The two R solutions are:\n  -0.358258\n  0.558258"],
            ["f(x) = x^2 + 2x + 1 ?",
                "0 = 0\n  Every real number is a solution"],
            ["a + 2 = 2 ?",
                "2 = 0\n  The eqution has no solution"],
            
            ["f(x) = 3^2 - 2",   "7"],
            ["f(x) = 0 ?",       "7 = 0\n  The eqution has no solution"],
            ["f(x) = 7 ?",       "0 = 0\n  Every real number is a solution"],
        ])

    def test_polynomials_computorv1_subject_examples(self):
        self.do([
            ["f(x) = 5 * X^0 + 4 * X^1 - 9.3 * X^2",  "-9.3 * x^2 + 4x + 5"],
            ["f(x) = 1 * X^0 ?",
                "-9.3 * x^2 + 4x + 4 = 0\n  The two R solutions are:\n  0.905239\n  -0.475131"],

            ["f(x) = 5 * X^0 + 4 * X^1", "4x + 5"],
            ["f(x) = 4 * X^0 ?",         "4x + 1 = 0\n  The R solution is:\n  -0.25"],

            ["f(x) = 8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3",
                "-5.6 * x^3 - 6x + 8"],
            ["f(x) = 3 * X^0 ?",
                "-5.6 * x^3 - 6x + 5 = 0\n  The polynomial degree is strictly greater than 2, I can't solve."],

            ["f(x) = 42 * X^0",  "42"],
            ["f(x) = 42 * X^0 ?",  "0 = 0\n  Every real number is a solution"],

            ["f(x) = 5 + 4 * X + X^2",  "x^2 + 4x + 5"],
            ["f(x) = X^2 ?",  "4x + 5 = 0\n  The R solution is:\n  -1.25"],
        ])

    def test_polynomials_computorv1_my_examples(self):
        self.do([
            ["f(x) = 1 * X^0 + 2 * X^1 + 1 * X^2",  "x^2 + 2x + 1"],
            ["f(x) = 0 ?",  "x^2 + 2x + 1 = 0\n  The R solution is:\n  -1.0"],
            # greater than 2, but 3 is 0, so can solve
            ["f(x) = 8 * X^0 - 6 * X^1 + 1 * X^2 - 0 * X^3",  "x^2 - 6x + 8"],
            ["f(x) = 3 * X^0 ?",  "x^2 - 6x + 5 = 0\n  The two R solutions are:\n  1.0\n  5.0"],

            ["f(x) = 1 * X^0 + 1 * X^1",    "x + 1"],
            ["f(x) = 0 ?",    "x + 1 = 0\n  The R solution is:\n  -1.0"],
            # non whole coefficients
            ["f(x) = 5.15 * X^0 + 0.4 * X^1 + 9.3 * X^2",    "9.3 * x^2 + 0.4x + 5.15"], 
            ["f(x) = 0.155 * X^0 + 0.2 * X^1 + 15.25345 * X^2 ?",
                "-5.95345 * x^2 + 0.2x + 4.995 = 0\n  The two R solutions are:\n  0.932925\n  -0.899332"],
            # every real number
            ["f(x) = 42 * X^0 + 2 * X^1",  "2x + 42"],
            ["f(x) = 42 * X^0 + 2 * X^1 ?",  "0 = 0\n  Every real number is a solution"],
            # every real number
            ["f(x) = 42 * X^0 + 2 * X^1 + 5 * X^2",  "5 * x^2 + 2x + 42"],
            ["f(x) = 42 * X^0 + 2 * X^1 + 5 * X^2 ?",
                "0 = 0\n  Every real number is a solution"],
            # complex solutions
            ["f(x) = 1 * X^0 + 2 * X^1 + 5 * X^2",  "5 * x^2 + 2x + 1"],
            ["f(x) = 0 ?",
                "5 * x^2 + 2x + 1 = 0\n  The two C solutions are:\n  -0.2 - 0.4i\n  -0.2 + 0.4i"],
            # complex solutions
            ["f(x) = 6.25 * X^0 + 4 * X^1 + 1 * X^2",   "x^2 + 4x + 6.25"],
            ["f(x) = 0 ?",
                "x^2 + 4x + 6.25 = 0\n  The two C solutions are:\n  -2.0 - 1.5i\n  -2.0 + 1.5i"],
            # complex solutions
            ["f(x) = 10 * X^0 - 3 * X^1 + 1 * X^2", "x^2 - 3x + 10"],
            ["f(x) = 0 ?",
                "x^2 - 3x + 10 = 0\n  The two C solutions are:\n  1.5 - 2.783882i\n  1.5 + 2.783882i"],
            # no solution
            ["f(x) = 42 * X^0",  "42"],
            ["f(x) = 24 * X^0 ?",  "18 = 0\n  The eqution has no solution"],
            # no solution
            ["f(x) = 1 * X^0 + 0 * X^1",    "1"],
            ["f(x) = 0 ?",    "1 = 0\n  The eqution has no solution"],
            # zero
            ["f(x) = 0 * X^0 + 1 * X^1",    "x"],
            ["f(x) = 0 ?",    "x = 0\n  The R solution is:\n  0"],
            # negative
            ["f(x) = -2 * X^0 - 1 * X^1",   "-x - 2"],
            ["f(x) = 0 ?",   "-x - 2 = 0\n  The R solution is:\n  -2.0"],
        ])


if __name__ == "__main__":
    unittest.main()