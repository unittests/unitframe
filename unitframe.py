#!/usr/bin/env python3
# unitframe.py - Runs unit tests in a loop by Sergey 2015
# UnitFrame - Unit testing TDD framework (github.com/unitframe/unitframe)

"""
Will open up the default editor and new xterm window for unit tests to be run
in a loop. Unit tests will be run each time project is updated and saved.

"""

# Modules
import unittest
import sys
import os
import argparse
import re
import random
import getpass
import shutil
import datetime
import time


###############################################################################
# Unitframe Class
###############################################################################


class Unitframe:
    """ Monitors all updates to dependent files and reruns the project """

    # Enums
    PYTHON, CPP, EXEC = range(3)

    # Configuration
    CFG_UPDATE_PERIOD = .5
    CFG_X_XTERM_OPT = "+aw -bg darkgreen -fg white -geometry 70x20+0+200"
    CFG_CPP_OPTS = "-std=c++11"
    CFG_CPP_DEBUG_OPTS = (
        "-Wall -Wextra -pedantic -O2 -Wshadow -Wformat=2 " +
        "-Wfloat-equal -Wconversion -Wlogical-op -Wcast-qual -Wcast-align " +
        "-D_GLIBCXX_DEBUG_PEDANTIC -D_FORTIFY_SOURCE=2")
    CFG_EXTS = {"py": PYTHON, "cc": CPP, "": EXEC}
    CFG_TYPES = {
        "s":   "template_script.py",
        "p":   "template_program.py",
        "pc":  "template_program.cc",
        "cf":  "template_contest.py",
        "cfc": "template_contest.cc"}

    # Command constants
    IS_WIN = (os.name == "nt")
    CMD_CLEAR = "cls" if IS_WIN else "clear"
    CMD_SEP = " & " if IS_WIN else " ; "
    CMD_EDITOR = "%EDITOR%" if IS_WIN else "$EDITOR"

    def __init__(self, arg_str=""):
        """ Default constructor """

        # Argument parsing
        self.arg_str = arg_str
        parser = argparse.ArgumentParser(
            description="Unitframe script")
        parser.add_argument(
            "proj", help="Project name (required argument)")
        parser.add_argument(
            "-type", action="store", default="p",
            help="New project template (default p): " +
            ", ".join(sorted(
                [v + " " + self.CFG_TYPES[v] for v in self.CFG_TYPES])))
        parser.add_argument(
            "-xterm", action="store_true", default="", help="Xterm mode")
        parser.add_argument(
            "-pre", action="store", default="",
            help="Run a Programm on top of the Project")
        parser.add_argument(
            "-args", action="store", default="",
            help="Passing argument to the Project")
        self.args = parser.parse_args(self.arg_str.split())

        # Calculate paths
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        self.checks_dir = os.path.join(self.script_dir, "checks")
        self.templates_dir = os.path.join(self.script_dir, "templates")

        # New project or existing
        self.is_new = not os.path.exists(self.args.proj)

        # Add extensions for new projects if missing
        if self.is_new:
            ext = filename_ext(self.CFG_TYPES[self.args.type])
            if not re.match(".*\." + ext + "$", self.args.proj):
                self.args.proj += "." + ext
                # Check for existing file one more time
                self.is_new = not os.path.exists(self.args.proj)

        # Project language and extension
        self.language = self.CFG_EXTS[filename_ext(self.args.proj)]

    def create_new_project(self, filename):
        """ Create a new project file and replace """

        # Extract template info from hash
        template = self.CFG_TYPES[self.args.type]
        template_file = os.path.join(self.templates_dir, template)
        proj_name = filename_strip_ext(filename)

        os.system(
            "cp " + os.path.normpath(template_file) + " " +
            os.path.normpath(filename))

        # Contest replacement
        # NOTE: Needs to happen before Class replacement
        if search_file("__Contest__", filename):

            allmatch = re.match("^([^_]*)_(.*)$", proj_name)
            if allmatch:
                self.cont_num = allmatch.group(1)
                self.cont_project = allmatch.group(2)
            else:
                raise Exception("Expected contest num as a prefix")

            proj_name = self.cont_project

            contest = " Codeforces.com/problemset/problem/"
            m = re.search("(\d+)(\w)", self.cont_num)
            if not m:
                raise Exception("Wrong contest format " + self.cont_num)
            contest += m.group(1) + "/" + m.group(2)
            replace_file("__Contest__", contest, filename)

        replace_file("__Filename__", filename, filename)
        replace_file("__Class__", proj_name.capitalize(), filename)

        date = datetime.date.today().strftime('%d/%m/%Y')
        replace_file("__Date__", date, filename)

        year = datetime.date.today().strftime('%Y')
        replace_file("__Year__", year, filename)

        user = getpass.getuser().capitalize()
        replace_file("__User__", user, filename)

    def set_cmd(self, filename):
        """ Program a cmd line for a watcher function """
        self.cmd = ""
        if self.args.xterm:
            prog_cmd = filename

            # Additional commands for python
            if self.language == self.PYTHON:

                # Run PEP8 for python scripts
                self.cmd += os.path.join(self.checks_dir, "pep8.py")
                self.cmd += " " + filename + self.CMD_SEP

                # For Win frame needs to be run by python program
                if self.IS_WIN:
                    prog_cmd = "python " + prog_cmd
                # Use -ut for python scripts
                prog_cmd += " -ut"

            # Additional commands for C++
            if self.language == self.CPP:
                binary = "/tmp/" + filename_strip_ext(self.args.proj)
                binary_exe = os.path.normpath(binary + ".exe")
                options = self.CFG_CPP_OPTS + " " + self.CFG_CPP_DEBUG_OPTS
                prog_cmd = "rm -f " + binary_exe + self.CMD_SEP
                prog_cmd += "g++ " + options + " -o " + binary + " "
                prog_cmd += filename + self.CMD_SEP
                prog_cmd += binary + " -ut"

            # Final cmd string
            self.cmd += self.args.pre + " " + prog_cmd + " " + self.args.args
        else:
            editor_cmd = self.CMD_EDITOR + " " + filename
            frame_cmd = sys.argv[0] + " " + self.arg_str + " -xterm"
            if self.IS_WIN:
                # For Win frame itself needs to be run by python program
                frame_cmd = "python " + frame_cmd
                self.cmd += editor_cmd + self.CMD_SEP + "START " + frame_cmd
            else:
                self.cmd += (
                    "xterm " + self.CFG_X_XTERM_OPT + " -T '" + filename +
                    "' -e \"" + editor_cmd + " &; " + frame_cmd + "; csh\"&")

    def run(self, test=False):
        """ Main execution function """

        if self.is_new:
            if not test:
                print("Can't find project " + self.args.proj)
                print("Created a NEW one!")
            self.create_new_project(self.args.proj)

        self.set_cmd(self.args.proj)

        if test:
            return

        if self.args.xterm:
            watcher_files = [self.args.proj]
            update = datetime.datetime.min
            while True:
                if files_are_modified(watcher_files, update):
                    update = datetime.datetime.utcnow()
                    os.system(self.CMD_CLEAR)
                    ftime = datetime.datetime.now().strftime('%H:%M:%S')
                    print(ftime + " Running " + self.args.proj)
                    os.system(self.cmd)
                time.sleep(self.CFG_UPDATE_PERIOD)
        else:
            print("PROJ : ", self.args.proj)
            os.system(self.cmd)

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


def replace_file(pattern, substr, filename):
    """ Replaces pattern with a sub-string in the file """
    file_handle = open(filename, "r")
    file_string = file_handle.read()
    file_handle.close()

    file_string = re.sub(pattern, substr, file_string)

    file_handle = open(filename, "w", newline="\n")
    file_handle.write(file_string)
    file_handle.close()


def filename_strip_ext(filename):
    """ Return file name w/o extension and dirs """
    base = os.path.basename(filename)
    # Strip file extension
    return os.path.splitext(base)[0]


def filename_ext(filename):
    """ Return file name extension """
    base = os.path.basename(filename)
    return os.path.splitext(base)[1][1:]


def file_get_mdatetime(filename):
    """ Calulating the modification datetime of the file """
    return datetime.datetime.utcfromtimestamp(os.path.getmtime(filename))


def file_is_modified(filename, lastupdate):
    """ Return true if file was modified since the last update time """
    now = datetime.datetime.utcnow()
    update = file_get_mdatetime(filename)
    return now >= update and update >= lastupdate


def files_are_modified(filenames, lastupdate):
    """ Return true if one of files was modified """
    for filename in filenames:
        if file_is_modified(filename, lastupdate):
            return True
    return False

###############################################################################
# Unit Tests
###############################################################################


class unitTests(unittest.TestCase):

    tmp_area = "/tmp/ut" + getpass.getuser()
    test_area = tmp_area + "/t" + str(random.randrange(10000))
    tmp_file = test_area + "/f" + str(random.randrange(10000))

    now = datetime.datetime.utcnow()
    now_minus_1s = now - datetime.timedelta(seconds=1)

    def setUp(self):
        os.makedirs(self.test_area, exist_ok=True)

    def test_Unitframe_class__basic_functions(self):
        """ Basic functions """
        proj = self.tmp_file + "_new"
        proj_py = proj + ".py"
        f = Unitframe(proj)
        self.assertEqual(f.args.proj, proj_py)
        f.run(test=True)
        os.remove(proj_py)

    def test_Unitframe_class__create_new_project(self):
        """ Create new project if file does not exists, make sure that py file
        extension is not added twice"""
        py_file = self.tmp_file + ".py"
        f = Unitframe(py_file + " -type s")
        f.create_new_project(f.args.proj)
        proj_name = filename_strip_ext(self.tmp_file)
        self.assertEqual(
            os.system(
                "cat " + os.path.normpath(py_file) + "| grep " +
                proj_name + " -q"), 0)

        # Make sure prefix is stripped from file name for contest projects
        pref = "552"
        test_file = self.test_area + "/" + pref + "_project"
        py_file = test_file + ".py"
        f = Unitframe(test_file + " -type cf")
        f.create_new_project(f.args.proj)
        self.assertEqual(f.cont_num, "552")
        self.assertEqual(f.cont_project, "project")
        proj_name = filename_strip_ext(self.tmp_file)
        self.assertEqual(
            os.system(
                "cat " + os.path.normpath(py_file) +
                "| grep \"class Project\" -q"), 0)

        # Code forces C++ project
        cpp_file = test_file + ".cc"
        f = Unitframe(test_file + " -type cfc")
        f.create_new_project(f.args.proj)
        self.assertEqual(f.cont_num, "552")
        self.assertEqual(f.cont_project, "project")
        self.assertEqual(
            os.system(
                "cat " + os.path.normpath(cpp_file) +
                "| grep \"namespace std\" -q"), 0)

    def test_Unitframe_class__set_cmd(self):
        """ Create watcher cmd """
        self.maxDiff = None
        proj = self.tmp_file + "_cmd"
        f = Unitframe(proj + " -arg arg -pre pre")
        f.set_cmd(proj)
        if f.IS_WIN:
            self.assertEqual(
                f.cmd, "%EDITOR% " + proj + " & START python " + sys.argv[0] +
                " " + proj + " -arg arg -pre pre -xterm")
        else:
            self.assertEqual(
                f.cmd, "xterm " + f.CFG_X_XTERM_OPT + " -T '" + proj +
                "' -e \"$EDITOR " + proj + " &; " + sys.argv[0] +
                " " + proj + " -arg arg -pre pre" +
                " -xterm; csh\"&")

        proj = self.tmp_file + "_xcmd"
        f = Unitframe(proj + " -x -arg arg -pre pre")
        f.set_cmd(proj)
        self.assertEqual(
            f.cmd, os.path.join(f.checks_dir, "pep8.py") + " " + proj +
            f.CMD_SEP + "pre " + ("python " if f.IS_WIN else "") +
            proj + " -ut arg")

    def test_xcleanup(self):
        shutil.rmtree(self.tmp_area)

if __name__ == '__main__':
    if sys.argv[-1] == "-ut":
        unittest.main(argv=[" "])
    Unitframe(" ".join(sys.argv[1:])).run()
