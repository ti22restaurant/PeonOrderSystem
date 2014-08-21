"""This module defines the DisplayComponent
abstract class

@author: Carl McGraw
@contact: cjmcgraw(- at -)u.washington.edu
@version: 1.x
"""
from abc import ABCMeta, abstractmethod, abstractproperty

from .AbstractComponent import AbstractComponent


class DisplayComponent(AbstractComponent):
    """Describes the required functionality
    for a class to be a DisplayComponent
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_selected(self):
        """Gets the iter pointing
        to the selected row.

        @return: Gtk.TreeIter
        """
        pass

    @abstractmethod
    def set_selected(self, itr):
        """Sets the selected row to
        the row the iter is pointing
        to.

        @param itr: Gtk.TreeIter
        """
        pass

    @abstractmethod
    def set_selection_func(self, func, *args):
        """

        @param args:
        @return:
        """
        pass