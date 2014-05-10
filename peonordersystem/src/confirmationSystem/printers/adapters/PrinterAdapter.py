"""This module provides the adapter
that wraps printer functionality
and allows the printer to be
accessed through the abstract
methods print_data.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from cups import Connection

from .abc.AbstractPrinterAdapter import AbstractPrinterAdapter


class PrinterAdapter(AbstractPrinterAdapter):
    """Provides the basic functionality of wrapping
    the printer and allowing data to be printed.
    """

    def __init__(self, printer_name):
        """Initializes the adapter"""
        self._printer_name = printer_name
        self._connection = Connection()

    def print_data(self, data_file_str, title_str, options):
        """Prints the given data with the given
        information.

        @param data_file_str: str representing the
        file to be printed.

        @param title_str: str representing the title
        that the printer job should be associated
        with.

        @param options: dict of options that the
        should be associated with the printer job.

        @return: bool value representing if the
        printer was successful in scheduling the
        job.
        """
        value = self._connection.printFile(self._printer_name, data_file_str,
                                           title_str, options)
        return value > 0
