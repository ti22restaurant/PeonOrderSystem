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
from reportlab.pdfgen.canvas import Canvas

from peonordersystem.SystemPath import SYSTEM_TEMP_PATH
from peonordersystem.src.Settings import FRONT_RECEIPT_FILE_NAME

from .containers.HeaderContainer import HeaderContainer
from .containers.MainContainer import MainContainer
from .containers.FooterContainer import FooterContainer

from .abc.Formatter import AbstractFormatter


class FrontFormatter(AbstractFormatter):
    """Formats given order data into a
    printable file representing a receipt
    for the "front" area to be displayed
    to customers
    """
    DEFAULT_FILE = join(SYSTEM_TEMP_PATH, FRONT_RECEIPT_FILE_NAME)

    REQUIRED_KEYS = {'order', 'number', 'total', 'subtotal', 'tax'}

    def __init__(self):
        """Initializes the FrontFormatter"""
        self._x = None
        self._y = None
        self._areas = None

    def format_data(self, data):
        """Formats the data into a
        file for printing

        @param data: dict representing
        the order data to be formatted
        The following keys are required:

            'order' :   list of MenuItem
                        representing the
                        order

            'number':   int representing
                        the order number

            'subtotal': float representing
                        the subtotal

            'tax'   :   float representing
                        the tax

            'total' :   float representing
                        the total

        @return: str representing the path
        to the file that was formatted
        """
        self._clear_state()
        self._check_keys(data)
        self._generate_display_areas(data)
        self._create_file()
        self._clear_state()
        return self.DEFAULT_FILE

    def _clear_state(self):
        """

        @return:
        """
        self._areas = []
        self._x = 0.0
        self._y = 0.0

    def _generate_display_areas(self, data):
        """Generates the areas for display
        from the given data

        @param data: dict representing the
        order data

        @return: None
        """
        footer = FooterContainer(0, self._y)
        self._areas.append(footer)
        area = footer.area
        self._x = max(self._x, area[0])
        self._y += area[1]

        main = MainContainer(0, self._y, data)
        self._areas.append(main)
        area = main.area
        self._x = max(self._x, area[0])
        self._y += area[1]

        header = HeaderContainer(0, self._y)
        self._areas.append(header)
        area = header.area
        self._x = max(self._x, area[0])
        self._y += area[1]

    def _check_keys(self, data):
        """Checks if the given data
        contains the required keys

        @param data: dict representing
        the order data

        @return: bool value representing
        if the test was passed or not
        """
        if not self.REQUIRED_KEYS in data:
            raise KeyError(
                """Cannot format order data. There were missing required keys in
                the given order data. Expected keys:
                    1. 'order'      :   list of MenuItems representing the order,
                    2. 'number'     :   int representing the order number,
                    3. 'subtotal'   :   float representing subtotal of order,
                    4. 'tax'        :   float representing the tax of the order,
                    5. 'total'      :   float representing the total of the order

                One or more keys were missing!
                Print job canceled.""")
        return True

    def _create_file(self):
        """Creates the file at the
        default path with the
        generated data displays

        @return: None
        """
        canvas = Canvas(self.DEFAULT_FILE, pagesize=(self._x, self._y))

        for area in self._areas:
            area.write(canvas)

        canvas.save()