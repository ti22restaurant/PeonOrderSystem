"""This module provides the
abstract base class that is used
as an adapter for the modules to
access the printer.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AbstractPrinterAdapter(object):
    """Describes the basic functionality
    for the an object to be a useable
    PrinterAdapter.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def print_data(self, printer_str, data_file_str, title_str, options):
        """Prints the data.

        @param printer_str: str representing the printer
        to be printed to.

        @param data_file_str: str representing the file
        name of the data to be printed.

        @param title_str: str representing the title
        that the job should be associated with.

        @param options: dict of options that represent
        the options associated with the printing job.

        @return: bool value representing if the
        system received the job.
        """
        pass
