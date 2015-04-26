# OpenBSD Arduino Toolchain Tests

This repo houses tests for the arduino toolchain running on OpenBSD.

## Dependencies

You need:

 * Python-2.7
 * The `sh` module
 * `py.test`

```
$ sudo pkg_add -i py-test py-pip
$ pip2.7 install --user sh
```

## Running tests

```
py.test
```

Add '-v -s' for more verbose information.
