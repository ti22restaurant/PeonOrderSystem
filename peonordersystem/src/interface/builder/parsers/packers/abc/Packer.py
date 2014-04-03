"""This module provides the
abstract base class for the
packer class.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AbstractPacker(object):
    """Describes the functionality
    required for an object to be a
    useable Packer.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def pack_menu_data(self, menu_data):
        """Updates the stored menu data
        by packing the given data into
        its source.

        @param menu_data: dict representing
        the updated menu data.

        @return: None
        """
        pass

    @abstractmethod
    def pack_categories_data(self, categories_data):
        """Updates the stored categories
        data by packing the given data
        into its source.

        @param categories_data: dict
        representing the updated categories
        data.

        @return: None
        """
        pass

    @abstractmethod
    def pack_options_data(self, option_data):
        """Updates the stored options data
        by packing the given data into its
        source.

        @param option_data: dict representing
        the updated options data.

        @return: None
        """
        pass

    @abstractmethod
    def pack_discount_template_data(self, discount_template_data):
        """Updates the stored discount templates
        data by packing the given data into
        its source.

        @param discount_template_data: dict
        representing the updated discount
        templates data.

        @return: None
        """
        pass