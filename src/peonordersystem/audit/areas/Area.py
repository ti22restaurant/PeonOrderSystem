"""This module defines the abstract
base class of Area that is used to as
the base for all Areas that may be added
to Worksheets.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class Area(object):
    """Abstract Base Class for
    the areas. Supplies Connect
    function that is used to add
    the area to a worksheet.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self, worksheet, format_data, row, col):
        pass
