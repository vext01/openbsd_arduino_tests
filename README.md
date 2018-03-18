# OpenBSD Arduino Toolchain Tests

This repo houses tests for the arduino toolchain running on OpenBSD.

## Dependencies

You need:

 * Python-2.7
 * `py.test`

## Running tests

```
py.test test_arduino.py
```

Add '-v -s' for more verbose information.

## Adding more tests

 * Add your ino file into the `inos` directory.
 * Add a comment at the top saying where it came from (URL).
 * Add a test in `test_arduino.py`
