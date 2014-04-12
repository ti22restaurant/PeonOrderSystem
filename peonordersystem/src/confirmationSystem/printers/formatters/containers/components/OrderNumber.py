"""This module describes the OrderNumber
class that is used to generate objects
for displaying the Order Number on a
receipt.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from reportlab.platypus import Paragraph

from .abc.Component import Component


class OrderNumber(Component):
    """Creates the necessary objects
    that can be used to display an
    the order number on a receipt.
    """
    DEFAULT_HEIGHT = 12

    ORDER_NUMBER_FORMAT = """
        <para align=left size=%s>
            Order Number #{number}
        </para>
    """ % DEFAULT_HEIGHT

    def __init__(self, number):
        """Initializes the OrderNumber with
        the given number.

        @param number: int representing the
        order number to be displayed.
        """
        super(OrderNumber, self).__init__()
        self._generate_order_number(number)

    @property
    def height(self):
        """Gets the height of this
        component.

        @return: float representing
        the height.
        """
        return self.DEFAULT_HEIGHT * 2

    @property
    def width(self):
        """Gets the width of this
        component.

        @return: float representing
        the width.
        """
        return self.DEFAULT_WIDTH

    def _generate_order_number(self, number):
        """Generates the display for the order
        number.

        @param number: int representing the
        order number to display.

        @return: None
        """
        text = self.ORDER_NUMBER_FORMAT.format(number=number)
        p_text = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        self._flowables.append(p_text)