"""This module defines the
properties view display area.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from gi.repository import Gtk

from .abc.View import AbstractView
from peonordersystem.src.interface.connectors.Connector import Connector


class PropertiesView(AbstractView):
    """Provides the functionality
    for a properties view area that
    generates widgets for display.
    """

    DEFAULT_BUTTON_HEIGHT = 50
    DEFAULT_BUTTON_WIDTH = 80

    def __init__(self, title):
        """Initializes the view.

        @param title: str to be
        associated with this area.
        """
        self._title = title
        self._connector = Connector()
        self._view = self._set_up_view()
        self._main_widget = self._set_up()

    @property
    def main_widget(self):
        """Gets the main widget
        that holds all the widgets
        to be displayed.

        @return: Gtk.Widget
        """
        return self._main_widget

    def _set_up_view(self):
        """Sets up the view for
        displaying data.

        @return: Gtk.TreeView
        """
        view = Gtk.TreeView()

        rend = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn('Unused Categories', rend, text=0)
        view.append_column(col)

        return view

    def _set_up(self):
        """Sets up the widgets for
        display

        @return: Gtk.Frame that holds
        all the widgets to be displayed.
        """
        frame = Gtk.Frame(label=self._title)
        main_box = Gtk.VBox()
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self._view)
        main_box.pack_start(scrolled_window, True, True, 5.0)

        control_area = self._create_control_area()
        main_box.pack_start(control_area, False, False, 5.0)

        frame.add(main_box)
        return frame

    def _create_control_area(self):
        """Creates the control area
        widgets for display.

        @return: Gtk.Container that
        holds all the widgets for
        displaying the control area.
        """
        main_box = Gtk.HBox()

        pull_button = self._set_up_push_button()
        main_box.pack_start(pull_button, False, False, 5.0)

        return main_box

    def _set_up_push_button(self):
        """Sets up the push button
        for pushing data from the
        view.

        @return: Gtk.Button that
        represents the push button.
        """
        button = Gtk.Button('<')
        button.set_focus_on_click(False)
        button.set_size_request(self.DEFAULT_BUTTON_WIDTH,
                                self.DEFAULT_BUTTON_HEIGHT)

        self._register_push_button(button)
        return button

    def _register_push_button(self, button):
        """Registers the given button as a
        push button.

        @param button: Gtk.Button that is to
        be registered as a push button.

        @return: None
        """
        self._connector.register(button, 'clicked', 'pull_category')

    def connect_signals(self, connect_ref):
        """Connects the signals associated
        with this view.

        @param connect_ref: obj representing
        the object to connect the signals to.

        @return: None
        """
        self._connector.connect(connect_ref)

    def get_selected(self):
        """Gets a reference to the
        currently selected row in
        the view.

        @return: Gtk.TreeIter pointing
        to the currently selected row.
        """
        selection = self._view.get_selection()
        model, itr = selection.get_selected()
        return itr

    def set_selected(self, itr):
        """Sets the selected row in
        the view.

        @param itr: Gtk.TreeIter
        pointing to the row to be
        selected.

        @return: Gtk.TreeIter pointing
        to the row that was selected.
        """
        selection = self._view.get_selection()
        return selection.select_iter(itr)

    def set_model(self, model):
        """Sets the model used to
        store the data for display
        in the view.

        @param model: Gtk.TreeModel
        that stores the data for
        display.

        @return: None
        """
        self._view.set_model(model)