"""Provides the the abstract base
class ReceiptContainer.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from json import loads

from reportlab.platypus.frames import Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Spacer

from .Container import Container

from peonordersystem.src.confirmationSystem.printers.formatters.PrinterSettings \
    import DEFAULT_FRONT_PRINTER_WIDTH


class ReceiptContainer(Container):
    """Describes the functionality required
    for an object to be a useable
    ReceiptContainer.
    """
    DEFAULT_WIDTH = DEFAULT_FRONT_PRINTER_WIDTH
    DEFAULT_STYLE = ParagraphStyle({'wordWrap': 1})
    CENTER_STYLE = ParagraphStyle({'wordWrap': 1, 'alignment': 'TA_CENTER'})

    TITLE_FORMAT = """
        <para size={size}>
            <b>{title}</b>
        </para>
    """
    TITLE_SIZE = 12

    SPACER_HEIGHT = 10
    SPACER_WIDTH = DEFAULT_WIDTH
    SPACER = Spacer(SPACER_WIDTH, SPACER_HEIGHT)

    SPACER_ARGS = [SPACER], SPACER_WIDTH, SPACER_HEIGHT

    def __init__(self):
        """Initializes the ReceiptContainer"""
        self._width = 0.0
        self._height = 0.0

        self._x = None
        self._y = None

        self._components = []

    @property
    def start_point(self):
        """Gets the point that
        represents the initial point
        for this container

        @return: 2 tuple of (float, float)
        representing the x and y coordinates
        that is the starting point of the
        area written.
        """
        return self._x, self._y

    @start_point.setter
    def start_point(self, coord):
        """Sets the point that
        represents the initial
        point for this container.

        @param coord: 2 tuple of
        (float, float) representing
        the x and y coordinates of
        where the container should
        be written on a cartesian
        plane.

        @return: None
        """
        self._x, self._y = coord

    @property
    def area(self):
        """Gets the values that
        represent the area of the
        container

        @return: 2 tuple of (int, int)
        representing the width and height
        of the frame respectively.
        """
        return self._width, self._height

    def add_component(self, component):
        """Adds the given component
        to the container.

        @param component: Component
        object to be added.

        @return: None
        """
        self.add_flowables(component.flowables,
                           component.width,
                           component.height)

    def add_flowables(self, flowables, width, height):
        """Adds the given list of flowables,
        with the specified width and height
        to the container.

        @param flowables: list of
        reportlab.platypus.flowable
        objects representing the displays
        to be added to the container.

        @param width: float representing
        the width associated with the
        widest flowable in the list.

        @param height: float representing
        the cumulative height of all flowables
        if they were to be placed consecutively
        without breaks.

        @return: None
        """
        self._components += flowables
        self._update_area(width, height)

    def _update_area(self, width, height):
        """Updates the area associated with
        the container.

        @param width: float representing
        the width that the area must be
        able to contain. The largest width
        given will be used.

        @param height: float representing
        the height that the area must be
        able to contain. The height will
        be the cumulative height of all
        displays.

        @return: None
        """
        self._width = max(self._width, width)
        self._height += height

    def write(self, canvas):
        """Writes the frame to the
        given canvas.

        @param canvas: reportlab.pdfgen.canvas.Canvas
        object that represents the canvas that the
        container should write the frame to.

        @return: None
        """
        self._check_canvas(canvas)
        self._check_start_point()

        frame = Frame(self._x, self._y, self._width, self._height,
                      topPadding=0, bottomPadding=0)
        frame.addFromList(self._components, canvas)

    def _check_start_point(self):
        """Checks if a valid start
        point has been specified.

        @throws ValueError: if no
        start point has been defined
        for this container.

        @return: bool value representing
        if the test was passed.
        """
        if self._x is None and self._y is None:
            raise ValueError("The start_point for the container has yet to be set!")
        return True

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