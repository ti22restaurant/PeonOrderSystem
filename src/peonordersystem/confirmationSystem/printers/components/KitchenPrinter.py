"""This module provides the KitchenPrinter
class that allows for data to be sent to
the kitchen printer.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from LocationPrinter import LocationPrinter


class KitchenPrinter(LocationPrinter):
    """Provides the functionality for
    sending data to kitchen printer.
    """

    KITCHEN_PRINTER_NAME = "KITCHEN_PRINTER"

    def __init__(self):
        """Initializes the printer"""
        super(KitchenPrinter, self).__init__(self.KITCHEN_PRINTER_NAME)

    def _get_title(self):
        """Gets the title data associated
        with the data to be sent to the
        kitchen.

        @return: str
        """
        title = super(KitchenPrinter, self)._get_title()
        return 'Kitchen ' + title

