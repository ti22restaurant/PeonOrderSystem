"""This module defines the Abstract Base Class
Updater that updates the components.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class Updater(object):
    """This class defines the
    base functionality required to
    be an Updater class.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, *args):
        """Abstract Method.

        Updates the class.
        """
        pass
