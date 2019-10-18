import sys
import os
from os.path import getmtime

WATCHED_FILES = ["lib/morgue_parser.py", __file__]
WATCHED_FILES_MTIMES = [(f, getmtime(f)) for f in WATCHED_FILES]


def watch_for_changes():
    for f, mtime in WATCHED_FILES_MTIMES:
        if getmtime(f) != mtime:
            print("\n\033[33;1mRestarting!!!\033[0m")
            os.execv(sys.executable, ["python"] + sys.argv)
