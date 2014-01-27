"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import datetime
from peonordersystem.Settings import SQLITE_DATE_FORMAT_STR
from peonordersystem.confirmationSystem.bundlers.abc.CollectionDataBundle import \
    CollectionDataBundle


class DateDataBundle(CollectionDataBundle):
    """DateDataBundle is used to wrap a date database row in an
    easy to use format.
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
        DateDataBundle.

        @return: datetime.time object
        """
        return None

    @property
    def name(self):
        """Gets the property name

        @return: str that represents
        the name associated with the
        DateDataBundle.
        """
        return 'Date: ' + str(self.date)

    @property
    def togo_orders(self):
        """Gets the number of togo orders
        in this DateDataBundle.

        @return: int representing the
        number of togo orders.
        """
        return self.num_of_order_types['togo']

    @property
    def standard_orders(self):
        """Gets the number of standard
        orders in this DateDataBundle.

        @return: int representing the
        number of standard orders.
        """
        return self.num_of_order_types['standard']

    def __len__(self):
        """Get the length of the DateDataBundle,
        by default this is number if indictative of
        how many orders are encompassed for this single
        date.

        @return: int representing the number of orders
        that this DateDataBundle represents.
        """
        num_standard_orders = len(self.num_of_order_types['standard'])
        num_togo_orders = len(self.num_of_order_types['togo'])
        return num_standard_orders + num_togo_orders