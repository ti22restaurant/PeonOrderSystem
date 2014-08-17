"""This module defines the abstract base
class for View objects

@author: Carl McGraw
@contact: cjmcgraw(- at -)u.washington.edu
@version: 1.x
"""
from abc import ABCMeta, abstractmethod


class View(object):
    """Describes the required functionality
    for an object to be a valid View object
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def set_mapper(self, mapper):
        """Sets the stored mapper used
        by the view to the given mapper

        @param mapper: SignalMapper
        """
        pass

    @abstractmethod
    def run(self):
        """Runs the main dialog
        window.

        @return: Gtk.ResponseType
        """
        pass