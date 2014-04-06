"""Provides the the abstract base
class ReceiptContainer.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from json import loads
from abc import ABCMeta, abstractmethod

from reportlab.platypus.frames import Frame
from reportlab.lib.styles import getSampleStyleSheet

from .Container import Container


class ReceiptContainer(Container):
    """Describes the functionality required
    for an object to be a useable
    ReceiptContainer.
    """

    __metaclass__ = ABCMeta

    DEFAULT_STYLE = getSampleStyleSheet()['Normal']

    def __init__(self, x, y, width, height):
        """Initializes the ReceiptContainer.

        @param x: int representing the initial
        x value that the container frame should
        be written at.

        @param y: int representing the initial
        y value that the container frame should
        be written at

        @param width: int representing the width
        of the header container. This is also the
        x coordinate representing its area.

        @param height: int representing the height
        of the header container. This is also the
        y coordinate representing its area.
        """
        self._area = (width, height)
        self._start_point = (x, y)
        self._frame = Frame(x, y, width, height)
        self._header = self.create_header()

    @abstractmethod
    def create_header(self):
        """Creates the header that represents
        the data this container will write in
        its frame.

        @return: list of reportlab.Flowable
        objects that represents the data to
        be written by the container.
        """
        pass

    @property
    def start_point(self):
        """Gets the point that
        represents the initial point
        for this frame.

        @return: 2 tuple of (int, int)
        representing the x and y coordinates
        that is the starting point of the
        area written.
        """
        return self._start_point

    @property
    def area(self):
        """Gets the values that
        represent the area of the
        frame.

        @return: 2 tuple of (int, int)
        representing the width and height
        of the frame respectively.
        """
        return self._area

    def write(self, canvas):
        """Writes the frame to the
        given canvas.

        @param canvas: reportlab.pdfgen.canvas.Canvas
        object that represents the canvas that the
        container should write the frame to.

        @return: None
        """
        self._check_canvas(canvas)
        self._frame.addFromList(self._header, canvas)

    def format_rml_file(self, rml_file_path, cfg_file_path):
        """Formats the rml file at the given path
        with the data from the given config file
        path.

        @param rml_file_path: str representing the
        path to the rml file to be formatted.

        @param cfg_file_path: str representing the
        path to the cfg file to be accessed for the
        format data.

        @return: str representing the formatted rml
        file.
        """
        data = self._get_rml_data(rml_file_path)
        frmt = self._get_cfg_data(cfg_file_path)
        return data.format(**frmt)

    def _get_rml_data(self, rml_file_path):
        """Gets the rml data from the given
        rml file path.

        @param rml_file_path: str representing
        the file to be retrieved.

        @return: str representing the data contained
        within the given rml file path location.
        """
        with open(rml_file_path, 'r') as rml_file:
            return rml_file.read()

    def _get_cfg_data(self, cfg_file_path):
        """Gets the cfg data from the given
        cfg file path.

        @param cfg_file_path: str representing
        the file to be retrieved and parsed.

        @return: dict representing the formatting
        data stored in the config file.
        """
        with open(cfg_file_path, 'r') as cfg_file:
            cfg_json_data = cfg_file.read()
            return loads(cfg_json_data)