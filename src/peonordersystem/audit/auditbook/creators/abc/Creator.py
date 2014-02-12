"""This module defines the abstract base
class creator.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class Creator(object):
    """Describes the necessary
    methods for a class to be
    a useable creator.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, data):
        """Updates the data
        associated with the
        creator.

        @param data: data to
        be updated.

        @return: None
        """
        pass

    @abstractmethod
    def finalize(self):
        """Finalizes the creator

        @return: None
        """
        pass
