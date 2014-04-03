"""This module defines the abstract
base class for the LocationPrinter

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AbstractLocationPrinter(object):
    """Describes the basic functionality
    required for an object to the a
    LocationPrinter.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def send_to_printer(self, data):
        """Sends the given data to
        the printer.

        @param data: str data to be
        sent to the printer.

        @return: bool value representing
        if the print was successful.
        """
        pass