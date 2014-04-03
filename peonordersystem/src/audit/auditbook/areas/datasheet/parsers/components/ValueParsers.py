"""This module defines parser objects that are used for
obtaining Values from PackagedData subclasses.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.ValueParser import ValueParser


class OrdersValueParser(ValueParser):
    """Defines behavior for parsing data
    and obtaining values associated with
    the number of orders in the given data.
    """
    def get_value(self, packaged_data):
        """Gets the data value from the packaged
        data.

        @param packaged_data: DataBundle subclass
        that is to have its value calculated.

        @return: int representing the value associated
        with this DataBundle.
        """
        return packaged_data.standard_orders + packaged_data.togo_orders


class ItemsValueParser(ValueParser):
    """Defines behavior for parsing data
    and obtaining values associated with
    the number of items in the given data.
    """

    def get_value(self, packaged_data):
        """Gets the data value from the packaged
        data.

        @param packaged_data: DataBundle subclass
        that is to have its value calculated.

        @return: int representing the value associated
        with this DataBundle.
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

        @param packaged_data: DataBundle subclass
        that is to have its value calculated.

        @return: int representing the value associated
        with this DataBundle.
        """
        return packaged_data.total