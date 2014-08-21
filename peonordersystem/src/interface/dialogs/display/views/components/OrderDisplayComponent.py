"""This module defines the standard
order display class

@author: Carl McGraw
@contact: cjmcgraw(- at -)u.washington.edu
@version: 1.x
"""
from .abc.TreeViewComponent import TreeViewComponent
from peonordersystem.src.interface.dialogs.DialogBuilder import (PACK_ARGS,
                                                                 generate_hbox,
                                                                 generate_scrolled_window,
                                                                 generate_treeview,
                                                                 generate_text_columns)


class OrderDisplayComponent(TreeViewComponent):
    """This describes the functionality of the
    class whose main widget is simply an order
    display. This represents the view section
    which is entirely model less.
    """

    def __init__(self):
        """Initializes the display components"""
        self._view = None
        self._columns = []
        self._container = self._generate_container()

    @property
    def main_component(self):
        """Gets the main component to
        be displayed

        @return: Gtk.Container holding
        the widgets to be displayed
        """
        return self._container

    def get_selected(self):
        """Gets the currently selected
        row

        @return: Gtk.TreeIter
        """
        selection = self._view.get_selection()
        _, _, itr = selection.get_selected()
        return itr

    def set_selected(self, itr):
        """Selects the given represented
        row.

        @param itr: Gtk.TreeIter
        """
        self._view.set_selected(itr)

    def set_selection_func(self, func, *args):
        """Sets the selection function to the
        given function and passes the given
        arguments to that function

        @param func: function to be called
        upon selection

        @param args: catchall that catches
        all arguments and passes them to the
        function when called.
        """
        selection = self._view.get_selection()
        selection.set_select_function(func, None, True, *args)

    def set_model(self, model):
        """Sets the current display
        model.

        @param model: Gtk.TreeModel
        """
        self._view.set_model(model)

    def _generate_container(self):
        """Generates the main container
        for this display.

        @return: Gtk.Container
        """
        container = self._create_container()
        self._create_view()
        scrolled_window = generate_scrolled_window()
        scrolled_window.add(self._view)
        container.pack_start(scrolled_window, *PACK_ARGS)
        return container

    def _create_view(self):
        """Creates the view to be
        displayed in the main
        container.

        @return: Gtk.TreeView
        """
        columns = self._generate_columns()
        self._view = generate_treeview()
        self.set_columns(columns)

    def set_columns(self, columns):
        """

        @param columns:
        @return:
        """
        for col in self._columns:
            self._view.remove_column(col)

        self._columns = []
        for column in columns:
            self._view.append_column(column)
            self._columns.append(column)

    def _generate_columns(self):
        """Generates the columns to
        be displayed in the view

        @return: list of
        Gtk.TreeViewColumns
        """
        col_titles = self._generate_column_titles()
        return generate_text_columns(col_titles)

    def _generate_column_titles(self):
        """Generates a list of titles
        representing the titles to be
        associated with the columns of
        the display

        @return: list of str
        """
        return ["Order Name"]

    def _create_container(self):
        """Creates the container.

        @return: Gtk.Container
        """
        return generate_hbox()