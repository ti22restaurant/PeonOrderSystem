"""This module defines the Divider
class that is used as a component
in a container.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from reportlab.platypus import Paragraph

from .abc.Component import Component


class Divider(Component):
    """Divider creates a divider
    using default settings to span
    a set distance across the ticket.
    """

    # Determined experimentally
    DIVIDER_FACTOR = 69
    DIVIDER = ':' * DIVIDER_FACTOR

    LINE_SIZE = 10
    NUM_OF_LINES = 1

    DIVIDER_TEXT = """
        <para align=center size={size}>
            {divider}
        </para>
    """.format(size=LINE_SIZE, divider=DIVIDER)

    DEFAULT_FONT_SIZE = 12

    def __init__(self):
        """Initializes the divider."""
        super(Divider, self).__init__()
        self._create_divider()

    @property
    def width(self):
        """Gets the width
        associated with the
        divider.

        @return: float representing
        the width.
        """
        return self.DEFAULT_WIDTH

    @property
    def height(self):
        """Gets the height
        associated with the
        divider.

        @return: float representing
        the height
        """
        return self.LINE_SIZE * self.NUM_OF_LINES * 2

    def _create_divider(self):
        """Creates the divider flowables.

        @return: None
        """
        text = self.DIVIDER_TEXT.format(divider=self.DIVIDER)
        p_text = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        self._flowables.append(p_text)