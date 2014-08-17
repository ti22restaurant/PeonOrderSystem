"""This module defines the abstract class
TreeViewComponent

@author: Carl McGraw
@contact: cjmcgraw(- at -)u.washington.edu
@version: 1.x
"""
from abc import ABCMeta, abstractmethod

from .DisplayComponent import DisplayComponent


class TreeViewComponent(DisplayComponent):
    """Describes the basic functionality
    necessary for a class to be a
    TreeViewComponent
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def set_columns(self, columns):
        """Sets the tree views colums.

        @param columns: list of
        Gtk.TreeViewColumns
        """
        pass

    @abstractmethod
    def set_model(self, model):
        """Sets the model associated
        with the tree view

        @param model: Gtk.Treemodel
        """
        pass