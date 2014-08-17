"""This module provides the BaseLayout class

@author: Carl McGraw
@contact: cjmcgraw(- at -)u.washington.edu
@version: 1.x
"""
from peonordersystem.src.interface.dialogs.DialogBuilder import (PACK_ARGS,
                                                                 generate_hbox)
from .abc.AbstractLayout import AbstractLayout


class BaseLayout(AbstractLayout):
    """Provides a class that wraps components
    into a main layout.
    """

    def __init__(self):
        """Initializes the layout"""
        self._main_widget = generate_hbox()
        self._components = []

    @property
    def main_container(self):
        """Gets the main container

        @return: Gtk.Container
        """
        return self._main_widget

    def add_component(self, component):
        """Adds the given component to the
        layout.

        @param component: Gtk.Widget to be
        added.
        """
        component_widget = component.main_component
        self._components.append(component)
        self._main_widget.pack_start(component_widget, *PACK_ARGS)

    def remove_component(self, component):
        """Removes the given component from
        the layout.

        @param component: Gtk.Widget to be
        removed.

        @return: bool representing if the
        removal was successful or not
        """
        try:
            component_widget = component.main_component
            self._components.remove(component)
            self._main_widget.remove(component_widget)
            return True
        except ValueError:
            return False

    def remove_all_components(self):
        """Removes all currently stored
        components from the layout.
        """
        for component in self._components:
            self._main_widget.remove(component)

        self._components = []