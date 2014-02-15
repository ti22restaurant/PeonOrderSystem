"""This class holds the Abstract Base
Class used to define base functionality
for a ValueParser object.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class ValueParser(object):
    """ValueParser provides the
    methods to allow parsing given
    data to determine its associated
    value based on the time of parser
    instantiated.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """Initializes the parser"""
        pass

    @abstractmethod
    def get_value(self, packaged_data):
        """Gets the data value from the packaged
        data.

        @param packaged_data: DataBundle subclass
        that is to have its value collected.

        @return: value representing the value associated
        with the packaged data parsed based on specific
        class instance data.
        """
        pass