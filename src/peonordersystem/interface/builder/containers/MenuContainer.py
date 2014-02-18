"""This module provides the container
that is used to wrap the functionality
of the Gtk.Notebook so that components
may be added.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from gi.repository import Gtk

from .abc.Container import AbstractContainer
from .components.abc.Component import AbstractComponent


class MenuContainer(AbstractContainer):
    """Provides a wrapper for the Gtk.Notebook
    that allows for components to be added as
    new pages to the notebook.
    """

    def __init__(self, menu_notebook):
        """Initializes the container.

        @param menu_notebook: Gtk.Notebook
        that represents the Notebook to be
        wrapped.
        """
        self._check_notebook(menu_notebook)
        self._notebook = menu_notebook

    @staticmethod
    def _check_notebook(notebook):
        """Checks if the given notebook
        may have its functionality wrapped.

        @raise TypeError: If the given notebook
        is either null or isn't an instance of
        Gtk.Notebook.

        @param notebook: object to be tested.

        @return: bool value representing if
        the test was passed.
        """
        if not notebook or not isinstance(notebook, Gtk.Notebook):
            raise TypeError("Cannot perform this operation without a valid "
                            "Gtk.Notebook object to operate on!")
        return True

    def add(self, component):
        """Adds a component as a new
        page to the container notebook.

        @param component: AbstractComponent
        subclass that is to be added as a
        new page.

        @return: None
        """
        self._check_component(component)
        self._add_component(component)

    def _add_component(self, component):
        """Adds the given component to the
        notebook.

        @param component: AbstractComponent
        subclass that is to be added as a
        new page.

        @return: None
        """
        widget = component.main_widget
        title = component.name
        self._notebook.append_page(widget, tab_label=Gtk.Label(title))

    @staticmethod
    def _check_component(component):
        """Checks if the given component
        is of the proper type to be added
        to this container.

        @raise TypeError: If the given component
        is either null or not a subclass of
        AbstractComponent.

        @param component: object to be tested.

        @return: bool value representing
        if the test was passed.
        """
        if not component or not isinstance(component, AbstractComponent):
            raise TypeError("Cannot add a non-component to this container. The added"
                            " component must be a subclass of AbstractComponent")
        return True

