"""This module defines the outward
facing printer class that are
interacted with to format and print
data.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .adapters.abc.AbstractDataAdapter import AbstractDataAdapter

from .formatters.FrontFormatter import FrontFormatter
from .formatters.KitchenFormatter import KitchenFormatter

from .components.FrontPrinter import FrontPrinter
from .components.KitchenPrinter import KitchenPrinter

from .abc.AbstractPrinter import AbstractPrinter


class Printer(AbstractPrinter):
    """Provides outward facing
    object that is to be interacted
    with to both format and print
    data.
    """

    def __init__(self):
        """Initializes the printer"""
        self._front_printer = FrontPrinter()
        self._front_formatter = FrontFormatter()

        self._kitchen_formatter = KitchenFormatter()
        self._kitchen_printer = KitchenPrinter()

    def print_to_front(self, data):
        """Prints the given data to the
        front.

        @param data: DataAdapter class
        that represents the data to be
        formatted and printed.

        @return: bool value representing
        if the job succeeded or not.
        """
        self._check_data_type(data)
        self._front_formatter.format_data(data)
        file_path = self._front_formatter.file_path
        return self._front_printer.send_to_printer(file_path)

    def print_to_kitchen(self, data):
        """Prints the given data to the
        kitchen.

        @param data: DataAdapter class
        that represents the data to be
        formatted and printed.

        @return: bool value representing
        if the job succeeded or not.
        """
        self._check_data_type(data)
        self._kitchen_formatter.format_data(data)
        file_path = self._kitchen_formatter.file_path
        return self._kitchen_printer.send_to_printer(file_path)

    def _check_data_type(self, data):
        """Checks if the given data
        is of the AbstractDataAdapter
        type.

        @param data: object to be tested.

        @raise TypeError: if the object
        given is not an instance of
        AbstractDataAdapter.

        @return: bool value representing
        if the test was passed or not.
        """
        if not isinstance(data, AbstractDataAdapter):
            raise TypeError("Cannot format and print data unless it is an instance "
                            "of AbstractDataAdapter!")
        return True