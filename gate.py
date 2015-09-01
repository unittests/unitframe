#!/usr/bin/env python
# gate.py - Searches for and runs all repo gating tests
#
# Copyright (C) 2015 Sergey Sokolov, License MIT

"""
Repo gating test runner. Searches for all python files containing unit tests
and executes all tests in order.

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
import filehelp
import time


###############################################################################
# Gate Class
###############################################################################


class Gate:
    """ Gate representation """

    TYPES = {
        "py":  "python",
        "cc":  "c++"}

    def __init__(self, arg_str=""):
        """ Default constructor """

        # Argument parsing
        self.arg_str = arg_str
        parser = argparse.ArgumentParser(
            description="Gate script")
        parser.add_argument(
            "path", nargs="?", default=filehelp.gitroot(),
            help="Optional path")
        self.args = parser.parse_args(self.arg_str.split())

    def run(self, test=False):
        """ Main execution function """

        if test:
            return

        # Record the starting time
        start_time = time.time()

        fail = 0

        for ext in self.TYPES.keys():
            language = self.TYPES[ext]

            # Search files
            pats = ["\." + ext + "$"]
            files = filehelp.find_files(self.args.path, patterns=pats)

            for filename in files:

                if fail:
                    break

                # Check that file supports unit tests
                if not filehelp.search_file("\-ut", filename):
                    continue

                print("\nGATE: Running Unit Tests for " + filename)

                if language == "python":

                    # Run Python files
                    if os.system("python " + filename + " -ut"):
                        fail = 1
                elif language == "c++":

                    # Run C++ files
                    bin = "/tmp/" + filehelp.filename_strip_ext(filename)
                    # options = ""
                    options = "-std=c++11"
                    build = "g++ " + options + " -o " + bin + " " + filename

                    if os.system(build):
                        fail = 1
                    else:
                        if os.system(bin + " -ut"):
                            fail = 1

        elp_time = time.time() - start_time
        print("\nGATE: Elapsed Time " + str(round(elp_time, 3)) + "s")

        if fail:
            print("GATE: FAILED!")
            exit(1)
        else:
            print("GATE: ALL TESTS PASSED!")


###############################################################################
# Executable code
###############################################################################


def main():

    # Sandbox
    sb = Gate(" ".join(sys.argv[1:]))
    sb.run()

###############################################################################
# Unit Tests
###############################################################################


class unitTests(unittest.TestCase):

    tmp_area = "/tmp/ut" + getpass.getuser()
    test_area = tmp_area + "/t" + str(random.randrange(10000))
    tmp_file = test_area + "/f" + str(random.randrange(10000))

    def setUp(self):
        os.makedirs(self.test_area, exist_ok=True)

    def test_Gate_class__basic_functionality(self):
        """ Gate class basic testing """

        # Check default path is repo root
        d = Gate()
        gitroot = filehelp.gitroot()
        self.assertEqual(d.args.path, gitroot)

    def test_Gate_class__run(self):
        """ Main execution function """
        d = Gate()
        d.run(test=True)

    def test_xcleanup(self):
        shutil.rmtree(self.tmp_area)

if __name__ == "__main__":
    if sys.argv[-1] == "-ut":
        unittest.main(argv=[" "])
    main()
