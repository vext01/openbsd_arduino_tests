import sh
import shutil
import os

WORK_DIR = "work"
INO_DIR = "inos"
HERE = os.path.abspath(os.path.dirname(__file__))

def mk_project(proj_name, ino_file=None):
    """ builds a fresh arduino project and optionally copies in an ino """
    proj_dir = os.path.join(WORK_DIR, proj_name)
    if os.path.exists(proj_dir):
        shutil.rmtree(proj_dir)
    os.chdir(WORK_DIR)
    sh.arduinoproject(proj_name)
    os.chdir(HERE)
    if ino_file:
        shutil.copy(os.path.join(INO_DIR, ino_file), proj_dir)
    return proj_dir

def compile(proj_dir):
    os.chdir(proj_dir)
    sh.make()
    os.chdir(HERE)

def test_blank():
    """ blank project """
    d = mk_project("blank")
    compile(d)


