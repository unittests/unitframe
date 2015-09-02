# unitframe
Unit testing TDD framework

## License
MIT License. For more information, please refer to [LICENSE](LICENSE)

## unitframe.py - Tracks project changes and periodically reruns unit-tests

FIXME: Opens editor and xterm window and runs your self executable script after each
modification.

Unitframe running [Cppunit](http://cppunit.github.io/cppunit/) (C++ unit testing)

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
