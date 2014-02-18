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

    @abstractmethod
    def get_menu_data(self):
        """Gets the stored menu data.

        @return: dict representing
        the menu data.
        """
        pass

    @abstractmethod
    def get_categories_data(self):
        """Gets the stored categories
        data.

        @return: dict representing the
        categories data.
        """
        pass

    @abstractmethod
    def get_options_data(self):
        """Gets the stored options
        data.

        @return: dict representing the
        options data
        """
        pass

    @abstractmethod
    def get_discount_templates_data(self):
        """Gets the stored discount templates
        data.

        @return: dict representing the stored
        discount templates data.
        """
        pass

    @abstractmethod
    def update_menu_data(self, updated_menu_data):
        """Updates the stored menu data.

        @param updated_menu_data: dict
        representing the updated data.

        @return: None
        """
        pass

    @abstractmethod
    def update_categories_data(self, updated_categories_data):
        """Updates the stored categories data.

        @param updated_categories_data: dict
        representing the updated categories
        data.

        @return: None
        """
        pass

    @abstractmethod
    def update_options_data(self, updated_options_data):
        """Updates the stored options data.

        @param updated_options_data: dict
        representing the updated options
        data.

        @return: None
        """
        pass

    @abstractmethod
    def update_discount_templates_data(self, updated_discount_templates):
        """Updates the stored discount
        templates data.

        @param updated_discount_templates: dict
        representing the updated discount templates
        data.

        @return: None
        """
        pass