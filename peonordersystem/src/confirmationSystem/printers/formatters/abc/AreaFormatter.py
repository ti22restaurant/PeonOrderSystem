"""This module provides
the abstract base class
that defines the AreaFormatter
class.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from reportlab.pdfgen.canvas import Canvas

from abc import ABCMeta, abstractproperty, abstractmethod

from .Formatter import AbstractFormatter


class AreaFormatter(AbstractFormatter):
    """Implements the base functionality
    shared by all AreaFormatter subclasses.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """Initializes the formatter"""
        self._x = None
        self._y = None
        self._displays = None

    @abstractproperty
    def file_path(self):
        """Gets the file path
        that the formatter saves
        the formatted file to

        @return: str representing
        the path to the formatted
        file
        """
        pass

    @property
    def required_keys(self):
        """Gets a set of keys
        that are required for
        the formatter to perform
        its formatting operation.

        @return: Set of str values
        representing the required
        data keys.
        """
        return set()

    @property
    def area(self):
        """Gets the area of the
        formatted file as a 2 tuple
        representing the width and
        height respectively.

        @return: 2 tuple (float, float)
        representing the width and height
        of the area.
        """
        return self._x, self._y

    @property
    def available_coord(self):
        """Gets the next available
        coord that a display container
        could be added to.

        @return: 2 tuple(float, float)
        representing the next useable
        coordinate that a display
        container can be added to.
        """
        return 0.0, self._y

    def _clear_state(self):
        """Clears the state of
        any previous format. Allowing
        for another format to take
        place.

        @return: None
        """
        self._displays = []
        self._x = 0.0
        self._y = 0.0

    def format_data(self, data):
        """Formats the given data
        into a file.

        @param data: dict that contains
        the necessary keys defined by
        required_keys property.

        @return: str representing the
        path to the file formatted with
        the given data.
        """
        self._clear_state()
        self._check_keys(data)
        self.generate_display_areas(data)
        self._create_file()
        self._clear_state()
        return self.file_path

    @abstractmethod
    def generate_display_areas(self, data):
        """Generates the display areas.
        This method is passed the data to
        be formatted and should add display
        containers.

        @param data: dict that contains the
        necessary keys and values for the
        display areas to be generated.

        @return: None
        """
        pass

    def add_display(self, display):
        """Adds the given display container
        to the file.

        @param display: Container object
        representing the displays to be
        contained within the file.

        @return: None
        """
        self._configure_display(display)
        self._displays.append(display)
        self._update_area_space(*display.area)

    def _configure_display(self, display):
        """Configures the start point of
        the display to be at the next
        available location.

        @param display: Container object
        to be configured and have its
        starting point defined.

        @return: None
        """
        display.start_point = self.available_coord

    def _update_area_space(self, width, height):
        """Updates the area space
        that represents the area of
        the file.

        @param width: float representing
        the width to be updated. The width
        will be updated only if it exceeds
        previously required widths.

        @param height: float representing
        the height to be updated. The height
        will be updated for every item added.

        @return: None
        """
        self._x = max(self._x, width)
        self._y += height

    def _check_keys(self, data):
        """Checks if the required keys
        are contained within the given
        data.

        @param data: dict of str keys
        mapped to values.

        @throws KeyError: If the required
        keys were not contained within the
        given data dict

        @return: bool value representing if
        the test was passed.
        """
        if not self.required_keys.issubset(data):
            raise KeyError("Expected keys were not present in data!")
        return True

    def _create_file(self):
        """Creates the file and
        inserts the given display
        containers into the file.

        @return: None
        """
        x, y = self.area
        canvas = Canvas(self.file_path, pagesize=(x, y))

        for display in self._displays:
            display.write(canvas)
        canvas.save()