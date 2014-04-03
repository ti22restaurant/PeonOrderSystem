"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import datetime
import jsonpickle

from peonordersystem.src.Settings import SQLITE_DATE_TIME_FORMAT_STR
from .abc.CollectionDataBundle import CollectionDataBundle


class OrderDataBundle(CollectionDataBundle):
    """OrderDataBundle class is used to wrap a row that was returned
    from the respective database, allowing for an easier to access
    format.
    """

    def __init__(self, database_stored_data):
        """Packages the order data that is stored
        in the database in a easy to access format.

        @param database_stored_data: tuple representing
        the database columns that is to be interpreted
        and stored in this class.
        """
        super(OrderDataBundle, self).__init__()
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

        self._date = order_date
        self.data = jsonpickle.decode(unpacked_data_json)
        self.notification_data = jsonpickle.decode(unpacked_notification_json)
        self.item_frequency = jsonpickle.decode(unpacked_item_freq_json)
        self._name = unpacked_name
        self.order_number = unpacked_number
        self._totals = {'subtotal': unpacked_subtotal,
                       'tax': unpacked_tax,
                       'total': unpacked_total}

        self._is_standard = unpacked_type_is_standard
        self._is_togo = unpacked_type_is_togo

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
        with the OrderDataBundle

        @return: datetime.datetime object
        """
        return self._date

    @property
    def time(self):
        """Gets the time associated with the
        OrderDataBundle.

        @return: datetime.time object.
        """
        return self._date.time()

    @property
    def name(self):
        """Gets the name property

        @return: str representing
        the name associated with this
        OrderDataBundle
        """
        return self._name

    @property
    def total(self):
        """Gets the total associated
        with the OrderDataBundle.

        @return: float representing
        the total.
        """
        return self._totals['total']

    @property
    def subtotal(self):
        """Gets the subtotal associated
        with the OrderDataBundle

        @return: float representing
        the subtotal
        """
        return self._totals['subtotal']

    @property
    def tax(self):
        """Gets the tax associated with
        the OrderDataBundle.

        @return: float representing the
        tax.
        """
        return self._totals['tax']

    @property
    def togo_orders(self):
        """Gets the value representing
        if this OrderDataBundle is a togo
        order.

        @return: int representing if the
        OrderDataBundle is a togo order.
        """
        return self._is_togo

    @property
    def standard_orders(self):
        """Gets the value representing
        if this OrderDataBundle is a standard
        order.

        @return: int representing if the
        OrderDataBundle is a standard order.
        """
        return self._is_standard

    def __len__(self):
        """Get the length of the OrderDataBundle,
         by default is the number of MenuItems in the
         PackagedorderData.

        @return: int representing the number of
        MenuItems that this OrderDataBundle represents
        """
        return len(self.data)