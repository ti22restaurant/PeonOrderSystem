#!/usr/bin/python
"""main module that runs the PeonOrderSystem"""
import sys
from os import path

cwd = path.dirname(path.realpath(__file__))
PROJECT_PATH = path.split(cwd)[0]
sys.path.append(PROJECT_PATH)

from peonordersystem.src.PeonOrderSystem import PeonOrderSystem
from gi.repository.Gtk import MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION

REQUIRED_MIN_VERSION = (3, 4, 2)
FOUND_VERSION = MAJOR_VERSION, MINOR_VERSION, MICRO_VERSION


def _check_gtk_version(found_version, req_version):
    """Checks the current Gtk version.

    @param found_version: tuple of ints representing
    the version number that was found.

    @param req_version: tuple of ints representing
    the version number required.

    @raise: ImportError if the given version does not
    match the required version.

    @return: None
    """
    if found_version < req_version:
        data = {
            'req_version': '.'.join([str(x) for x in req_version]),
            'found_version': '.'.join([str(x) for x in found_version])
        }

        raise ImportError("""
            Gtk+ version {req_version} or greater required.\n
            Gtk+ version {found_version} found.\n
            """.format(**data))

_check_gtk_version(FOUND_VERSION, REQUIRED_MIN_VERSION)

PoS = PeonOrderSystem()
PoS.run()
