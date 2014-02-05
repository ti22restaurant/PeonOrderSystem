"""This module defines the abstract base
class for Grouper objects.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from abc import ABCMeta, abstractmethod


class Grouper(object):
    """Abstract Base Class that
    defines how the Grouper subclasses
    will be interacted with.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_key_index(self, value):
        """Gets the key index associated
        with the given value.

        @param value: object that represents
        some value to be grouped with the
        expected keys.
        """
        pass
