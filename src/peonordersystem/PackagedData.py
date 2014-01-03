"""This module provides classes that are utilized in parsing and storing the
necessary data that can be obtained via database. Each constructor of the
PackagedData classes takes a tuple represented as a row of their respective
databases.

@group PackagedData: PackagedData group represents the classes that subclass
the PackagedData class. These classes are unified under a specific abstract
class which implements certain properties that must be defined for their
usage.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""

import abc
import datetime
import jsonpickle

from src.peonordersystem.Settings import (SQLITE_DATE_TIME_FORMAT_STR,
                                          SQLITE_DATE_FORMAT_STR)


class PackagedData(object):
    """PackagedData represents the abstract base class
    that must be instantiated for any type of data to be
    utilized as a packaged data type.

    This requires defining the abstract property of date
    for access.

    @var date: datetime.datetime object representing the
    datetime associated with the PackagedData.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractproperty
    def date(self):
        """Abstract method. Gets the date property.

        @return: None
        """
        pass


class PackagedDateData(PackagedData):
    """PackagedDateData is used to wrap a date database row in an
    easy to use format.

    @var totals: dict that maps str keys representing the
        {
            'subtotal'  :   order subtotal,
            'tax'       :   order tax,
            'total'     :   order total
        }

    @var num_of_order_types: dict that maps str keys
    representing the types of orders for that date

        {
            'standard' : num of standard orders,
            'togo'     : num of togo orders
        }

    @group PackagedData: subclass member of packaged
    data as such they are expected to have:

        @var date: datetime.date object that represents
        the date associated with the data.

    """

    def __init__(self, database_stored_data):
        """Packages the date data that is stored
        in the database in an easy to access format.

        @param database_stored_data: tuple representing
        the database columns that is to be interpreted
        and stored in this class.
        """
        (unpacked_date,
         unpacked_num_of_orders_standard,
         unpacked_num_of_orders_togo,
         unpacked_subtotal,
         unpacked_tax,
         unpacked_total) = database_stored_data

        self.num_of_order_types = {'standard': unpacked_num_of_orders_standard,
                                   'togo': unpacked_num_of_orders_togo}

        self.totals = {'subtotal': unpacked_subtotal,
                       'tax': unpacked_tax,
                       'total': unpacked_total}

        curr_date = datetime.datetime.strptime(unpacked_date, SQLITE_DATE_FORMAT_STR)
        self._date = curr_date.date()

    @property
    def date(self):
        """Getter for the property date.

        @return: datetime.date object
        that represents the date associated
        with this date.
        """
        return self._date

    def __eq__(self, other):
        """Compares two PackagedDateData objects
        for equality. Two objects are equal when
        their dicts match.

        @param other: PackagedDateData object
        that is to be compared.

        @return: bool representing equality.
        """
        return self.__dict__ == other.__dict__


class PackagedOrderData(PackagedData):
    """PackagedOrderData class is used to wrap a row that was returned
    from the respective database, allowing for an easier to access
    format.

    @var data: list of MenuItem objects that represent the
    order.

    @var name: str representing the orders name

    @var order_number: int representing the order number of
    this order.

    @var order_type: str representing the type of order.

    @var totals: dict that maps str keys representing the

        {
            'subtotal'  :   order subtotal,
            'tax'       :   order tax,
            'total'     :   order total
        }

    @var notification_data: list of MenuItem object that
    represent the associated notification items.

    @var item_frequency: Counter representing the number
    of MenuItem objects, by name, there were called for this
    order.

    @group PackagedData: subclass member of packaged
    data as such they are expected to have:

        @var date: datetime.date object that represents
        the date associated with the data.
    """

    def __init__(self, database_stored_data):
        """Packages the order data that is stored
        in the database in a easy to access format.

        @param database_stored_data: tuple representing
        the database columns that is to be interpreted
        and stored in this class.
        """
        (unpacked_number,
        unpacked_date,
        unpacked_name,
        unpacked_subtotal,
        unpacked_tax,
        unpacked_total,
        unpacked_has_notifications,
        unpacked_notification_json,
        unpacked_item_freq_json,
        unpacked_type_is_standard,
        unpacked_type_is_togo,
        unpacked_data_json) = database_stored_data

        order_date = datetime.datetime.strptime(unpacked_date,
                                                SQLITE_DATE_TIME_FORMAT_STR)

        if unpacked_type_is_standard:
            order_type = 'standard'
        else:
            order_type = 'togo'
        self._date = order_date
        self.data = jsonpickle.decode(unpacked_data_json)
        self.notification_data = jsonpickle.decode(unpacked_notification_json)
        self.item_frequency = jsonpickle.decode(unpacked_item_freq_json)
        self.name = unpacked_name
        self.order_number = unpacked_number
        self.totals = {'subtotal': unpacked_subtotal,
                       'tax': unpacked_tax,
                       'total': unpacked_total}
        self.order_type = order_type

    @property
    def date(self):
        """Getter method for abstract property
        date.

        @return: datetime.datetime object
        associated with this order.
        """
        return self._date

    def __eq__(self, other):
        """Compares two PackagedOrderData objects
        for equality. Two objects are equal when
        their dicts match.

        @param other: PackagedOrderData object
        that is to be compared.

        @return: bool representing equality.
        """
        return self.__dict__ == other.__dict__


class PackagedItemData(PackagedData):
    """PackagedItemData class is used to wrap the database columns
    data into an easier to use format.

    @var data: MenuItem object associated with the item

    @var number: int representing the order number
    under which this item was called.

    @var name: str representing the name of this MenuItem
    object.

    @var is_notification: bool value representing of the MenuItem
    was a notification item.

    @group PackagedData: subclass member of packaged
    data as such they are expected to have:

        @var date: datetime.date object that represents
        the date associated with the data.
    """

    def __init__(self, database_stored_data):
        """Packages the item data that is stored in
        a database row into an easier to operate format.

        @param database_stored_data: tuple representing
        the columns associated with the database.
        """
        (OrderNumber,
         ItemName,
         ItemDate,
         ItemIsNotification,
         ItemData_json) = database_stored_data

        self._date = datetime.datetime.strptime(ItemDate, SQLITE_DATE_TIME_FORMAT_STR)
        self.data = jsonpickle.decode(ItemData_json)
        self.order_number = OrderNumber

    @property
    def date(self):
        """Getter that gets the date associated
        with the MenuItem

        @return: datetime.datetime object that
        this item was ordered at.
        """
        return self._date

    @property
    def name(self):
        """Getter that gets the name associated
        with the MenuItem

        @return: str representing the MenuItems
        name.
        """
        return self.data.get_name()

    @property
    def is_notification(self):
        """Getter that gets the notification
        boolean value associated with the stored
        MenuItem.

        @return: bool representing if this
        item data represented here is a notification
        item.
        """
        return self.data.is_notification()

    def __eq__(self, other):
        """Compares two PackagedItemData objects
        for equality. Two objects are equal when
        their dicts match.

        @param other: PackagedItemData object
        that is to be compared.

        @return: bool representing equality.
        """
        return self.__dict__ == other.__dict__


