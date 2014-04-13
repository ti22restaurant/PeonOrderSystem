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
    SPACER_WIDTH = 10
    SPACER_HEIGHT = 10
    SPACER = Spacer(10, 10)

    def __init__(self, x, y, order_data):
        """Initializes the MainContainer
        setting up the display at the given
        area with the given data.

        @param x: int representing the x
        coordinate that the container frame
        should be placed at.

        @param y: int representing the y
        coordinate that the container frame
        should be placed at.

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
        self._order_data = order_data
        self._expected_height = 0.0
        self._expected_width = 0.0

        self._components = self._generate_and_assemble_components()

        super(MainContainer, self).__init__(x, y, self._expected_width,
                                            self._expected_height)

    def _generate_and_assemble_components(self):
        """Generates and assembles the
        components.

        @return: list of reportlab.platypus.Flowable
        objects representing the data to be displayed.
        """
        order_number = self._create_order_num_display()
        divider = self._create_divider()
        items_table = self._create_items_display()
        total_table = self._create_total_display()

        components = []

        components += divider.flowables
        self._update_area(divider.height, divider.width)

        components += order_number.flowables
        self._update_area(order_number.height, order_number.width)

        components += divider.flowables
        self._update_area(divider.height, divider.width)

        components += items_table.flowables
        self._update_area(items_table.height, items_table.width)

        components += [self.SPACER]
        self._update_area(self.SPACER_HEIGHT, self.SPACER_WIDTH)

        components += total_table.flowables
        self._update_area(total_table.height, total_table.width)

        components += [self.SPACER]
        self._update_area(self.SPACER_HEIGHT, self.SPACER_WIDTH)

        return components

    def _update_area(self, height, width):
        """Updates the area with the given
        values.

        @param height: int representing the
        height value to update. This value is
        added to the current height.

        @param width: int representing the
        width value to update. This value will
        replace the current width if it is greater.
        But the width value will not be added.

        @return: None
        """
        self._expected_height += height
        self._expected_width = max(width, self._expected_width)

    def create_header(self):
        """Creates the header for
        the container.

        @return: list of reportlab.platypus.Flowable
        objects that are to be displayed in the
        container frame.
        """
        return self._components

    def _create_divider(self):
        """Creates the divider component.

        @return: Divider
        """
        return Divider()

    def _create_order_num_display(self):
        """Creates the order number
        component.

        @return: OrderNumber
        """
        return OrderNumber(self._order_data['number'])

    def _create_items_display(self):
        """Creates the items display
        component.

        @return: ItemsTable
        """
        return ItemsTable(self._order_data['order'])

    def _create_total_display(self):
        """Creates the total display
        component.

        @return: TotalsTable
        """
        return TotalsTable(self._order_data)