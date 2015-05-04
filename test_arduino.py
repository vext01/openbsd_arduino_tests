#!/usr/bin/env python2.7
# When hacking, please use PEP8

import sh
import shutil
import os
import pytest

HERE = os.path.abspath(os.path.dirname(__file__))
WORK_DIR = os.path.join(HERE, "work")
INO_DIR = os.path.join(HERE, "inos")

USB_VID = '0x2341'
USB_PID = '0x803c'
USB_MANUFACTURER = '"\\"Unknown\\""'
USB_PRODUCT = '"\\"Arduino Micro\\""'
USB_FLAGS = ("USER_CXXFLAGS=-DUSB_VID=%s -DUSB_PID=%s " +
             "-DUSB_MANUFACTURER=%s -DUSB_PRODUCT=%s") % (
                 USB_VID, USB_PID, USB_MANUFACTURER, USB_PRODUCT)


def mk_project(proj_name, ino_file=True):
    """ builds a fresh arduino project and optionally copies in an ino """

    print("")  # for verbose mode, newline before debug info

    if not os.path.exists(WORK_DIR):
        os.mkdir(WORK_DIR)

    proj_dir = os.path.join(WORK_DIR, proj_name)
    print("Removing existing project dir...")
    if os.path.exists(proj_dir):
        shutil.rmtree(proj_dir)

    os.chdir(WORK_DIR)
    sh.arduinoproject(proj_name)
    os.chdir(HERE)

    if ino_file:
        shutil.copy(os.path.join(INO_DIR, proj_name + ".ino"), proj_dir)
    return proj_dir


def compile(proj_dir, make_flags=None):
    """ comples the project, optionally passing flags to make """

    if not make_flags:
        make_flags = []
    os.chdir(proj_dir)
    print("Running 'make %s'" % " ".join(make_flags))
    print(sh.make(make_flags))
    os.chdir(HERE)

    # existing hex file indicates a succeeded compile
    proj_name = os.path.basename(proj_dir)
    assert os.path.exists(os.path.join(proj_dir, "applet", proj_name + ".hex"))

# >>> Tests below


def test_blank():
    proj = mk_project("blank", ino_file=False)
    compile(proj)


def test_webserver():
    proj = mk_project("webserver")
    compile(proj, ['LIBRARIES=SPI Ethernet'])


def test_eeprom():
    proj = mk_project("eeprom")
    compile(proj, ['LIBRARIES=EEPROM'])


def test_lcd():
    proj = mk_project("lcd")
    compile(proj, ['LIBRARIES=LiquidCrystal Wire'])


def test_datalogger():
    proj = mk_project("datalogger")
    compile(proj, ['LIBRARIES=SD SPI'])


def test_bridge():
    proj = mk_project("bridge")
    compile(proj, ['LIBRARIES=Bridge File'])


# #error If you are here, you should check what is exactly the processor
# you are using...
# AND
# avr32/io.h: No such file or directory
#
# I think this is because our avr-gcc doesn't target avr32?
# I see there is a separate avr32 port.
@pytest.mark.xfail
def test_wifi():
    proj = mk_project("wifi")
    compile(proj, ['LIBRARIES=WiFi Bridge', 'VARIANT=yun',
                   'MCU=atmega32u4', USB_FLAGS])

# If the abpve comment about avr32 is correct, this test passes as a fluke.
def test_esplorablink():
    proj = mk_project("esplorablink")
    compile(proj, ['LIBRARIES=Esplora', 'VARIANT=leonardo',
                   'MCU=atmega32u4', USB_FLAGS])

# XXX test extra user flags and files.
