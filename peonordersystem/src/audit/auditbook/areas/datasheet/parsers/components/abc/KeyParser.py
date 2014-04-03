"""This module stores the Abstract Base
Class used to define the base functionality
for a KeyParser object.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class KeyParser(object):
    """KeyParser object represents
    the object that is used to parse
    DataBundle and retrieve a key
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
        with the given DataBundle.

        @param packaged_data: DataBundle subclass
        object that represents the data to have its
        key value retrieved.

        @return: value representing the key value
        associated with the DataBundle
        """
        pass