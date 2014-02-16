"""This module defines the base
class for the MenuButton.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractproperty, abstractmethod


class AbstractMenuButton(object):
    """Describes the required functionality
    for an object to be a useable MenuButton.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def main_widget(self):
        """Gets the main widget
        associated with the MenuButton.

        @return: Gtk.Widget
        """
        pass

    @abstractproperty
    def menu_item(self):
        """Gets the associated
        MenuItem

        @return: MenuItem
        """
        pass

    @abstractmethod
    def connect(self, *args):
        """Connects the signals
        of the button.

        @param args: arguments
        to be passed to the connect
        function of the widget.

        @return: None
        """
        pass
