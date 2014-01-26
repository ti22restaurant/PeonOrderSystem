"""This module represents the generic DataParser
that is used to parse general data and retrieve
value and key comparisons.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from abc import ABCMeta, abstractmethod


class DataParser(object):
    """Abstract Base Class.

    Represents the DataParser that
    determines how data is obtained
    from a PackagedData class.
    """

    __metaclass__ = ABCMeta

    def __init__(self, key_parser, value_parser):
        """Initializes the DataParser"""
        self._key_parser = key_parser
        self._value_parser = value_parser

    def get_data_value(self, data):
        """Gets the value associated with the
        packaged data.

        @param data: object that is to have
        the value obtained.

        @return: value representing the value associated
        with the data
        """
        return self._value_parser.get_value(data)

    def get_data_comparison_value(self, data):
        """Gets the comparison value for the given
        data.

        @param data: object that is to have its
        comparison value obtained.

        @return: value to be used for comparing
        the data.
        """
        return self._key_parser.get_key(data)
