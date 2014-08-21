"""This module provides the
abstract base class for the
view.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractView(object):
    """Describes the functionality
    necessary for an object to be
    a useable view.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def main_widget(self):
        """Gets the main widget
        associated with the view.
        This is the widget to
        be used to display the view
        in the selected area.

        @return: Gtk.Widget
        """
        pass

    @abstractmethod
    def set_model(self, model):
        """Sets the model to
        associate the view with.

        @param model: Gtk.TreeModel
        to associate this view with.

        @return: None
        """
        pass

    @abstractmethod
    def get_selected(self):
        """Gets the iter and
        model pointing to the
        selected row.

        @return: tuple of
        (Gtk.TreeModel, Gtk.TreeIter)
        representing the data model
        and the iter pointing to the
        row respectively.
        """
        pass

    @abstractmethod
    def set_selected(self, itr):
        """Sets the selected row.

        @param itr: Gtk.TreeIter
        pointing to the row to be
        selected.

        @return: None
        """
        pass

    @abstractmethod
    def connect_signals(self, connect_ref):
        """Connects the signals of the views
        widgets to the given reference.

        @param connect_ref: obj that contains
        the necessary methods to be connected

        @return: None
        """
        pass