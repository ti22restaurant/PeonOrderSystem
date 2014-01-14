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

        @return: datetime.date object
        """
        pass

    @property
    def datetime(self):
        """Abstract method. Gets the datetime property.

        @return: datetime.datetime object
        """
        return datetime.combine(self.date(), self.time())

    @abc.abstractproperty
    def time(self):
        """Abstract method. Gets the time property.

        @return: datetime.time object
        """
        pass

    @abc.abstractproperty
    def name(self):
        """Abstract Method.

        Gets the name property.

        @return: str representing the
        PackagedData's name.
        """
        pass

    def __eq__(self, other):
        """Compares this item to another
        item for equality.

        @param other: PackagedData subclass that
        represents the item to be compared to
        for equality.

        @return: bool value if the two items are
        the same PackagedData item.
        """
        return self.__dict__ == other.__dict__

    @abc.abstractmethod
    def __len__(self):
        """Abstract method.

        Gets the int associated with the PackagedData
        that represents a value of stored data.

        @return: int representing the associated value of
        stored data.
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
        return self._date.date()

    @property
    def datetime(self):
        """

        @return:
        """
        return None

    @property
    def time(self):
        """ Gets the time associated with this
        PackagedDateData.

        @return: datetime.time object
        """
        return None

    @property
    def name(self):
        """Gets the property name

        @return: str that represents
        the name associated with the
        PackagedDateData.
        """
        return 'Date: ' + str(self.date)

    def __len__(self):
        """Get the length of the PackagedDateData,
        by default this is number if indictative of
        how many orders are encompassed for this single
        date.

        @return: int representing the number of orders
        that this PackagedDateData represents.
        """
        num_standard_orders = len(self.num_of_order_types['standard'])
        num_togo_orders = len(self.num_of_order_types['togo'])
        return num_standard_orders + num_togo_orders


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
        self._name = unpacked_name
        self.order_number = unpacked_number
        self.totals = {'subtotal': unpacked_subtotal,
                       'tax': unpacked_tax,
                       'total': unpacked_total}
        self.order_type = order_type

    @property
    def date(self):
        """Getter method for abstract property
        date.

        @return: datetime.date object
        associated with this order.
        """
        return self._date.date()

    @property
    def datetime(self):
        """Gets the datetime associated
        with the PackagedOrderData

        @return: datetime.datetime object
        """
        return self._date

    @property
    def time(self):
        """Gets the time associated with the
        PackagedOrderData.

        @return: datetime.time object.
        """
        return self._date.time()

    @property
    def name(self):
        """Gets the name property

        @return: str representing
        the name associated with this
        PackagedOrderData
        """
        return self._name

    def __len__(self):
        """Get the length of the PackagedOrderData,
         by default is the number of MenuItems in the
         PackagedorderData.

        @return: int representing the number of
        MenuItems that this PackagedOrderData represents
        """
        return len(self.data)


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

        @return: datetime.date object that
        this item was ordered at.
        """
        return self._date.date()

    @property
    def datetime(self):
        """Gets the datetime associated
        with the PackagedItemData

        @return: datetime.datetime object
        """
        return self._date

    @property
    def time(self):
        """Gets the time associated with the
        PackagedItemData.

        @return: datetime.time object
        """
        return self._date.time()

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

    def __len__(self):
        """Gets the length of this PackagedItemData,
        by default this value is one representing
        how many items are represented here.

        @return: int representing the number of items
        this PackagedItemdata represents. By default
        value is 1.
        """
        return 1


