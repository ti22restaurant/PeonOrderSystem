"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import datetime
import jsonpickle
from peonordersystem.Settings import SQLITE_DATE_TIME_FORMAT_STR
from peonordersystem.confirmationSystem.bundlers.abc.DataBundle import DataBundle


class ItemDataBundle(DataBundle):
    """ItemDataBundle class is used to wrap the database columns
    data into an easier to use format.

    @var data: MenuItem object associated with the item

    @var number: int representing the order number
    under which this item was called.

    @var name: str representing the name of this MenuItem
    object.

    @var is_notification: bool value representing of the MenuItem
    was a notification item.

    @group DataBundle: subclass member of packaged
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
        with the ItemDataBundle

        @return: datetime.datetime object
        """
        return self._date

    @property
    def time(self):
        """Gets the time associated with the
        ItemDataBundle.

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
        """Gets the length of this ItemDataBundle,
        by default this value is one representing
        how many items are represented here.

        @return: int representing the number of items
        this PackagedItemdata represents. By default
        value is 1.
        """
        return 1