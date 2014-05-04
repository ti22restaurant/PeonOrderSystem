"""This module defines the abstract
base class for Generators.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod, abstractproperty
from reportlab.pdfgen.canvas import Canvas


class Container(object):
    """Describes the required functionality
    for an object to be a useable Frame.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def area(self):
        """Gets the area taken up
        by the Frame as a point.

        @return: 2 tuple of (float, float)
        representing the x and y area taken
        up by the frame respectively.
        """
        pass

    # This is an abstract property. Unable to declare
    # as such though because of the setter!
    @property
    def start_point(self):
        """Gets the starting
        point of this container.

        @return: 2 tuple of (float, float)
        representing the x and y area where
        this frame begins on a cartesian
        plane.
        """
        return None

    @start_point.setter
    def start_point(self, coord):
        """Sets the starting
        point for the container.

        @param coord: 2 tuple of
        (float, float) representing
        the x and y area where the
        container begins on a cartesian
        plane.

        @return: None
        """
        pass

    @abstractmethod
    def write(self, canvas):
        """Writes the stored frame
        data to the given canvas.

        @param canvas: reportlab.pdfgen.canvas.Canvas
        class that represents the canvas to
        be written to.

        @return: None
        """
        pass

    def _check_canvas(self, canvas):
        """Checks whether the given canvas
        is a valid reportlab.pdfgen.canvas.Canvas.

        @param canvas: object to be tested.

        @return: bool value representing if
        the given canvas is a
        reportlab.pdfgen.canvas.Canvas
        """
        return isinstance(canvas, Canvas)