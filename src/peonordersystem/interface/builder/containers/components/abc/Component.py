"""This module provides the abstract
base classes for the components that
may be added to containers.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractComponent(object):
    """Describes the necessary functionality
    for an object to be useable as a component.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def name(self):
        """Gets the name
        associated with the
        component.

        @return: str
        """
        pass

    @abstractproperty
    def main_widget(self):
        """Gets the main widget
        associated with the component.

        @return: Gtk.Widget
        """
        pass

    @abstractmethod
    def add(self, area):
        """Adds the given area
        to the component.

        @param area: AbstractArea
        that will be added to this
        component.

        @return: None
        """
        pass
