"""This module provides the abstract base
class for an object to be an area and as
such addable to a component.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractproperty


class AbstractArea(object):
    """Defines the base functionality
    required for an object to be a
    useable area.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def main_widget(self):
        """Gets the main widget
        associated with the area.

        @return: Gtk.Widget
        """
        pass