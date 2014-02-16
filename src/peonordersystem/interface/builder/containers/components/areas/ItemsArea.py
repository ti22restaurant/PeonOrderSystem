"""This module defines the ItemsArea
that is used to display data in a given
area comprised of MenuButtons.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from collections import deque
from gi.repository import Gtk

from .abc.Area import AbstractArea


class ItemsArea(AbstractArea):
    """An area used to hold and
    display MenuButtons.
    """

    def __init__(self, area_data, area_name, num_of_subareas=2,
                 has_title_area=False):
        """Initializes the ItemsArea.

        @param area_data: list of MenuButtons that represents
        the buttons to be displayed in this area.

        @param area_name: str representing the name to
        be associated with the area.

        @keyword num_of_subareas: int representing the number
        of sub areas that this area should be divided into.
        Each sub area is a column for the boxes, this number
        represents the number of columns to display the buttons
        data on. Default is 2.

        @keyword has_title_area: bool value representing if the
         title area should be displayed. Default is False.
        """
        self._title_flag = has_title_area
        self._num_subareas = num_of_subareas

        self._data = area_data
        self._name = area_name
        self._widget = self._set_up_main_area()

    @property
    def main_widget(self):
        """Gets the main widget
        associated with this area.

        @return: Gtk.Widget
        """
        return self._widget

    def _set_up_main_area(self):
        """Sets up the main area.

        @return: None
        """
        main_box = Gtk.VBox()
        title_area = self._set_up_title_area()
        main_box.pack_start(title_area, False, False, 5.0)
        buttons_area = self._set_up_button_area()
        main_box.pack_start(buttons_area, True, True, 5.0)
        return main_box

    def _set_up_title_area(self):
        """Sets up the title area.

        @return: None
        """
        if self._title_flag:
            return self._create_title_area()

    def _create_title_area(self):
        """Creates the title area.

        @return: None
        """
        sub_box = Gtk.VBox()
        label = Gtk.Label(self._name)
        sub_box.pack_start(label, True, True, 5.0)
        return sub_box

    def _set_up_button_area(self):
        """Sets up the button area.

        @return: None
        """
        sub_box = Gtk.HBox()
        boxes = self._create_button_boxes()

        for box in boxes:
            sub_box.pack_start(box, True, True, 5.0)

        return sub_box

    def _create_button_boxes(self):
        """Creates the button boxes that
        are used to store the buttons.

        @return: None
        """
        box_queue = self._create_button_subboxes()

        for item in self._data:
            box = box_queue.popleft()
            box.pack_start(item, True, True, 5.0)
            box_queue.append(box)

        return box_queue

    def _create_button_subboxes(self):
        """Creates the button subboxes that
        represent the number of columns
        that the buttons will be displayed
        in.

        @return: None
        """
        box_queue = deque()

        for x in range(self._num_subareas):
            box_queue.append(Gtk.VBox())

        return box_queue