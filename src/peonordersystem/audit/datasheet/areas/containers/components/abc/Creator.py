"""This module defines the abstract base
class for the Creator.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class Creator(object):
    """Creator generates data to be
    stored and displayed. Thus the
    creator defines a get data format
    for displaying the created data.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data_format(self, format_data):
        """Gets the format data to display"""
        pass
