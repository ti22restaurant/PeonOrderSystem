"""This module provides the
abstract base class for the
unpacker.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AbstractUnpacker(object):
    """Describes the default functionality
    necessary for an object to be a useable
    Unpacker.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def unpack_menu_data(self):
        """Gets the stored menu
        data.

        @return: dict
        """
        pass

    @abstractmethod
    def unpack_categories_data(self):
        """Gets the stored categories
        data.

        @return: dict
        """
        pass

    @abstractmethod
    def unpack_options_data(self):
        """Gets the stored options
        data.

        @return: dict
        """
        pass

    @abstractmethod
    def unpack_discount_templates_data(self):
        """Gets the stored discount
        templates data.

        @return: dict
        """
        pass
