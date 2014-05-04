"""This module defines the
FrontFormatter class that is
used to format order data into
a printable file that represents
the front receipt.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from os.path import join

from peonordersystem.SystemPath import SYSTEM_TEMP_PATH
from peonordersystem.src.Settings import FRONT_RECEIPT_FILE_NAME

from .containers.HeaderContainer import HeaderContainer
from .containers.MainContainer import MainContainer
from .containers.FooterContainer import FooterContainer

from .abc.AreaFormatter import AreaFormatter


class FrontFormatter(AreaFormatter):
    """Formats given order data into a
    printable file representing a receipt
    for the "front" area to be displayed
    to customers
    """
    DEFAULT_FILE = join(SYSTEM_TEMP_PATH, FRONT_RECEIPT_FILE_NAME)

    REQUIRED_KEYS = {'order', 'number', 'total', 'subtotal', 'tax'}

    @property
    def file_path(self):
        """Gets the file path
        that the formatter uses
        for storing generated
        files.

        @return: str representing
        the file path.
        """
        return self.DEFAULT_FILE

    @property
    def required_keys(self):
        """

        @return:
        """
        return self.REQUIRED_KEYS

    def generate_display_areas(self, data):
        """Generates the areas for display
        from the given data

        @param data: dict representing the
        order data

        @return: None
        """
        footer = FooterContainer()
        self.add_display(footer)

        main = MainContainer(data)
        self.add_display(main)

        header = HeaderContainer()
        self.add_display(header)