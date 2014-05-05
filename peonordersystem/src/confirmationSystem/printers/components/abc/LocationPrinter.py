"""This module defines the abstract
base class for the LocationPrinter

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod

from peonordersystem.src.confirmationSystem.printers.adapters.PrinterAdapter \
    import PrinterAdapter


class AbstractLocationPrinter(object):
    """Describes the basic functionality
    required for an object to the a
    LocationPrinter.
    """

    __metaclass__ = ABCMeta

    def __init__(self, printer_name):
        """Initializes the location printer
        with the given name.

        @param printer_name: str representing
        the name to be associated with the
        location printer.
        """
        self._printer = PrinterAdapter(printer_name)

    @abstractmethod
    def send_to_printer(self, file_path):
        """Sends the given data to
        the printer.

        @param file_path: str representing
        the file path to be printed.

        @return: bool value representing
        if the print was successful.
        """
        pass