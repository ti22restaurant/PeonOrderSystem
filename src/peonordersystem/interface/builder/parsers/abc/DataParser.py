"""This module defines the abstract
base class for DataParser objects.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractproperty, abstractmethod


class AbstractDataParser(object):
    """Describes the required functionality
    for an object to be a useable DataParser.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def menu_data(self):
        """Gets the stored menu
        data.

        @return: dict
        """
        pass

    @abstractproperty
    def categories_data(self):
        """Gets the stored
        categories data.

        @return: dict
        """
        pass

    @abstractmethod
    def unpack_menu_item_data(self):
        """Unpacks the menu item data
        from its source.

        @return: dict
        """
        pass

    @abstractmethod
    def unpack_categories_data(self):
        """Unpacks the categories data
        from its source.

        @return: dict
        """
        pass

    @abstractmethod
    def unpack_options_data(self):
        """Unpacks the options data
        from its source

        @return: dict
        """
        pass

    @abstractmethod
    def unpack_discount_templates_data(self):
        """Unpacks the discount templates
        data from its source

        @return: dict
        """
        pass

    @abstractmethod
    def pack_menu_data(self, menu_data):
        """Updates the stored menu data's
        source by packing the given data
        into it.

        @param menu_data: dict representing
        the updated menu data.

        @return: None
        """
        pass

    @abstractmethod
    def pack_options_data(self, options_data):
        """Updates the stored options data's
        source by packing the given data into
        it.

        @param options_data: dict representing
        the updated options data.

        @return: None
        """
        pass

    @abstractmethod
    def pack_categories_data(self, categories_data):
        """Updates the stored categories data's
        source by packing the given data into
        it.

        @param categories_data: dict representing
        the updated categories data.

        @return: None
        """
        pass

    @abstractmethod
    def pack_discount_templates_data(self, discount_templates_data):
        """Updates the stored discount templates
        data's source by packijng the given data
        into it.

        @param discount_templates_data: dict
        representing the updated discount templates
        data.

        @return: None
        """
        pass