"""This module defines the
abstract base class of observer
that will be subclassed by all
observers.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AbstractObserver(object):
    """Describes the required functionality
    for an object to be an observer.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def notify(self, data):
        """Notifies the observer
        of the given data.

        @param data: values that
        the observer subscribed
        for.

        @return: None
        """
        pass
