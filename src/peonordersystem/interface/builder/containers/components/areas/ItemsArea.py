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

    DEFAULT_NUM_OF_SUB_AREAS = 2
    ITEMS_PER_AREA = 3

    def __init__(self, area_data, area_name,has_title_area=True):
        """Initializes the ItemsArea.

        @param area_data: list of MenuButtons that represents
        the buttons to be displayed in this area.

        @param area_name: str representing the name to
        be associated with the area.

        @keyword has_title_area: bool value representing if the
         title area should be displayed. Default is False.
        """
        self._title_flag = has_title_area
        self._data = area_data
        self._name = area_name

        self._num_subareas = self._get_number_of_sub_areas()
        self._widget = self._set_up_main_area()

    @property
    def main_widget(self):
        """Gets the main widget
        associated with this area.

        @return: Gtk.Widget
        """
        return self._widget

    def _get_number_of_sub_areas(self):
        """Gets the number of sub areas that
        should be displayed in this items area.

        @return: int representing the number
        of sub areas.
        """
        n = len(self._data) / self.ITEMS_PER_AREA
        return max(n, self.DEFAULT_NUM_OF_SUB_AREAS)

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
        return Gtk.VBox()

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