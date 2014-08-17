"""This module defines the abstract dialog
class.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.1
"""

from abc import ABCMeta, abstractmethod
from peonordersystem.src.interface.dialogs.DialogBuilder import (ACCEPT_RESPONSE,
                                                                 CANCEL_RESPONSE)


class AbstractDialog(object):
    """Abstract class that defines the outward
    facing functionality for a dialog class.
    """
    ACCEPT_RESPONSE = ACCEPT_RESPONSE
    CANCEL_RESPONSE = CANCEL_RESPONSE

    __metaclass__ = ABCMeta

    @abstractmethod
    def set_layout(self, layout):
        """Sets the content area of
        the dialog to the given layout

        @param layout: Gtk.Widget
        """
        pass

    @abstractmethod
    def run_dialog(self):
        """Runs the dialog

        @return int: representing
        the response.
        """
        pass
