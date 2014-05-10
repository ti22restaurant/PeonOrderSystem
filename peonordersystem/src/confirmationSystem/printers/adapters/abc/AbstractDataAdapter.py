"""This module defines the
abstract base class that is
used to define the DataAdapter.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractproperty


class AbstractDataAdapter(object):
    """Describes the required functionality
    for an object to be a useable DataAdapter.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def order_number(self):
        """Gets the order number
        associated with the data.

        @return: int
        """
        pass

    @abstractproperty
    def order_name(self):
        """Gets the order name
        associated with the data.

        @return: str
        """
        pass

    @abstractproperty
    def totals(self):
        """Gets a dict representing
        the str keys to totals float
        values.

            'total'     :   float value representing
                            the total of all items associated
                            with this data.

            'subtotal'  :   float value representing the subtotal
                            of all items associated with this data.

            'tax'       :   float value representing the tax of all
                            items associated with this data.

        @return: dict
        """
        pass

    @abstractproperty
    def priority_order(self):
        """Gets a list of items
        representing the priority
        order associated with the
        data.

        @return: list of MenuItems
        """
        pass

    @property
    def has_priority(self):
        """Gets if the data has
        a valid priority list.

        @return: bool value
        representing if the
        priority list is non
        empty.
        """
        return len(self.priority_order) != 0

    @abstractproperty
    def order(self):
        """Gets a list of items
        representing the order
        associated with this data.

        @return: list of MenuItems
        """
        pass

    @property
    def has_order(self):
        """Gets if the order has
        a valid order list.

        @return: bool value
        representing if the
        order list is non empty.
        """
        return len(self.order) != 0
