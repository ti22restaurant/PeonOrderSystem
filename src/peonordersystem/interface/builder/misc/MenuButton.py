"""This provides the MenuButton class

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from gi.repository import Gtk

from .abc.MenuButton import AbstractMenuButton


class MenuButton(AbstractMenuButton):
    """This class is used as to create
    and store a button associated with
    a MenuItem.
    """

    def __init__(self, menu_item):
        """Initializes the MenuButton.

        @param menu_item: MenuItem object
        that represents the MenuItem to
        be associated with the button.
        """
        self._data = menu_item
        self._widget = Gtk.Button(menu_item.get_name())
        self._set_widget_properties()

    def _set_widget_properties(self):
        """Sets the properties associated
        wtih the widget.

        @return: None
        """
        self._widget.set_focus_on_click(False)

    @property
    def main_widget(self):
        """Gets the associated
        widget.

        @return: Gtk.Widget
        """
        return self._widget

    @property
    def menu_item(self):
        """Gets the associated
        Menuitem

        @return: MenuItem
        """
        return self._data

    def connect(self, *args):
        """Connects the given
        arguments to the button
        widget.

        @param args: arguments to
        be passed to the widget.

        @return: None
        """
        self._widget.connect(*args)