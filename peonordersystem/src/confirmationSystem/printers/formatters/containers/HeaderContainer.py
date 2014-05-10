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
                                          RECEIPT_COMPONENT_TITLE_TEMPLATE_FILE_NAME,
                                          RECEIPT_COMPONENT_TITLE_CFG_FILE_NAME,
                                          RECEIPT_COMPONENT_TIMESTAMP_TEMPLATE_FILE_NAME,
                                          RECEIPT_COMPONENT_TIMESTAMP_CFG_TIME_FILE_NAME)

from peonordersystem.SystemPath import (SYSTEM_MEDIA_PATH,
                                        SYSTEM_TEMPLATE_RECEIPT_HEADER_PATH)

from .abc.ReceiptContainer import ReceiptContainer


class TicketHeaderContainer(ReceiptContainer):
    """Defines the TicketHeaderContainer
    that is used to format the header at
    the top of the ticket
    """
    CFG_DATE_KEY = 'DATE'
    CFG_TIME_KEY = 'TIME'
    CFG_NAME_KEY = 'NAME'

    SIZE_KEY = 'SIZE'

    def __init__(self, data):
        """Initializes the header.

        @param data: DataAdapter object
        representing the data to be formatted
        into this header.
        """
        super(TicketHeaderContainer, self).__init__()
        self._name = data.order_name
        self._number = data.order_number
        self._size = 0.0
        self._rows = 0

        self._create_components()

    def _create_components(self):
        """Creates the components for
        display.

        @return: None
        """
        timestamp = self._create_component_timestamp()

        width = DEFAULT_FRONT_PRINTER_WIDTH
        height = self._size * self._rows

        self.add_flowables([timestamp], width, height)
        self.add_flowables(*self.SPACER_ARGS)
        self.add_flowables(*self.SPACER_ARGS)
        self.add_flowables(*self.SPACER_ARGS)

    def _create_component_timestamp(self):
        """Creates the timestamp that represents
        the timestamp data for the component

        @return: reportlab.platypus.Paragraph
        object that represents the text to be
        displayed.
        """
        rml_path = join(SYSTEM_TEMPLATE_RECEIPT_HEADER_PATH,
                        RECEIPT_COMPONENT_TIMESTAMP_TEMPLATE_FILE_NAME)
        cfg_path = join(SYSTEM_TEMPLATE_RECEIPT_HEADER_PATH,
                        RECEIPT_COMPONENT_TIMESTAMP_CFG_TIME_FILE_NAME)
        cfg_data = self._get_cfg_data(cfg_path)
        rml_data = self._get_rml_data(rml_path)

        self._alter_state(cfg_data)

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

        cfg_data[self.CFG_NAME_KEY] = self._name

        return cfg_data

    def _alter_state(self, data):
        """Alters the stored state in the
        header with the given data.

        @param data: DataAdapter that holds
        the necessary data.

        @return: None
        """
        self._size = data[self.SIZE_KEY]
        self._rows = len(data) + 2


class HeaderContainer(TicketHeaderContainer):
    """Defines the HeaderContainer
    that is used to generate, store
    and write receipt Headers.
    """
    # Determined experimentally
    DEFAULT_HEADER_HEIGHT = 174
    HEADER_IMAGE_PATH = join(SYSTEM_MEDIA_PATH, RECEIPT_IMAGE_FILE_NAME)

    def _create_components(self):
        """Creates the header that represents
        the data this container will write in
        its frame.

        @return: list of reportlab.Flowable
        objects that represents the data to
        be written by the container.
        """
        flowables = []

        img = self._create_component_image()
        flowables.append(img)

        title = self._create_component_title()
        flowables.append(title)

        timestamp = self._create_component_timestamp()
        flowables.append(timestamp)

        width = DEFAULT_FRONT_PRINTER_WIDTH
        height = self.DEFAULT_HEADER_HEIGHT

        self.add_flowables(flowables, width, height)

    def _create_component_image(self):
        """Creates the image for the
        component.

        @return: reportlab.platypus.Image
        that represents the image to be
        displayed.
        """
        return Image(self.HEADER_IMAGE_PATH,
                     width=RECEIPT_IMAGE_WIDTH,
                     height=RECEIPT_IMAGE_HEIGHT)

    def _create_component_title(self):
        """Creates the text that represents
        the title data for the component.

        @return: reportlab.platypus.Paragraph
        object that represents the text to be
        displayed.
        """
        rml_path = join(SYSTEM_TEMPLATE_RECEIPT_HEADER_PATH,
                        RECEIPT_COMPONENT_TITLE_TEMPLATE_FILE_NAME)
        cfg_path = join(SYSTEM_TEMPLATE_RECEIPT_HEADER_PATH,
                        RECEIPT_COMPONENT_TITLE_CFG_FILE_NAME)
        paragraph_text = self.format_rml_file(rml_path, cfg_path)
        return Paragraph(paragraph_text, self.DEFAULT_STYLE)

