"""This module provides the MenuComponent
which is used as a page for a notebook.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from gi.repository import Gtk

from .abc.Component import AbstractComponent
from .areas.abc.Area import AbstractArea


class MenuComponent(AbstractComponent):
    """Represents a notebook page. This
    component pulls areas and displays
    them in a single box that represents
    the page of a notebook.
    """

    def __init__(self, area_name):
        """Initializes the component.

        @param area_name: str representing
        the name to be associated with this
        component.
        """
        self._name = area_name
        self._widget = Gtk.VBox()

    @property
    def name(self):
        """Gets the name associated
        with this component.

        @return: str
        """
        return self._name

    @property
    def main_widget(self):
        """Gets the main widget
        that represents this component.

        @return: Gtk.Widget
        """
        return self._widget

    def add(self, area):
        """Adds an area to the
        component.

        @param area: AbstractArea
        subclass that represents
        the area to be added.

        @return: None
        """
        self._check_area(area)
        self._add_to_widget(area)

    def _add_to_widget(self, area):
        """Adds the widgets associated
        with the area to the widgets that
        are used in the display of this
        component.

        @param area: AbstractArea subclass
        that represents the area to be added.

        @return: None
        """
        area_widget = area.main_widget
        self._widget.pack_start(area_widget, True, True, 5.0)

    @staticmethod
    def _check_area(area):
        """Checks if the given area is
        a useable area.

        @raise TypeError: If the given
        area is null or is not a subclass
        member of AbstractArea.

        @param area: object representing
        the area to be tested.

        @return: bool value if the test
        was passed.
        """
        if not area or not isinstance(area, AbstractArea):
            raise TypeError("builder component cannot add an area that doesnt use "
                            "the AbstractArea as a base class!")
        return True