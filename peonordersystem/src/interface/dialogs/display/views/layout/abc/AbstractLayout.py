"""This module defines the basic fucntionality
of the abstract layout class

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.1
"""

from abc import ABCMeta, abstractproperty, abstractmethod


class AbstractLayout(object):
    """Provides the external facing functionality
    for the BaseLayout class
    """
    
    __metaclass__ = ABCMeta
    
    @abstractproperty
    def main_container(self):
        """Gets the main component
        
        @return: Gtk.Widget
        """
        pass

    @abstractmethod
    def add_component(self, component):
        """Adds the given component to the
        layout.

        @param component: Gtk.Widget that
        represents the component to be added.

        @return: bool representing if the
        component was added
        """
        pass

    @abstractmethod
    def remove_component(self, component):
        """Removes the given component from
        the layout.

        @param component: Gtk.Widget that
        represents the component to be
        removed.

        @return: bool representing if the
        component was removed.
        """
        pass

    @abstractmethod
    def remove_all_components(self):
        """Removes all components from the
        layout.

        @return:
        """
        pass
