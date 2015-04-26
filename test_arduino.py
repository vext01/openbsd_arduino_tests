#!/usr/bin/env python2.7
# When hacking, please use PEP8

import sh
import shutil
import os

HERE = os.path.abspath(os.path.dirname(__file__))
WORK_DIR = os.path.join(HERE, "work")
INO_DIR = os.path.join(HERE, "inos")


def mk_project(proj_name, ino_file=None):
    """ builds a fresh arduino project and optionally copies in an ino """

    if not os.path.exists(WORK_DIR):
        os.mkdir(WORK_DIR)

    proj_dir = os.path.join(WORK_DIR, proj_name)
    if os.path.exists(proj_dir):
        shutil.rmtree(proj_dir)

    os.chdir(WORK_DIR)
    sh.arduinoproject(proj_name)
    os.chdir(HERE)

    if ino_file:
        shutil.copy(os.path.join(INO_DIR, ino_file), proj_dir)
    return proj_dir


def compile(proj_dir, make_flags=None):
    """ comples the project, optionally passing flags to make """
    if not make_flags:
        make_flags = []
    os.chdir(proj_dir)
    print(sh.make(*make_flags))
    os.chdir(HERE)

    # existing hex file indicates a succeeded compile
    proj_name = os.path.basename(proj_dir)
    assert os.path.exists(os.path.join(proj_dir, "applet", proj_name + ".hex"))

# >>> Tests below

def test_blank():
    """ blank project """
    proj = mk_project("blank")
    compile(proj)
