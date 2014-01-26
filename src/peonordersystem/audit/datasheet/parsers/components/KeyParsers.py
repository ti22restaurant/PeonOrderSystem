"""This module defines parser objects that are
used in obtaining key data from PackagedData
subclass objects.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from abc import ABCMeta, abstractmethod


class KeyParser(object):
    """KeyParser object represents
    the object that is used to parse
    PackagedData and retrieve a key
    value associated with the data.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """Initializes the KeyParser object"""
        pass

    @abstractmethod
    def get_key(self, packaged_data):
        """Abstract Method.

        Gets the key value stored associated
        with the given PackagedData.

        @param packaged_data: PackagedData subclass
        object that represents the data to have its
        key value retrieved.

        @return: value representing the key value
        associated with the PackagedData
        """
        pass


class TimeKeyParser(KeyParser):
    """TimeKeyParser represents the object
    that is used to parse PackagedData and
    retrieve the associated time value.
    """

    def get_key(self, packaged_data):
        """Gets the time key value stored
        in the given packaged data.

        @param packaged_data: PackagedData
        subclass that represents the data
        stored.

        @return: datetime.time that represents
        the time associated with the data.
        """
        return packaged_data.time


class DateKeyParser(KeyParser):
    """DateKeyParser represents the object
    that is used to parse PackagedData and
    retrieve the associated date value.
    """

    def get_key(self, packaged_data):
        """Gets the date key value stored
        in the given packaged data

        @param packaged_data: PackagedData
        subclass that represents the data
        stored.

        @return: datetime.date that represents
        the date associated with the data.
        """
        return packaged_data.date


