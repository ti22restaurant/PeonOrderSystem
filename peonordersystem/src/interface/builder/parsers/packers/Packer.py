"""This module provides the
Packer class which is used
to update stored data used
by the builder.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import jsonpickle
jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)

from .abc.Packer import AbstractPacker
from peonordersystem.SystemPath import (MENU_DATA, OPTION_DATA,
                                        DISCOUNT_DATA, CATEGORIES_DISPLAY_DATA)


class Packer(AbstractPacker):
    """Updates stored data used
    by the builder.
    """

    def pack_menu_data(self, menu_data):
        """Updates the stored menu data
        by packing the given data into
        its source.

        @param menu_data: dict representing
        the updated menu data.

        @return: None
        """
        self._pack_data(menu_data, MENU_DATA)

    def pack_options_data(self, option_data):
        """Updates the stored options data
        by packing the given data into its
        source.

        @param option_data: dict representing
        the updated options data.

        @return: None
        """
        self._pack_data(option_data, OPTION_DATA)

    def pack_categories_data(self, categories_data):
        """Updates the stored categories data
        by packing the given data into its
        source.

        @param categories_data: dict representing
        the updated categories data.

        @return: None
        """
        self._pack_data(categories_data, CATEGORIES_DISPLAY_DATA)

    def pack_discount_template_data(self, discount_template_data):
        """Updates the stored discount template
        data by packing the given data into
        its source.

        @param discount_template_data: dict
        representing the updated discount
        templates data.

        @return: None
        """
        self._pack_data(discount_template_data, DISCOUNT_DATA)

    def _pack_data(self, data, filepath):
        """Packs the given data into
        the given file path.

        @param data: obj that is to be
        the updated data.

        @param filepath: str representing
        the filepath to the source that
        is to be overwritten.

        @return: None
        """
        with open(filepath, 'w') as f_data:
            encoded_data = jsonpickle.encode(data)
            f_data.write(encoded_data)