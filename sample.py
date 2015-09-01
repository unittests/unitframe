#!/usr/bin/env python
# __Filename__ - <!!! Template !!!> program by __User__ __Year__

"""
<!!! Template !!!>

"""

# Standard modules
import unittest
import sys
import os
import argparse
import re
import random
import subprocess
import getpass
import shutil

# Additional modules


###############################################################################
# __Class__ Class (Main Program)
###############################################################################


class __Class__:
    """ __Class__ representation """

    def __init__(self, arg_str=""):
        """ Default constructor """

        # Argument parsing
        self.arg_str = arg_str
        parser = argparse.ArgumentParser(
            description="__Class__ script")
        parser.add_argument(
            "arg", nargs="?", default="", help="optional argument")
        parser.add_argument(
            "-a", action="store_true", default="", help="Option")
        self.args = parser.parse_args(self.arg_str.split())

    def run(self, test=False):
        """ Main execution function """

        if test:
            return

###############################################################################
# Unit Tests
###############################################################################


class unitTests(unittest.TestCase):

    tmp_area = "/tmp/ut" + getpass.getuser()
    test_area = tmp_area + "/t" + str(random.randrange(10000))
    tmp_file = test_area + "/f" + str(random.randrange(10000))

    def setUp(self):
        os.makedirs(self.test_area, exist_ok=True)

    def test___Class___class__basic_functionality(self):
        """ __Class__ class basic testing """
        d = __Class__()
        self.assertEqual(d.args.a, "")

    def test___Class___class__run(self):
        """ Main execution function """
        d = __Class__()
        d.run(test=True)

    def test_xcleanup(self):
        shutil.rmtree(self.tmp_area)

if __name__ == "__main__":
    if sys.argv[-1] == "-ut":
        unittest.main(argv=[" "])
    __Class__(" ".join(sys.argv[1:])).run()
