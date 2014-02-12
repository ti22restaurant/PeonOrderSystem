"""This module defines the MutableData
that is able to be updated or changed
on after creation.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from collections import Counter
from datetime import datetime as DateTime

from .abc.AuditData import AuditData


class MutableData(AuditData):
    """This class defines the MutuableData
    that can be changed after creation.
    """

    def __init__(self, name, new_datetime):
        """Initializes the MutableData.

        @param name: str representing the
        name associated with the data set.

        @param date: datetime.datetime
        associated with the data set.
        """
        self._check_datetime(new_datetime)
        self._name = name
        self._datetime = new_datetime

        self._data = []
        self._notification_data = []
        self._item_frequency = Counter()

        self._total = 0.0
        self._subtotal = 0.0
        self._tax = 0.0

        self._standard_orders = 0
        self._togo_orders = 0

        self._item_frequency = Counter()
        self._notification_data = []

    @staticmethod
    def _check_datetime(new_datetime):
        """Checks if the datetime is
        of the correct type.

        @param new_datetime: object
        to be checked.

        @return: bool value representing
        if the test was passed.
        """
        if not new_datetime or not isinstance(new_datetime, DateTime):
            raise TypeError('Cannot preform that operation without a valid '
                            'datetime. Expected datetime.datetime object '
                            'received {} instead'.format(type(new_datetime)))
        return True

    def update(self, update_data):
        """Updates the MutableData set.

        @param update_data: CollectionDataBundle
        subclass.

        @return: None
        """
        self._check_data(update_data)
        self.data += update_data.data
        self.total += update_data.total
        self.subtotal += update_data.subtotal
        self.tax += update_data.tax

        self.standard_orders += update_data.standard_orders
        self.togo_orders += update_data.togo_orders

        self.item_frequency += update_data.item_frequency
        self.notification_data += update_data.notification_data

    @property
    def data(self):
        """Gets the data associated
        with this data.

        @return: list of MenuItem objects.
        """
        return self._data

    @data.setter
    def data(self, new_data):
        """Sets the data associated
        with this data.

        @return: None
        """
        self._data = new_data

    @property
    def name(self):
        """Gets the name
        associated with the
        data.

        @return: str representing
        the name.
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name associated
        with the data.

        @param name: str representing
        the new name.

        @return: None
        """
        self._name = name

    @property
    def date(self):
        """Gets the datetime.date
        associated with the data.

        @return: datetime.date
        """
        return self._datetime.date()

    @date.setter
    def date(self, date):
        """Sets the datetime.date
        associated with the data.

        @param date: datetime.date
        to be stored as the new
        date.

        @return: None
        """
        self._datetime = DateTime.combine(date, self._datetime.time())

    @property
    def time(self):
        """Gets the time associated
        with the data.

        @return: datetime.time
        """
        return self._datetime.time()

    @time.setter
    def time(self, time):
        """Sets the time associated
        with the data.

        @param time: datetime.time
        representing the new time to
        associate with the data.

        @return: None
        """
        self._datetime = DateTime.combine(self._datetime.date(), time)

    @property
    def datetime(self):
        """Gets the datetime
        associated with the data.

        @return: datetime.datetime
        """
        return self._datetime

    @datetime.setter
    def datetime(self, new_datetime):
        """Sets the datetime associated
        with the data.

        @param new_datetime: datetime.datetime
        that represents the new datetime to
        associate with the data.

        @return: None
        """
        self._check_datetime(new_datetime)
        self._datetime = new_datetime

    @property
    def total(self):
        """Gets the total associated
        with the data.

        @return: float representing
        the total associated with
        the data.
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total associated
        with the data.

        @param total: float representing
        the new total to associate with
        the data.

        @return: None
        """
        self._total = total

    @property
    def subtotal(self):
        """Gets the subtotal associated
        with the data.

        @return: float representing the
        subtotal
        """
        return self._subtotal

    @subtotal.setter
    def subtotal(self, subtotal):
        """Sets the subtotal associated
        with the data.

        @param subtotal: float representing
        the subtotal to set.

        @return: None
        """
        self._subtotal = subtotal

    @property
    def tax(self):
        """Gets the tax associated
        with the data.

        @return: float representing
        the tax.
        """
        return self._tax

    @tax.setter
    def tax(self, tax):
        """Sets the tax associated
        with the data.

        @param tax: float representing
        the tax to be set.

        @return: None
        """
        self._tax = tax

    @property
    def standard_orders(self):
        """Gets the standard orders
        associated with the data.

        @return: int
        """
        return self._standard_orders

    @standard_orders.setter
    def standard_orders(self, orders):
        """Sets the standard orders
        associated with the data.

        @param orders: int representing
        the new standard orders to associate
        with the data.

        @return: None
        """
        self._standard_orders = orders

    @property
    def togo_orders(self):
        """Gets the togo orders associated
        with the data.

        @return: int representing the togo
        orders.
        """
        return self._togo_orders

    @togo_orders.setter
    def togo_orders(self, orders):
        """Sets the togo orders associated
        with the data.

        @param orders: int representing the
        togo orders to associate with the data.

        @return: None
        """
        self._togo_orders = orders

    @property
    def item_frequency(self):
        """Gets a Counter representing
        the item frequency associated
        with the data.

        @return: collections.Counter
        """
        return self._item_frequency

    @item_frequency.setter
    def item_frequency(self, data):
        """Sets the item frequency to
        the given counter.

        @param data: Counter that
        represents the item frequency.

        @return: None
        """
        self._item_frequency = data

    @property
    def notification_data(self):
        """Gets a list of MenuItems
        that represents the notification
        data associated with the data.

        @return: list of MenuItems
        """
        return self._notification_data

    @notification_data.setter
    def notification_data(self, data):
        """Sets the notification data.

        @param data: list of MenuItem
        objects that is to be stored as
        the notification data.

        @return: None
        """
        self._notification_data = data