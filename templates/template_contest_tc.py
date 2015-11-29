#!/usr/bin/env python3
# __Filename__ - __TC_Contest__ by __User__ __Year__

import unittest
import sys

###############################################################################
# __Class__ Class (Main Program)
###############################################################################


class __Class__:
    """ __Class__ representation """

    def __init__(self, *test_inputs):
        """ Default constructor """
        self.test_inputs = test_inputs

    def REPLACE_ME(self, nums):

        result = 0

        return result

    def calculate(self):
        """ Main calcualtion function of the class """
        return self.REPLACE_ME(self.test_inputs)

###############################################################################
# Unit Tests
###############################################################################


class unitTests(unittest.TestCase):

    def test_single_test(self):
        """ __Class__ class testing """

        # Sample test
        test = (2, 3, 4, 5)
        self.assertEqual(__Class__(test).calculate(), 0)

        # Sample test
        test = ()
        # self.assertEqual(__Class__(test).calculate(), 0)

        # Sample test
        test = ()
        # self.assertEqual(__Class__(test).calculate(), 0)

        # My tests
        test = ()
        # self.assertEqual(__Class__(test).calculate(), 0)

        # Time limit test
        # self.time_limit_test(5000)

    def time_limit_test(self, nmax):
        """ Timelimit testing """
        import random
        import timeit

        # Random inputs
        test = [random.randint(1, 10000) for i in range(nmax)]

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
    unittest.main(argv=[" "])
