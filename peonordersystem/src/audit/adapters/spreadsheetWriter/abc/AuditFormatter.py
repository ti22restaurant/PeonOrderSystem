"""This module defines the abstract base
class that acts as an a grouper for the
AuditFormat adapters.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AuditFormatter(object):
    """Describes the base functionality
    required for an object to be considered
    and AuditFormatter.
    """

    __metaclass__ = ABCMeta


    @abstractmethod
    def __getitem__(self, key):
        """Gets the item associated
        with the given key.

        @param key: str representing
        the key of the format to get.

        @return: XLFormat object that
        represents the format.
        """
        pass
