"""This module defines the
Container that is used for
displaying general items
to the kitchen.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from reportlab.platypus import Paragraph

from .abc.ReceiptContainer import ReceiptContainer

from .components.KitchenTable import KitchenTable


class TicketContainer(ReceiptContainer):
    """This module is used to generate
    the display tables for the Ticket
    showing the normal orders MenuItems.
    """

    def __init__(self, order_data):
        """Initializes the container
        with the given order data.

        @param order_data: dict of
        str keys to values. The following
        str value pairs are expected to
        exist in the dict:

            'order' :   list of MenuItem objects
                        representing the non-priority
                        order.
        """
        super(TicketContainer, self).__init__()
        self._order_data = order_data

        self._generate_and_assemble_components()

    def _generate_and_assemble_components(self):
        """Generates and assembles the
        components used to display the
        items data.

        @return: None
        """
        ticket_title = self._create_ticket_title()
        items_table = self._create_items_table()

        self.add_flowables(*self.SPACER_ARGS)
        self.add_flowables(*self.SPACER_ARGS)
        self.add_flowables([ticket_title], self.DEFAULT_WIDTH, self.TITLE_SIZE)
        self.add_flowables(*self.SPACER_ARGS)

        self.add_component(items_table)

    def _create_ticket_title(self):
        """Creates the title associated
        with the TicketContainer area.

        @return: reportlab.platypus.Paragraph
        that is used to display the ticket
        title.
        """
        ptext = self.TITLE_FORMAT.format(size=self.TITLE_SIZE,
                                         title="ORDER : ")
        return Paragraph(ptext, self.DEFAULT_STYLE)

    def _create_items_table(self):
        """Creates the table used
        for displaying the items data

        @return: KitchenTable object
        that is used for displaying
        the items data.
        """
        return KitchenTable(self._order_data['order'])