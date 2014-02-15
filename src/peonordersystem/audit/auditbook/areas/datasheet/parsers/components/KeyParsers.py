"""This module defines parser objects that are
used in obtaining key data from PackagedData
subclass objects.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.KeyParser import KeyParser


class TimeKeyParser(KeyParser):
    """TimeKeyParser represents the object
    that is used to parse DataBundle and
    retrieve the associated time value.
    """

    def get_key(self, packaged_data):
        """Gets the time key value stored
        in the given packaged data.

        @param packaged_data: DataBundle
        subclass that represents the data
        stored.

        @return: datetime.time that represents
        the time associated with the data.
        """
        return packaged_data.time


class DateKeyParser(KeyParser):
    """DateKeyParser represents the object
    that is used to parse DataBundle and
    retrieve the associated date value.
    """

    def get_key(self, packaged_data):
        """Gets the date key value stored
        in the given packaged data

        @param packaged_data: DataBundle
        subclass that represents the data
        stored.

        @return: datetime.date that represents
        the date associated with the data.
        """
        return packaged_data.date


