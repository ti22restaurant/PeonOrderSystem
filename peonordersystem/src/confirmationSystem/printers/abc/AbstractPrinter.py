"""This module provides the abstract
base class for printers.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AbstractPrinter(object):
    """Describes the necessary functionality
    for an object to be a useable printer.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def print_to_kitchen(self, data):
        """Prints the given data to the
        kitchen.

        @param data: list of MenuItem
        objects that represents the order
        to be sent to the kitchen.

        @return: bool value representing
        if the print was successful.
        """
        pass

    @abstractmethod
    def print_to_front(self, data):
        """Prints the given data to
        the front.

        @param data: list of MenuItem
        objects that represents the order
        to be sent to the front.

        @return: bool value representing
        if the print was successful
        """
        pass