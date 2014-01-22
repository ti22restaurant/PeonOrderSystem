"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from abc import ABCMeta, abstractmethod


class PackageValue(object):
    """Abstract Base Class.

    Represents the PackageValue that
    determines how data is obtained
    from a PackagedData class.
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """Initializes the PackageValue"""
        pass

    @abstractmethod
    def get_data_value(self, packaged_data):
        """Gets the value associated with the
        packaged data.

        @param packaged_data: PackagedData object
        that is to have the value obtained.

        @return: value representing the value associated
        with the PackagedData
        """
        pass

    @abstractmethod
    def get_data_comparison_value(self, packaged_data):
        """Gets the comparison value for the given
        data.

        @return: value to be used for comparing
        the data.
        """
        pass


class OrdersTimePackageValue(PackageValue):
    """This class represents the PackageValue
    for orders given that they are organized
    by time as keys.
    """

    def get_data_value(self, packaged_data):
        """Gets the data value from the packaged
        data.

        @param packaged_data: PackagedData subclass
        that is to have its value calculated.

        @return: int representing the value associated
        with this PackagedData.
        """
        return 1

    def get_data_comparison_value(self, packaged_data):
        """Gets the basic comparison value for the packaged
        data.

        @param packaged_data: PackagedData subclass that
        represents the

        @return: datetime.time representing the time
        associated with the data.
        """
        return packaged_data.time


class ItemsTimePackageValue(PackageValue):
    """This class gets the PackageValue for
    items as long as they are organized by
    time keys.
    """

    def get_data_value(self, packaged_data):
        """Gets the data value from the packaged
        data.

        @param packaged_data: PackagedData subclass
        that is to have its value calculated.

        @return: int representing the value associated
        with this PackagedData.
        """
        return len(packaged_data)

    def get_data_comparison_value(self, packaged_data):
        """Gets the basic comparison value for the packaged
        data.

        @param packaged_data: PackagedData subclass that
        represents the

        @return: datetime.time representing the time
        associated with the data.
        """
        return packaged_data.time


class TotalsTimePackageValue(PackageValue):
    """This class gets the PackageValue for
    totals as long as they are organized by
    time keys.
    """

    def get_data_value(self, packaged_data):
        """Gets the data value from the packaged
        data.

        @param packaged_data: PackagedData subclass
        that is to have its value calculated.

        @return: int representing the value associated
        with this PackagedData.
        """
        return packaged_data.totals['total']

    def get_data_comparison_value(self, packaged_data):
        """Gets the basic comparison value for the packaged
        data.

        @param packaged_data: PackagedData subclass that
        represents the

        @return: datetime.time representing the time
        associated with the data.
        """
        return packaged_data.time