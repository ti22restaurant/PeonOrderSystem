"""This module defines the class
that is used to display the general
main part of a receipt.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from reportlab.platypus import Spacer

from .abc.ReceiptContainer import ReceiptContainer

from .components.TotalsTable import TotalsTable
from .components.ItemsTable import ItemsTable
from .components.Divider import Divider
from .components.OrderNumber import OrderNumber


class MainContainer(ReceiptContainer):
    """Used to generate the display of
    the main area of a receipt which
    includes displaying item, options
    and totals data.
    """
    DIVIDER = Divider()

    def __init__(self, order_data):
        """Initializes the MainContainer
        setting up the display at the given
        area with the given data.

        @param order_data: dict representing
        the order data. The following key and
        value pairs are expected:

            'number'    :   int representing order
                            number.

            'order'     :   list of MenuItems representing
                            the order.

            'subtotal'  :   float representing the subtotal

            'tax'       :   float representing the tax

            'total'     :   float representing the total
        """
        super(MainContainer, self).__init__()
        self._order_data = order_data
        self._generate_and_assemble_components()

    def _generate_and_assemble_components(self):
        """Generates and assembles the
        components.

        @return: list of reportlab.platypus.Flowable
        objects representing the data to be displayed.
        """
        order_number = self._create_order_num_display()
        items_table = self._create_items_display()
        total_table = self._create_total_display()

        self.add_component(self.DIVIDER)
        self.add_component(order_number)
        self.add_component(self.DIVIDER)
        self.add_component(items_table)
        self.add_flowables(*self.SPACER_ARGS)
        self.add_component(total_table)
        self.add_flowables(*self.SPACER_ARGS)

    def _create_order_num_display(self):
        """Creates the order number
        component.

        @return: OrderNumber
        """
        return OrderNumber(self._order_data.number)

    def _create_items_display(self):
        """Creates the items display
        component.

        @return: ItemsTable
        """
        return ItemsTable(self._order_data.order)

    def _create_total_display(self):
        """Creates the total display
        component.

        @return: TotalsTable
        """
        return TotalsTable(self._order_data.totals)