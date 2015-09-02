# unitframe
Unit testing TDD framework for source code development and verification.

Main components:
- [unitframe.py](unitframe.py)  - Runs unit tests in a loop
- [gate.py](gate.py)            - User commit gating script
- [templates/](templates)       - Templates directory for new projects/scripts 

## License
MIT License. For more information, please refer to [LICENSE](LICENSE)

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

Unitframe running [Cppunit](http://cppunit.github.io/cppunit/) (C++ unit testing) project

![cppunit](https://cloud.githubusercontent.com/assets/3139960/9642195/957b2946-516f-11e5-9d93-5807c4b8f9b9.jpg)

## gate.py - User commit gating script

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
- Script `-type c` ([Python](templates/template_script.py))
- Program `-type p/pc` ([Python](templates/template_program.py)/[C++](templates/template_program.cc))
- Contest solution `-type cf/cfc` ([Python](templates/template_contest.py)/[C++](templates/template_contest.cc))
