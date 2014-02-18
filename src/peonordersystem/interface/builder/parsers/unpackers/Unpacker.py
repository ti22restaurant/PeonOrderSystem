"""This module provides the
unpacker class that is used
to retrieve stored data used
by the builder object.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import jsonpickle

from .abc.Unpacker import AbstractUnpacker
from src.peonordersystem.path import (MENU_DATA, OPTION_DATA,
                                      DISCOUNT_DATA, CATEGORIES_DISPLAY_DATA)


class Unpacker(AbstractUnpacker):
    """Retrieves stored data that
    is used by the builder object.
    """

    def unpack_menu_data(self):
        """Unpacks the menu data

        @return: dict
        """
        return self._unpack_data(MENU_DATA)

    def unpack_categories_data(self):
        """Unpacks the categories data

        @return: dict
        """
        return self._unpack_data(CATEGORIES_DISPLAY_DATA)

    def unpack_options_data(self):
        """Unpacks the options data

        @return: dict
        """
        return self._unpack_data(OPTION_DATA)

    def unpack_discount_templates_data(self):
        """Unpacks the discount templates
        data.

        @return: dict
        """
        return self._unpack_data(DISCOUNT_DATA)

    def _unpack_data(self, filepath):
        """Unpacks the data at the
        given filepath

        @param filepath: str representing
        the path to the file that is to
        have its data unpacked via jsonpickle.

        @return: obj representing the data
        that was stored in the file and
        unpacked via jsonpickle.
        """
        f_data = open(filepath, 'r')
        return jsonpickle.decode(f_data.read())