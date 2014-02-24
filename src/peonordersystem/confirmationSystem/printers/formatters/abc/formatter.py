"""This module defines the abstract
base class for the formatter.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AbstractFormatter(object):
    """

    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def format_data(self, data):
        """Formats the given data
        into a standard printable
        format.

        @param data: list of MenuItem
        objects that represents the
        data to be printed.

        @return: str representing the
        data parsed into the respective
        format.
        """
        pass