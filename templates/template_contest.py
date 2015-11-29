#!/usr/bin/env python3
# __Filename__ - __CF_Contest__ by __User__ __Year__

import unittest
import sys

###############################################################################
# __Class__ Class (Main Program)
###############################################################################


class __Class__:
    """ __Class__ representation """

    def __init__(self, test_inputs=None):
        """ Default constructor """

        it = iter(test_inputs.split("\n")) if test_inputs else None

        def uinput():
            return next(it) if it else sys.stdin.readline().rstrip()

        # Reading single elements
        [self.n, self.m] = map(int, uinput().split())

        # Reading multiple number of lines of the same number of elements each
        l, s = self.n, 2
        inp = (" ".join(uinput() for i in range(l))).split()
        self.numm = [[int(inp[i]) for i in range(j, l*s, s)] for j in range(s)]
        self.numa, self.numb = self.numm

        # Reading a single line of multiple elements
        self.nums = list(map(int, uinput().split()))

    def calculate(self):
        """ Main calcualtion function of the class """

        result = 0

        return str(result)

###############################################################################
# Unit Tests
###############################################################################


class unitTests(unittest.TestCase):

    def test_single_test(self):
        """ __Class__ class testing """

        # Constructor test
        test = "2 3\n1 2\n3 4\n1 2 3"
        d = __Class__(test)
        self.assertEqual(d.n, 2)
        self.assertEqual(d.m, 3)
        self.assertEqual(d.numa, [1, 3])
        self.assertEqual(d.numb, [2, 4])
        self.assertEqual(d.nums, [1, 2, 3])

        # Sample test
        # self.assertEqual(__Class__(test).calculate(), "0")

        # Sample test
        test = ""
        # self.assertEqual(__Class__(test).calculate(), "0")

        # Sample test
        test = ""
        # self.assertEqual(__Class__(test).calculate(), "0")

        # My tests
        test = ""
        # self.assertEqual(__Class__(test).calculate(), "0")

        # Time limit test
        # self.time_limit_test(5000)

    def time_limit_test(self, nmax):
        """ Timelimit testing """
        import random
        import timeit

        # Random inputs
        test = str(nmax) + " " + str(nmax) + "\n"
        numnums = [str(i) + " " + str(i+1) for i in range(nmax)]
        test += "\n".join(numnums) + "\n"
        nums = [random.randint(1, 10000) for i in range(nmax)]
        test += " ".join(map(str, nums)) + "\n"

        # Run the test
        start = timeit.default_timer()
        d = __Class__(test)
        calc = timeit.default_timer()
        d.calculate()
        stop = timeit.default_timer()
        print("\nTimelimit Test: " +
              "{0:.3f}s (init {1:.3f}s calc {2:.3f}s)".
              format(stop-start, calc-start, stop-calc))

if __name__ == "__main__":

    # Avoiding recursion limitaions
    sys.setrecursionlimit(100000)

    if sys.argv[-1] == "-ut":
        unittest.main(argv=[" "])

    # Print the result string
    sys.stdout.write(__Class__().calculate())
