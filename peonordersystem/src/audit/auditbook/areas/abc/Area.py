"""This module defines the abstract
base class of Area that is used to as
the base for all Areas that may be added
to Worksheets.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod

from peonordersystem.src.audit.adapters.spreadsheetWriter.XLWorksheet \
    import XLWorksheet


class Area(object):
    """Abstract Base Class for
    the areas. Supplies Connect
    function that is used to add
    the area to a worksheet.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self, worksheet):
        pass

    @staticmethod
    def _check_worksheet(worksheet, message=None):
        """Checks that the given data is a valid
        worksheet subclass.

        @param worksheet: data to be tested if it
        is a Worksheet instance or subclass.

        @param message: str representing the message
        to display in-lieu of the default message.

        @return: bool value representing if the
        test was passed.
        """
        if not worksheet or not isinstance(worksheet, XLWorksheet):
            if message:
                msg = message
            else:
                msg = 'Cannot perform this operation without a valid XLWorksheet.'
            raise TypeError(msg)
        return True
