"""This module defines the DataAdapter

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.AbstractDataAdapter import AbstractDataAdapter


class DataAdapter(AbstractDataAdapter):
    """Encapsulates the data so that it
    may be operated on by the printers in
    this module group.
    """

    def __init__(self, data):
        """Initializes the adapter.

        @param data: dict of str to
        value pairs representing the
        data to be stored. Required
        key value pairs are:

            'number'            :   int representing the data number.

            'name'              :   str representing the data name.

            'total'             :   float representing the data total

            'subtotal'          :   float representing the data subtotal

            'tax'               :   float representing the data tax

            'priority_order'    :   list of MenuItem objects representing
                                    the priority order associated with this
                                    data

            'order'             :   list of MenuItem objects representing
                                    the non-priority order associated with
                                    this data.
        """
        self._number = data['number']
        self._name = data['name']

        self._totals = {
            'total':    data['total'],
            'subtotal': data['subtotal'],
            'tax':      data['tax']
        }

        self._priority_order = tuple(data['priority_order'])
        self._order = tuple(data['order'])

    @property
    def order_number(self):
        """Gets the order number
        associated with the data.

        @return: int
        """
        return self._number

    @property
    def order_name(self):
        """Gets the order name
        associated with this
        data.

        @return: str
        """
        return self._name

    @property
    def totals(self):
        """Gets a dict representing
        the totals associated with
        this data. Key value pairs
        are:

            'total'     :   float representing data total

            'subtotal'  :   float representing data subtotal

            'tax'       :   float representing data tax

        @return: dict
        """
        return self._totals

    @property
    def priority_order(self):
        """Gets a tuple of MenuItem
        objects representing the
        priority order associated
        with this data.

        @return: tuple of MenuItems
        """
        return self._priority_order

    @property
    def order(self):
        """Gets a tuple of MenuItem
        objects representing the
        order associated with this
        data.

        @return: tuple of MenuItems
        """
        return self._order