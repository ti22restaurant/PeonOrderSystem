"""This module will define the required
functionality for the Builder class to
Build the initial UI.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractBuilder(object):
    """Describes the functionality necessary
    for a class to be a useable Builder in the
    UI.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def window(self):
        """Gets the window associated
        with the builder.

        @return: Gtk.Window
        """
        pass

    @abstractproperty
    def reservation_window(self):
        """Gets the reservation window
        used for displaying the reservations.

        @return: Gtk.Container
        """
        pass

    @abstractproperty
    def upcoming_orders_window(self):
        """Gets the orders window used for
        displaying the orders.

        @return: Gtk.Container
        """
        pass

    @abstractmethod
    def add_from_file(self, path, title):
        """Adds the builder data from the given
        path with the given title.

        @param path: str representing the path
        to the builder xml file.

        @param title: title representing the
        title associated with the builder.

        @return: None
        """
        pass

    @abstractmethod
    def connect_signals(self, connect_ref):
        """Connects the signals to the necessary
        method calls.

        @param connect_ref: reference representing
        the connection that will be used as the main
        connector for all parts of the UI

        @return: None
        """
        pass

    @abstractmethod
    def set_menu_item_view(self, display_view):
        """Sets the view used to display the
        MenuItems.

        @param display_view: Gtk.TreeView that
        will be used to display the menu items

        @return: None
        """
        pass

    @abstractmethod
    def set_table(self, table_value):
        """Sets the currently displayed
        table.

        @param table_value: str representing
        the str to display as the selected
        table.

        @return: None
        """
        pass

    @abstractmethod
    def update_status(self, status_msg, styles=[]):
        """Updates the main status
        message with the given str.

        @param status_msg: str representing
        the status.

        @keyword styles: list representing the
        styles to apply to the status.

        @return: None
        """
        pass
