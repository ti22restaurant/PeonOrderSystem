"""This module defines the
KitchenFormatter that is used
to format files intended for
the kitchen.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from os.path import join

from peonordersystem.SystemPath import SYSTEM_TEMP_PATH
from peonordersystem.src.Settings import KITCHEN_TICKET_FILE_NAME

from .abc.AreaFormatter import AreaFormatter

from .containers.PriorityContainer import PriorityContainer
from .containers.TicketContainer import TicketContainer
from .containers.HeaderContainer import TicketHeaderContainer


class KitchenFormatter(AreaFormatter):
    """This class takes display components
    and formats them into a file for viewing
    for the kitchen
    """
    DEFAULT_FILE = join(SYSTEM_TEMP_PATH, KITCHEN_TICKET_FILE_NAME)
    REQUIRED_KEYS = {'priority', 'order'}

    @property
    def file_path(self):
        """Gets the file path
        that the formatted file
        is located at.

        @return: str representing
        the path to the generated
        file.
        """
        return self.DEFAULT_FILE

    @property
    def required_keys(self):
        """Gets a set of str
        representing the keys
        required of the given
        data.

        @return: set of str
        """
        return self.REQUIRED_KEYS

    def generate_display_areas(self, data):
        """Generates the display containers
        with the given data.

        @param data: dict of str keys to
        values that represent the data to
        be displayed.

        @return: None
        """
        if data.has_order:
            ticket = TicketContainer(data)
            self.add_display(ticket)

        if data.has_priority:
            priority = PriorityContainer(data)
            self.add_display(priority)

        header = TicketHeaderContainer(data)
        self.add_display(header)