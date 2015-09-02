# unitframe
Unit testing TDD framework for rapid source code development and verification. 

It was written primarily for Python, but C++ is also supported.

Main components:
- [unitframe.py](unitframe.py)  - Runs unit tests in a loop
- [gate.py](gate.py)            - User commit gating script
- [templates/](templates)       - Templates directory for new projects/scripts 
- [checks/](checks)             - Source code lint checks (currently only Pep8 for Python)

## License
MIT License. For more information, please refer to [LICENSE](LICENSE)

## Usage requirements
Each program has to support `-ut` command line switch which is used to enable unit testing mode of a program (always enabled is okay).

Programming languages supported: 
- Python (Win/Linux)
- C++ (Windows MinGW only)

It is recommended to use following unit testing libraries:
- Python - [Unittest](https://docs.python.org/3/library/unittest.html) native library
- C++ - [Cppunit](http://cppunit.github.io/cppunit/)

## unitframe.py - Runs unit tests in a loop
Will open editor and new xterm window for unit tests to be run in a loop. Unit tests will be run each time project is updated and saved.

```
usage: unitframe.py [-h] [-type TYPE] [-xterm] [-pre PRE] [-args ARGS] proj

Unitframe script

positional arguments:
  proj        Project name (required argument)

optional arguments:
  -h, --help  show this help message and exit
  -type TYPE  New project template (default p): cf template_contest.py, cfc
              template_contest.cc, p template_program.py, pc
              template_program.cc, s template_script.py
  -xterm      Xterm mode
  -pre PRE    Run a Programm on top of the Project
  -args ARGS  Passing argument to the Project
```

Unitframe launching GVIM and terminal window with one [Cppunit](http://cppunit.github.io/cppunit/) unit test failing after executing the following command:

`> unitframe 574D_blocks.cc`

![blocks](https://cloud.githubusercontent.com/assets/3139960/9644637/19b1065c-517c-11e5-8c73-ed636bbfc5bd.jpg)

## gate.py - User's commit gating script

Searches for all files supporting unit testing (-ut option) in the specified directory and runs them one by one. All tests must pass for gate script to exit normally.

`usage: gate.py [-h] [path]`

Gate passing all tests:
```
GATE: Running Unit Tests for codeforces/574D_blocks.cc
.....
--------------------------------------------------
Ran 5 checks in 0.049s

OK

GATE: Elapsed Time 37.829s
GATE: ALL TESTS PASSED!
```

## Templates for new projects

New project templates available:
- Basic script template `-type c` ([Python](templates/template_script.py))
- Program teplate `-type p/pc` ([Python](templates/template_program.py)/[C++](templates/template_program.cc))
- Contest solution template `-type cf/cfc` ([Python](templates/template_contest.py)/[C++](templates/template_contest.cc))
