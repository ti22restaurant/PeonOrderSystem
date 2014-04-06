"""This module defines the class that
is used to store and write header data
for a receipt.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from os.path import join
from datetime import datetime
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

from .abc.ReceiptContainer import ReceiptContainer


class HeaderContainer(ReceiptContainer):
    """Defines the HeaderContainer
    that is used to generate, store
    and write receipt Headers.
    """
    CFG_DATE_KEY = 'DATE'
    CFG_TIME_KEY = 'TIME'

    DEFAULT_HEADER_HEIGHT = 250
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
        super(HeaderContainer, self).__init__(x, y, width,
                                              self.DEFAULT_HEADER_HEIGHT)

    def create_header(self):
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
        paragraph_text = self.format_rml_file(rml_path, cfg_path)
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

        date_str = curr_datetime.strftime(cfg_data[self.CFG_DATE_KEY])
        cfg_data[self.CFG_DATE_KEY] = date_str

        time_str = curr_datetime.strftime(cfg_data[self.CFG_TIME_KEY])
        cfg_data[self.CFG_TIME_KEY] = time_str
        return cfg_data