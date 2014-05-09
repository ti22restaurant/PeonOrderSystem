"""This module provides the class
that allows for printing to the front
area.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from peonordersystem.src.Settings import FRONT_PRINTER_NAME

from .LocationPrinter import LocationPrinter


class FrontPrinter(LocationPrinter):
    """Provides the functionality for
    sending printer data to the front
    area.
    """

    def __init__(self):
        """Initializes the printer"""
        super(FrontPrinter, self).__init__(FRONT_PRINTER_NAME)