"""This module provides the class
that allows for printing to a given
printer name representing the location.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from datetime import datetime

from .confirmationSystem.printers.components.abc.LocationPrinter import AbstractLocationPrinter
from src.peonordersystem.confirmationSystem.printers.adapters.PrinterAdapter \
    import PrinterAdapter


class LocationPrinter(AbstractLocationPrinter):
    """Provides the functionality for
    sending printer data to the a specified
    location.
    """

    def __init__(self, printer_name):
        """Initializes the printer that
        prints to the given name.

        @param printer_name: str representing
        the printer name to be printed to.
        """
        self._printer = PrinterAdapter(printer_name)
        self._order_counter = 0

    def send_to_printer(self, data):
        """Sends the data to the printer
        for printing.

        @param data: str representing
        the file name to be printed.

        @return: bool value representing
        if the printer job was successfully
        passed to the printer.
        """
        title = self._get_title()
        options = self._get_options()

        self._order_counter += 1
        return self._printer.print_data(data, title, options)

    def _get_title(self):
        """Gets the title for the
        printer job.

        @return: str representing
        the title.
        """
        title = 'Order# {} at {}'
        order_date = datetime.now()
        return title.format(self._order_counter, order_date)

    def _get_options(self):
        """Gets the options associated
        with the printer job.

        @return: dict representing
        the associated options.
        """
        return {}