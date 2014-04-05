"""This module defines the class that
is used to store and write header data
for a receipt.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import jsonpickle
from os.path import join
from datetime import datetime
from reportlab.platypus.frames import Frame
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (Paragraph, Image)

from peonordersystem.src.confirmationSystem.printers.formatters.PrinterSettings \
    import DEFAULT_FRONT_PRINTER_WIDTH
from peonordersystem.src.Settings import (RECEIPT_IMAGE_FILE_NAME,
                                          RECEIPT_IMAGE_HEIGHT,
                                          RECEIPT_IMAGE_WIDTH,
                                          RECEIPT_HEADER_TITLE_TEMPLATE_FILE_NAME,
                                          RECEIPT_HEADER_TITLE_CFG_FILE_NAME,
                                          RECEIPT_HEADER_TIMESTAMP_TEMPLATE_FILE_NAME,
                                          RECEIPT_HEADER_TIMESTAMP_CFG_TIME_FILE_NAME)

from peonordersystem.SystemPath import (SYSTEM_MEDIA_PATH,
                                        SYSTEM_TEMPLATE_RECEIPT_HEADER_PATH)

from .abc.Container import Container


class HeaderContainer(Container):
    """Defines the HeaderContainer
    that is used to generate, store
    and write receipt Headers.
    """
    DEFAULT_HEADER_HEIGHT = 250

    DEFAULT_STYLE = getSampleStyleSheet()['Normal']
    HEADER_IMAGE_PATH = join(SYSTEM_MEDIA_PATH, RECEIPT_IMAGE_FILE_NAME)

    def __init__(self, x, y, width=DEFAULT_FRONT_PRINTER_WIDTH):
        """Initializes the HeaderContainer.

        @param x: int representing the initial
        x value that the container frame should
        be written at.

        @param y: int representing the initial
        y value that the container frame should
        be written at.

        @keyword width: int representing the
        width of the header container. By default
        this value is equal to the width of
        the printer page.
        """
        self._area = (width, self.DEFAULT_HEADER_HEIGHT)
        self._start_point = (x, y)
        self._frame = Frame(x, y, width, self.DEFAULT_HEADER_HEIGHT)
        self._header = self._create_header()

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

    def _create_header(self):
        """Creates the header that represents
        the data this container will write in
        its frame.

        @return: list of reportlab.Flowable
        objects that represents the data to
        be written by the container.
        """
        container = []
        img = self._create_header_image()
        container.append(img)

        title = self._create_header_title()
        container.append(title)

        timestamp = self._create_header_timestamp()
        container.append(timestamp)

        return container

    def _create_header_image(self):
        """Creates the image for the
        header.

        @return: reportlab.platypus.Image
        that represents the image to be
        displayed.
        """
        return Image(self.HEADER_IMAGE_PATH,
                     width=RECEIPT_IMAGE_WIDTH,
                     height=RECEIPT_IMAGE_HEIGHT)

    def _create_header_title(self):
        """Creates the text that represents
        the title data for the header.

        @return: reportlab.platypus.Paragraph
        object that represents the text to be
        displayed.
        """
        rml_path = join(SYSTEM_TEMPLATE_RECEIPT_HEADER_PATH,
                        RECEIPT_HEADER_TITLE_TEMPLATE_FILE_NAME)
        cfg_path = join(SYSTEM_TEMPLATE_RECEIPT_HEADER_PATH,
                        RECEIPT_HEADER_TITLE_CFG_FILE_NAME)
        paragraph_text = self._format_rml_file(rml_path, cfg_path)
        return Paragraph(paragraph_text, self.DEFAULT_STYLE)

    def _create_header_timestamp(self):
        """Creates the timestamp that represents
        the timestamp data for the header.

        @return: reportlab.platypus.Paragraph
        object that represents the text to be
        displayed.
        """
        rml_path = join(SYSTEM_TEMPLATE_RECEIPT_HEADER_PATH,
                        RECEIPT_HEADER_TIMESTAMP_TEMPLATE_FILE_NAME)
        cfg_path = join(SYSTEM_TEMPLATE_RECEIPT_HEADER_PATH,
                        RECEIPT_HEADER_TIMESTAMP_CFG_TIME_FILE_NAME)
        cfg_data = self._get_cfg_data(cfg_path)
        rml_data = self._get_rml_data(rml_path)

        self._update_cfg_timestamp(cfg_data)

        paragraph_text = rml_data.format(**cfg_data)
        return Paragraph(paragraph_text, self.DEFAULT_STYLE)

    def _update_cfg_timestamp(self, cfg_data):
        """Updates the timestamp config data to
        display the current timestamp at the time
        of this headers creation.

        @param cfg_data: dict representing the
        config data for the timestamp.

        @return: dict representing the updated
        config data for the timestamp.
        """
        curr_datetime = datetime.now()
        cfg_data['DATE'] = curr_datetime.strftime(cfg_data['DATE'])
        cfg_data['TIME'] = curr_datetime.strftime(cfg_data['TIME'])
        return cfg_data

    def _format_rml_file(self, rml_file_path, cfg_file_path):
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
        with open(rml_file_path, 'r') as data_file:
            return data_file.read()

    def _get_cfg_data(self, cfg_file_path):
        """Gets the cfg data from the given
        cfg file path.

        @param cfg_file_path: str representing
        the file to be retrieved and parsed.

        @return: dict representing the formatting
        data stored in the config file.
        """
        with open(cfg_file_path, 'r') as data_file:
            data = data_file.read()
            return jsonpickle.decode(data)