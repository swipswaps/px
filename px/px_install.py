import sys
import shutil

import os


def install(src, dest):
    """
    Copy src (file) into dest (file) and make dest executable.

    On trouble, prints message and exits with an error code.
    """
    try:
        _install(src, dest)
    except Exception as e:
        sys.stderr.write("Installing {} failed, please retry with sudo\n".format(dest))
        sys.stderr.write("Error was: {}\n".format(e.message))
        exit(1)
    print("Created: {}".format(dest))


def _install(src, dest):
    """
    Copy src (file) into dest (file) and make dest executable.

    Throws exception on trouble.
    """
    parent = os.path.dirname(dest)
    if not os.path.isdir(parent):
        raise IOError("ERROR: Destination parent is not a directory: %s\n" % parent)

    shutil.copyfile(src, dest)
    os.chmod(dest, 0755)