"""This module provides classes that are utilized in parsing and storing the
necessary data that can be obtained via database. Each constructor of the
PackagedData classes takes a tuple represented as a row of their respective
databases.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""

import datetime
import jsonpickle

from src.peonordersystem.Settings import (SQLITE_DATE_TIME_FORMAT_STR,
                                          SQLITE_DATE_FORMAT_STR)


class PackagedDateData(object):

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

        curr_date = datetime.datetime.strptime(unpacked_date, SQLITE_DATE_FORMAT_STR)
        self.date = curr_date.date()
        self.num_of_order_types = {'standard': unpacked_num_of_orders_standard,
                                   'togo': unpacked_num_of_orders_togo}

        self.totals = {'subtotal': unpacked_subtotal,
                       'tax': unpacked_tax,
                       'total': unpacked_total}

    def __eq__(self, other):
        """Compares two PackagedDateData objects
        for equality. Two objects are equal when
        their dicts match.

        @param other: PackagedDateData object
        that is to be compared.

        @return: bool representing equality.
        """
        return self.__dict__ == other.__dict__


class PackagedOrderData(object):

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

        self.order_date = order_date
        self.order_data = jsonpickle.decode(unpacked_data_json)
        self.notification_data = jsonpickle.decode(unpacked_notification_json)
        self.item_frequency = jsonpickle.decode(unpacked_item_freq_json)
        self.order_name = unpacked_name
        self.order_number = unpacked_number
        self.order_totals = {'subtotal': unpacked_subtotal,
                             'tax': unpacked_tax,
                             'total': unpacked_total}
        self.order_type = order_type

    def __eq__(self, other):
        """Compares two PackagedOrderData objects
        for equality. Two objects are equal when
        their dicts match.

        @param other: PackagedOrderData object
        that is to be compared.

        @return: bool representing equality.
        """
        return self.__dict__ == other.__dict__


class PackagedItemData(object):

    def __init__(self, database_stored_data):
        """

        @param database_stored_data:
        @return:
        """
        (OrderNumber,
         ItemName,
         ItemDate,
         ItemIsNotification,
         ItemData_json) = database_stored_data

        self.menu_item = jsonpickle.decode(ItemData_json)
        self.order_number = OrderNumber
        self.date = ItemDate
        self.name = property(self.menu_item.get_name)
        self.is_notification = property(self.menu_item.is_notification)

    def __eq__(self, other):
        """Compares two PackagedItemData objects
        for equality. Two objects are equal when
        their dicts match.

        @param other: PackagedItemData object
        that is to be compared.

        @return: bool representing equality.
        """
        return self.__dict__ == other.__dict__


