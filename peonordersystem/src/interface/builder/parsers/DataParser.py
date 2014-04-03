"""This module provides the DataParser
class that is used to pull necessary
data used by the Builder.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.DataParser import AbstractDataParser

from .packers.Packer import Packer
from .unpackers.Unpacker import Unpacker


class DataParser(AbstractDataParser):
    """Provides the generated and
    constant data necessary for
    performing building operations.
    """

    # Widget names supplied in the glade generated XML file.
    WIDGET_NAMES = {'main_window': 'POS_main_window',
                    'order_window': 'orderView',
                    'reservations_window': 'reservationsScrollWindow',
                    'upcoming_orders_window': 'upcomingOrdersScrollWindow',
                    'table_box': 'tablesBox',
                    'status_label': 'statusLabel',
                    'menu_notebook': 'menuNotebook',
                    'order_label': 'orderListLabel'}

    # Expected function names in the class that the signals will be connected to.
    FUNC_NAMES = {'table_button': 'table_button_clicked',
                  'menu_button': 'menu_button_clicked',
                  'misc_button': 'select_misc_order'}

    # Gtk.Widget flags that are useful.
    FLAGS = {'button': 'clicked',
             'destroy': 'delete-event'}

    def __init__(self):
        """Initializes the DataParser"""
        self._packer = Packer()
        self._unpacker = Unpacker()

        self._categories_display_data = self.unpack_categories_data()
        self._menu_items_data = self.unpack_menu_data()

    @property
    def menu_data(self):
        """Gets the stored menu data
        associated with the parser.

        @return: dict
        """
        return self._menu_items_data

    @property
    def categories_data(self):
        """Gets the stored categories
        data associated with the parser.

        @return: dict
        """
        return self._categories_display_data

    def unpack_menu_data(self):
        """Unpacks the stored menu data
        from its source.

        @note: Unless alterations have
        been made this will be identical
        to the menu_data property.

        @return: dict
        """
        return self._unpacker.unpack_menu_data()

    def unpack_categories_data(self):
        """Unpacks the categories data
        from its source.

        @note: Unless alterations have
        been made this will be identical
        to the categories_data property.

        @return: dict
        """
        return self._unpacker.unpack_categories_data()

    def unpack_options_data(self):
        """Unpacks the stored options
        data from its source.

        @return: dict
        """
        return self._unpacker.unpack_options_data()

    def unpack_discount_templates_data(self):
        """Unpacks the discount templates
        data from its source.

        @return: dict
        """
        return self._unpacker.unpack_discount_templates_data()

    def pack_menu_data(self, menu_data):
        """Updates the stored menu
        data at its source.

        @note: These changes will
        not be reflected in the
        property of the DataParser.
        It will continue to maintain
        a reference to the initial
        starting menu_data property.

        @param menu_data: dict
        representing the updated
        menu data.

        @return: None
        """
        self._packer.pack_menu_data(menu_data)

    def pack_categories_data(self, categories_data):
        """Updates the stored categories
        data at its source.

        @note: These changes will not
        be reflected in the property
        of the DataParser. It will
        continue to maintain a reference
        to the initial starting
        categories_data property.

        @param categories_data: dict
        representing the updated
        categories data.

        @return: None
        """
        self._packer.pack_categories_data(categories_data)

    def pack_options_data(self, option_data):
        """Updates the stored options
        data at its source.

        @param option_data: dict
        representing the updated
        options data.

        @return: None
        """
        self._packer.pack_options_data(option_data)

    def pack_discount_templates_data(self, discount_templates_data):
        """Updates the stored discount
        templates data at its source.

        @param discount_templates_data: dict
        representing the updated discount
        templates data.

        @return: None
        """
        self._packer.pack_discount_template_data(discount_templates_data)
