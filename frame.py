#!/usr/bin/env python
# frame.py - Track project changes and rerun unit-tests
#
# Copyright (C) 2013 Sergey Sokolov, License MIT

"""
Opens editor and xterm window and runs your self executable script after each
modification.

"""

# Standard modules
import unittest
import sys
import os
import argparse
import re
import random
import getpass
import shutil

# Additional modules
import datetime
import time


###############################################################################
# Frame Class
###############################################################################


class Frame:
    """ Monitors all updates to dependent files and reruns the project """

    script_dir = os.path.dirname(os.path.realpath(__file__))

    IS_WIN = (os.name == "nt")
    CMD_CLEAR = "cls" if IS_WIN else "clear"
    CMD_PEP8 = os.path.join(script_dir, "pep8.py")
    CMD_SEP = " & " if IS_WIN else " ; "
    CMD_EDITOR = "%EDITOR%" if IS_WIN else "$EDITOR"
    UPDATE_PERIOD = .5
    XTERM_OPT = "+aw -bg darkgreen -fg white -geometry 70x20+0+200"
    TYPES = {
        "py":  ("python",  "py", "sample.py",     ""),
        "i":   ("python",  "py", "sample_i.py",   ""),
        "cf":  ("python",  "py", "sample_cf.py",  "codeforces"),
        "cc":  ("c++",     "cc", "sample_i.cc",   ""),
        "cfc": ("c++",     "cc", "sample_cf.cc",  "codeforces")}
    CPP_OPTIONS = "-std=c++11"
    CPP_DEBUG_OPTIONS = (
        "-Wall -Wextra -pedantic -O2 -Wshadow -Wformat=2 " +
        "-Wfloat-equal -Wconversion -Wlogical-op -Wcast-qual -Wcast-align " +
        "-D_GLIBCXX_DEBUG_PEDANTIC -D_FORTIFY_SOURCE=2")

    def __init__(self, arg_str=""):
        """ Default constructor """

        # Argument parsing
        self.arg_str = arg_str
        parser = argparse.ArgumentParser(
            description="Frame script")
        parser.add_argument(
            "proj", help="Project name (required argument)")
        parser.add_argument(
            "-type", action="store", default="",
            help="New project type: " + ", ".join(sorted(self.TYPES.keys())))
        parser.add_argument(
            "-xterm", action="store_true", default="", help="Xterm mode")
        parser.add_argument(
            "-new", action="store_true", default="",
            help="Create a new Project")
        parser.add_argument(
            "-pre", action="store", default="",
            help="Run a Programm on top of the Project")
        parser.add_argument(
            "-args", action="store", default="",
            help="Passing argument to the Project")
        self.args = parser.parse_args(self.arg_str.split())

        self.cmd = ""
        self.cf_contest = ""

        # Default project type
        if not self.args.type:
            self.args.type = "py"

        # Extracting project type from the file extension
        ext = filename_ext(self.args.proj)
        if ext in self.TYPES.keys():
            self.args.type = ext

        # Check resulting type
        if self.args.type not in self.TYPES.keys():
            raise Exception("Project type is not supported! ", self.args.type)

        # Extract type details from hash
        type = self.TYPES[self.args.type]
        (self.language, self.ext, self.template, self.category) = type

        # Add extension for various project types
        if not re.match(".*\." + self.ext + "$", self.args.proj):
            self.args.proj += "." + self.ext

        # Extract contest name from the project
        if self.category == "codeforces":
            proj_name = filename_strip_ext(self.args.proj)
            allmatch = re.match("^([^_]*)_(.*)$", proj_name)
            if allmatch:
                self.cf_contest = allmatch.group(1)
                self.cf_project = allmatch.group(2)
            else:
                raise Exception("Expected contest name prefix")

    def create_new_project(self, filename):
        """ Create a new project file and replace """
        if os.path.exists(filename):
            return 0

        template_file = self.script_dir + "/"
        template_file += self.template

        proj_name = filename_strip_ext(filename)

        # Special project name for Codeforces
        if self.category == "codeforces":
            proj_name = self.cf_project

        os.system(
            "cp " + os.path.normpath(template_file) + " " +
            os.path.normpath(filename))

        replace_file("__Filename__", filename, filename)
        replace_file("__Class__", proj_name.capitalize(), filename)

        date = datetime.date.today().strftime('%d/%m/%Y')
        replace_file("__Date__", date, filename)

        year = datetime.date.today().strftime('%Y')
        replace_file("__Year__", year, filename)

        user = getpass.getuser().capitalize()
        replace_file("__User__", user, filename)

        contest = ""
        if self.category == "codeforces":
            contest = " Codeforces.com/problemset/problem/"
            m = re.search("(\d+)(\w)", self.cf_contest)
            if not m:
                raise Exception("Wrong contest format " + self.cf_contest)
            contest += m.group(1) + "/" + m.group(2)
        replace_file("__Contest__", contest, filename)

        return 1

    def set_cmd(self, filename):
        """ Program a cmd line for a watcher function """
        if self.args.xterm:
            prog_cmd = filename

            # Additional commands for python
            if self.language == "python":
                # Run PEP8 for python scripts
                self.cmd += self.CMD_PEP8 + " " + filename + self.CMD_SEP
                # For Win frame needs to be run by python program
                if self.IS_WIN:
                    prog_cmd = "python " + prog_cmd
                # Use -ut for python scripts
                prog_cmd += " -ut"

            # Additional commands for C++
            if self.language == "c++":
                binary = "/tmp/" + filename_strip_ext(self.args.proj)
                binary_exe = os.path.normpath(binary + ".exe")
                options = self.CPP_OPTIONS + " " + self.CPP_DEBUG_OPTIONS
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
                    "xterm " + Frame.XTERM_OPT + " -T '" + filename +
                    "' -e \"" + editor_cmd + " &; " + frame_cmd + "; csh\"&")

    def run(self, test=False):
        """ Main execution function """

        if not os.path.exists(self.args.proj):
            if not test:
                print("Can't find project. Created a NEW one!")
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
                time.sleep(self.UPDATE_PERIOD)
        else:
            print("PROJ : ", self.args.proj)
            os.system(self.cmd)

###############################################################################
# Executable code
###############################################################################


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


def main():

    # Sandbox
    sb = Frame(" ".join(sys.argv[1:]))
    sb.run()

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

    def test_Frame_class__basic_functions(self):
        """ Basic functions """
        proj = self.tmp_file + "_new"
        proj_py = proj + ".py"
        f = Frame(proj + " -new")
        self.assertEqual(f.args.proj, proj_py)
        f.run(test=True)
        os.remove(proj_py)

    def test_Frame_class__create_new_project(self):
        """ Create new project if file does not exists, make sure that py file
        extension is not added twice"""
        py_file = self.tmp_file + ".py"
        f = Frame(py_file + " -type py")
        self.assertEqual(f.create_new_project(f.args.proj), 1)
        proj_name = filename_strip_ext(self.tmp_file)
        self.assertEqual(
            os.system(
                "cat " + os.path.normpath(py_file) + "| grep " +
                proj_name + " -q"), 0)

        # Project already exists
        self.assertEqual(f.create_new_project(f.args.proj), 0)

        # Make sure prefix is stripped from file name for codeforces projects
        pref = "552"
        test_file = self.test_area + "/" + pref + "_project"
        py_file = test_file + ".py"
        f = Frame(test_file + " -type cf")
        self.assertEqual(f.cf_contest, "552")
        self.assertEqual(f.cf_project, "project")
        self.assertEqual(f.create_new_project(f.args.proj), 1)
        proj_name = filename_strip_ext(self.tmp_file)
        self.assertEqual(
            os.system(
                "cat " + os.path.normpath(py_file) +
                "| grep \"class Project\" -q"), 0)

        # Code forces C++ project
        cpp_file = test_file + ".cc"
        f = Frame(test_file + " -type cfc")
        self.assertEqual(f.cf_contest, "552")
        self.assertEqual(f.cf_project, "project")
        self.assertEqual(f.create_new_project(f.args.proj), 1)
        self.assertEqual(
            os.system(
                "cat " + os.path.normpath(cpp_file) +
                "| grep \"namespace std\" -q"), 0)

    def test_Frame_class__set_cmd(self):
        """ Create watcher cmd """
        self.maxDiff = None
        proj = self.tmp_file + "_cmd"
        f = Frame(proj + " -new -arg arg -pre pre")
        f.set_cmd(proj)
        if f.IS_WIN:
            self.assertEqual(
                f.cmd, "%EDITOR% " + proj + " & START python " + sys.argv[0] +
                " " + proj + " -new -arg arg -pre pre -xterm")
        else:
            self.assertEqual(
                f.cmd, "xterm " + Frame.XTERM_OPT + " -T '" + proj +
                "' -e \"$EDITOR " + proj + " &; " + sys.argv[0] +
                " " + proj + " -new -arg arg -pre pre" +
                " -xterm; csh\"&")

        proj = self.tmp_file + "_xcmd"
        f = Frame(proj + " -new -x -arg arg -pre pre")
        f.set_cmd(proj)
        self.assertEqual(
            f.cmd, f.CMD_PEP8 + " " + proj + f.CMD_SEP + "pre " +
            ("python " if f.IS_WIN else "") +
            proj + " -ut arg")

    def test_xcleanup(self):
        shutil.rmtree(self.tmp_area)

if __name__ == '__main__':
    if sys.argv[-1] == "-ut":
        unittest.main(argv=[" "])
    main()
