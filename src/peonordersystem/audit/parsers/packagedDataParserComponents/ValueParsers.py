"""This module defines parser objects that are used for
obtaining Values from PackagedData subclasses.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from abc import ABCMeta, abstractmethod


class ValueParser(object):
    """ValueParser provides the
    methods to allow parsing given
    data to determine its associated
    value based on the time of parser
    instantiated.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """Initializes the parser"""
        pass

    @abstractmethod
    def get_value(self, packaged_data):
        """Gets the data value from the packaged
        data.

        @param packaged_data: PackagedData subclass
        that is to have its value collected.

        @return: value representing the value associated
        with the packaged data parsed based on specific
        class instance data.
        """
        pass


class OrdersValueParser(ValueParser):
    """Defines behavior for parsing data
    and obtaining values associated with
    the number of orders in the given data.
    """
    def get_value(self, packaged_data):
        """Gets the data value from the packaged
        data.

        @param packaged_data: PackagedData subclass
        that is to have its value calculated.

        @return: int representing the value associated
        with this PackagedData.
        """
        return 1


class ItemsValueParser(ValueParser):
    """Defines behavior for parsing data
    and obtaining values associated with
    the number of items in the given data.
    """

    def get_value(self, packaged_data):
        """Gets the data value from the packaged
        data.

        @param packaged_data: PackagedData subclass
        that is to have its value calculated.

        @return: int representing the value associated
        with this PackagedData.
        """
        return len(packaged_data)


class TotalsValueParser(ValueParser):
    """Defines behavior for parsing
    data and obtaining values associated
    with the total of the given data.
    """

    def get_value(self, packaged_data):
        """Gets the data value from the packaged
        data.

        @param packaged_data: PackagedData subclass
        that is to have its value calculated.

        @return: int representing the value associated
        with this PackagedData.
        """
        return packaged_data.totals['total']