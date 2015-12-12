#!/usr/bin/env python3
# gate.py - User's commit gating script by Sergey 2015
# UnitFrame - Unit testing TDD framework (github.com/unitframe/unitframe)

"""
Searches for all files supporting unit testing (-ut option) in the specified
directory and runs them one by one. All tests must pass for gate script to
exit normally.
"""

# Modules
import unittest
import sys
import os
import argparse
import re
import random
import subprocess
import getpass
import shutil
import time

###############################################################################
# Gate Class
###############################################################################


class Gate:
    """ Gate representation """

    # Enums
    PYTHON, CPP, EXEC = range(3)

    # Configuration
    CFG_CPP_OPTS = "-std=c++11"
    CFG_EXTS = {"py": PYTHON, "cc": CPP, "": EXEC}

    # OS setting
    IS_WIN = (os.name == "nt")

    # XTerm colors
    XC_BOLD = '\033[1m' if not IS_WIN else ''
    XC_RED = '\033[91m' + XC_BOLD if not IS_WIN else ''
    XC_GRN = '\033[92m' + XC_BOLD if not IS_WIN else ''
    XC_ENDC = '\033[0m' if not IS_WIN else ''

    def __init__(self, arg_str=""):
        """ Default constructor """

        # Argument parsing
        self.arg_str = arg_str
        parser = argparse.ArgumentParser(
            description="Gate script")
        parser.add_argument(
            "path", nargs="?", default=os.getcwd(),
            help="Optional path")
        self.args = parser.parse_args(self.arg_str.split())

    def run(self, test=False):
        """ Main execution function """

        if test:
            return

        # Record the starting time
        start_time = time.time()

        fail = 0

        for ext in reversed(sorted(self.CFG_EXTS.keys())):
            language = self.CFG_EXTS[ext]

            # NOTE: Binary files are not supported
            if language == self.EXEC:
                continue

            # Search files
            pats = ["\." + ext + "$"]
            files = find_files(self.args.path, patterns=pats)

            for filename in files:

                if fail:
                    break

                # Check that file supports unit tests
                if not search_file("\-ut", filename):
                    continue

                print("\nGATE: Running Unit Tests for " + filename)

                if language == self.PYTHON:

                    # Run Python files
                    EXE = "python " if os.name == "nt" else ""
                    if os.system(EXE + filename + " -ut"):
                        fail = 1

                elif language == self.CPP:

                    # Run C++ files
                    bin = "/tmp/" + filename_strip_ext(filename)
                    options = self.CFG_CPP_OPTS
                    build = "g++ " + options + " -o " + bin + " " + filename

                    if os.system(build):
                        fail = 1
                    else:
                        if os.system(bin + " -ut"):
                            fail = 1

        elp_time = time.time() - start_time
        print("\nGATE: Elapsed Time " + str(round(elp_time, 3)) + "s")

        if fail:
            print("GATE: " + self.XC_RED + "FAILED!" + self.XC_ENDC)
            exit(1)
        else:
            print("GATE: " + self.XC_GRN + "ALL TESTS PASSED!" + self.XC_ENDC)


###############################################################################
# Helping functions
###############################################################################


def search_file(pattern, filename):
    """ Search file and return only the first match """
    if not os.path.exists(filename):
        raise Exception("Can't open file for reading! " + filename)

    fh = open(filename, "r")
    for line in fh:
        allmatch = re.findall(pattern, line)
        if allmatch:
            fh.close()
            return allmatch[0]

    fh.close()
    return None


def filename_strip_ext(filename):
    """ Return file name w/o extension and dirs """
    base = os.path.basename(filename)
    # Strip file extension
    return os.path.splitext(base)[0]


def find_files(dir, patterns=[]):
    result = []
    for path, dirs, files in os.walk(dir):
        for file in files:
            skip = 1 if patterns else 0
            for pattern in patterns:
                if re.search(pattern, file):
                    skip = 0
            if not skip:
                result.append(path + "/" + file)
    return result

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
        self.assertEqual(d.args.path, os.getcwd())

    def test_Gate_class__run(self):
        """ Main execution function """
        d = Gate()
        d.run(test=True)

    def test_xcleanup(self):
        shutil.rmtree(self.tmp_area)

if __name__ == "__main__":
    if sys.argv[-1] == "-ut":
        unittest.main(argv=[" "])
    Gate(" ".join(sys.argv[1:])).run()
