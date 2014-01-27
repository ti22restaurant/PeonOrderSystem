"""This module defines the abstract
base class DataBundle that is the
main superclass for all data bundle
objects.

All abstract items are guaranteed to
be included.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import datetime
from abc import ABCMeta, abstractproperty, abstractmethod


class DataBundle(object):
    """DataBundle represents the abstract base class
    that must be instantiated for any type of data to be
    utilized as a packaged data type.
    """
    __metaclass__ = ABCMeta

    @abstractproperty
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

    @abstractproperty
    def time(self):
        """Abstract method. Gets the time property.

        @return: datetime.time object
        """
        pass

    @abstractproperty
    def name(self):
        """Abstract Method.

        Gets the name property.

        @return: str representing the
        DataBundle's name.
        """
        pass

    def __eq__(self, other):
        """Compares this item to another
        item for equality.

        @param other: DataBundle subclass that
        represents the item to be compared to
        for equality.

        @return: bool value if the two items are
        the same DataBundle item.
        """
        return self.__dict__ == other.__dict__

    def __cmp__(self, other):
        """Compares this item to another
        item for ordering. This is done in
        reference to the date stored in these
        items.

        @param other: DataBundle subclass that
        represents the item to be compared to
        this item.

        @return: int representing the relationship
        between this object and the compared object.
        """
        if self.date == other.date:
            return cmp(self.datetime, other.datetime)
        return cmp(self.date, other.date)

    @abstractmethod
    def __len__(self):
        """Abstract method.

        Gets the int associated with the DataBundle
        that represents a value of stored data.

        @return: int representing the associated value of
        stored data.
        """
        pass