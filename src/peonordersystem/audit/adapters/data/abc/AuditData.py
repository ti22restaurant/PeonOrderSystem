"""This module defines the abstract
base class that all AuditData objects
needs to extend to be useable in the
audit system.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractproperty

from src.peonordersystem.confirmationSystem.bundlers.abc.CollectionDataBundle \
    import CollectionDataBundle


class AuditData(CollectionDataBundle):
    """This class defines the
    Abstract Base Class that is
    used to define the audit data's
    methods.
    """

    __metaclass__ = ABCMeta

    @staticmethod
    def _check_data(data):
        """Checks that the given data matches
        the requirements to be used.

        @raise TypeError: If the given data is
        not a subclass type of CollectionDataBundle.

        @return: bool value representing if the
        test was passed.
        """
        if not data or not isinstance(data, CollectionDataBundle):
            raise TypeError('Adapter cannot operate with the given data. The '
                            'data must be a subclass type of CollectionDataBundle '
                            'got {} instead'.format(type(data)))
        return True

    @abstractproperty
    def data(self):
        """Gets the stored
        MenuItem data in the
        data.

        @return: list of MenuItems
        """
        pass

    @abstractproperty
    def name(self):
        """Gets the name of
        the data.

        @return: str
        """
        pass

    @abstractproperty
    def date(self):
        """datetime.date representing
        the date associated with the
        data.

        @return: datetime.date
        """
        pass

    @abstractproperty
    def time(self):
        """datetime.time representing
        the time associated with the
        data.

        @return: datetime.time
        """
        pass

    @abstractproperty
    def datetime(self):
        """datetime.datetime representing
        the date and time associated with
        the data.

        @return: datetime.datetime
        """
        pass

    @abstractproperty
    def total(self):
        """Gets the total associated
        with the data.

        @return: float
        """
        pass

    @abstractproperty
    def tax(self):
        """Gets the tax associated
        with the data.

        @return: float
        """
        pass

    @abstractproperty
    def subtotal(self):
        """Gets the subtotal associated
        with the data.

        @return: float
        """
        pass

    @abstractproperty
    def togo_orders(self):
        """Gets the value representing
        the number of orders made togo.

        @return: int
        """
        pass

    @abstractproperty
    def standard_orders(self):
        """Gets the value representing
        the number of standard orders.

        @return: int
        """
        pass

    @abstractproperty
    def item_frequency(self):
        """Gets a Counter representing
        the item frequency associated
        with the data.

        @return: collections.Counter
        """
        pass

    @abstractproperty
    def notification_data(self):
        """Gets a list of MenuItems
        that represents the notification
        data associated with the data.

        @return: list of MenuItems
        """
        pass

    def __len__(self):
        """Gets the length
        associated with the data.

        @return: int
        """
        return self.standard_orders + self.togo_orders