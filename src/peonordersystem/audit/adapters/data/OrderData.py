"""This module defines OrderData
areas that are used for storing and
performing audits in the audit system.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.AuditData import AuditData


class OrderData(AuditData):
    """Represents a wrapper for
    data to be passed into the
    audit.
    """

    def __init__(self, data):
        """Initializes the OrderData object.

        @param data: CollectionDataBundle
        subclass that represents the data
        to be stored and audited.
        """
        self._check_data(data)
        self._data = data

    @property
    def data(self):
        """Gets the data associated
        with the data.

        @return: list of MenuItems
        """
        return self._data.data

    @property
    def name(self):
        """Gets the name of
        the data.

        @return: str
        """
        return self._data.name

    @property
    def date(self):
        """datetime.date representing
        the date associated with the
        data.

        @return: datetime.date
        """
        return self._data.date

    @property
    def time(self):
        """datetime.time representing
        the time associated with the
        data.

        @return: datetime.time
        """
        return self._data.time

    @property
    def datetime(self):
        """datetime.datetime representing
        the date and time associated with
        the data.

        @return: datetime.datetime
        """
        return self._data.datetime

    @property
    def total(self):
        """Gets the total associated
        with the data.

        @return: float
        """
        return self._data.total

    @property
    def subtotal(self):
        """Gets the subtotal associated
        with the data.

        @return: float
        """
        return self._data.subtotal

    @property
    def tax(self):
        """Gets the tax associated
        with the data.

        @return: float
        """
        return self._data.tax

    @property
    def togo_orders(self):
        """Gets the value representing
        the number of orders made togo.

        @return: int
        """
        return self._data.togo_orders

    @property
    def standard_orders(self):
        """Gets the value representing
        the number of standard orders.

        @return: int
        """
        return self._data.standard_orders

    @property
    def item_frequency(self):
        """Gets a Counter representing
        the item frequency associated
        with the data.

        @return: collections.Counter
        """
        return self._data.item_frequency

    @property
    def notification_data(self):
        """Gets a list of MenuItems
        that represents the notification
        data associated with the data.

        @return: list of MenuItems
        """
        return self._data.notification_data