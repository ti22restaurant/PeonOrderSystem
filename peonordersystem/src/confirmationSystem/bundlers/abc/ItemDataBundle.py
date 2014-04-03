"""This module defines an abstract base
class that is used as a superclass for
all concrete ItemDataBundle subclasses.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod

from .DataBundle import DataBundle


class ItemDataBundle(DataBundle):
    """Abstract Base Class.

    Base class that defines the necessary
    functionality for the ItemDataBundle
    concrete classes.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def is_notification(self):
        """Gets whether the associated
        item is a notification item or
        not.

        @return: bool value representing
        if the associated item is a notification
        item.
        """
        pass