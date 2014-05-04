"""This module defines the
PriorityContainer that is
used to display priority
items data.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph

from .abc.ReceiptContainer import ReceiptContainer

from .components.KitchenTable import KitchenTable
from .components.Divider import Divider

from peonordersystem.src.confirmationSystem.printers.formatters.PrinterSettings \
    import DEFAULT_FRONT_PRINTER_WIDTH


class PriorityContainer(ReceiptContainer):
    """Provides the functionality for
    displaying priority items.
    """
    DIVIDER = Divider()

    TITLE_SIZE = 12
    TITLE_FORMAT = """
        <para size=%s>
            <b>PRIORITY : </b>
        </para>
    """ % TITLE_SIZE

    PARAGRAPH_STYLE = getSampleStyleSheet()['Normal']

    TITLE = Paragraph(TITLE_FORMAT, PARAGRAPH_STYLE)
    TITLE_ARGS = [TITLE], DEFAULT_FRONT_PRINTER_WIDTH, TITLE_SIZE

    def __init__(self, order_data):
        """Initializes the PriorityContainer
        with the given data.

        @param order_data: dict of str keys
        mapped to necessary values. Expected
        key value pairs for the priority
        container are:

            'priority'  :   list of MenuItems
                            that represents the
                            priority order.
        """
        super(PriorityContainer, self).__init__()
        self._order_data = order_data

        self._generate_and_assemble_components()

    def _generate_and_assemble_components(self):
        """Generates and assembles the
        components that are used to create
        the display for the container.

        @return: None
        """
        priority_table = self._create_priority_table()

        self.add_flowables(*self.TITLE_ARGS)
        self.add_component(self.DIVIDER)
        self.add_component(priority_table)
        self.add_component(self.DIVIDER)

    def _create_priority_table(self):
        """Creates the priority table
        for displaying the items.

        @return: Component that represents
        the priority table.
        """
        return KitchenTable(self._order_data['priority'])