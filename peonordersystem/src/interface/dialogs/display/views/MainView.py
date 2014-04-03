"""This module defines the
MainView class that is used
that is used to display the
main view widgets.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from gi.repository import Gtk

from .abc.View import AbstractView
from .abc.SelectionObserver import AbstractObserver
from .abc.SelectionObservable import AbstractSelectionObservable

from peonordersystem.src.interface.connectors.Connector import Connector


class MainView(AbstractView, AbstractSelectionObservable):
    """Provides the functionality for
    a main view area which includes a view for
    displaying data and the buttons to alter said
    view.
    """

    def __init__(self, title):
        """Initializes the view.

        @param title: str to be
        associated with the area.
        """
        self._title = title
        self._connector = Connector()
        self._view = self._set_up_view()
        self._entry = Gtk.Entry()

        self._observers = set()

        self._main_widget = self._set_up()

    @property
    def main_widget(self):
        """Gets the main widget
        that holds all widgets
        to display.

        @return: Gtk.Widget
        """
        return self._main_widget

    def _set_up(self):
        """Sets up the widgets
        associated with this
        class.

        @return: Gtk.Frame that
        represents the main widget
        to display.
        """
        frame = Gtk.Frame(label=self._title)
        main_box = Gtk.VBox()
        main_box.pack_start(self._view, True, True, 5.0)
        control_area = self._create_control_area()

        main_box.pack_start(control_area, False, False, 5.0)

        frame.add(main_box)
        return frame

    def _create_control_area(self):
        """Creates the control area of
        the main widget. This area is
        used to control the view display.

        @return: Gtk.Box that stores the
        widgets for the control area.
        """
        main_box = Gtk.VBox()

        add_area = self._create_control_area_add()
        main_box.pack_start(add_area, True, True, 5.0)
        remove_area = self._create_control_area_remove()
        main_box.pack_start(remove_area, True, True, 5.0)

        return main_box

    def _create_control_area_add(self):
        """Creates the add area of the
        control area.

        @return: Gtk.Box that displays
        the widgets associated with the
        add area.
        """
        main_box = Gtk.HBox()

        main_box.pack_start(self._entry, True, True, 5.0)
        add_button = self._set_up_add_button()
        main_box.pack_start(add_button, False, False, 5.0)

        return main_box

    def _set_up_add_button(self):
        """Sets up the add button

        @return: Gtk.Button that
        represents the set up add
        button.
        """
        button = Gtk.Button('ADD NEW PAGE')
        button.set_focus_on_click(False)
        self._register_add_button(button)
        return button

    def _register_add_button(self, button):
        """Registers the given button as
        an add button with the connector.

        @param button: Gtk.Button to be
        registered as an add button.

        @return: None
        """
        self._connector.register(button, 'clicked', 'add_key', self._entry)

    def _create_control_area_remove(self):
        """Creates the remove area for the
        control area.

        @return: Gtk.Box that holds all the
        widgets for displaying the remove
        area.
        """
        main_box = Gtk.HBox()
        remove_button = self._set_up_remove_button()
        main_box.pack_end(remove_button, False, False, 5.0)

        return main_box

    def _set_up_remove_button(self):
        """Sets up the remove button.

        @return: Gtk.Button
        """
        button = Gtk.Button('REMOVE PAGE')
        button.set_focus_on_click(False)
        self._register_remove_button(button)
        return button

    def _register_remove_button(self, button):
        """Registers the given button as a
        remove button.

        @param button: Gtk.Button that is to
        be registered as a remove button.

        @return:
        """
        self._connector.register(button, 'clicked', 'remove_selected_key')

    def _set_up_view(self):
        """Sets up the view for
        displaying the data.

        @return: Gtk.TreeView
        """
        view = Gtk.TreeView()

        selection = view.get_selection()
        selection.set_select_function(self._select_func, None)

        rend = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Page Key', rend, text=0)
        view.append_column(column)

        return view

    def _select_func(self, selection, model, path, is_selected, *args):
        """Function that is called when a
        selectino has been made.

        @param selection: Gtk.TreeSelection
        that represents the selection associated
        with the view.

        @param model: Gtk.TreeModel that represents
        the model associated with the view.

        @param path: Gtk.TreePath representing the
        path of the row that was selected and initiated
        this function call.

        @param is_selected: bool value representing if
        the row is currently selected.

        @param args: wildcard catchall for any user data.

        @return: bool value representing if the row
        is acceptable to be selected.
        """
        # has_selection is used to prevent multiple
        # notifications to observers. This ensures that
        # the method is only entered when a row is selected
        # and not unselected.
        _, has_selection = selection.get_selected()

        if not is_selected and has_selection:
            itr = model.get_iter(path)
            self.notify_selection(self, itr)
        return True

    def register_selection_observation(self, observer_ref):
        """Registers the given observer reference
        as a selection observer on this view.

        @param observer_ref: AbstractObserver
        subclass that wants to observer.

        @return: bool value if the registration
        was successful or not.
        """
        if observer_ref and isinstance(observer_ref, AbstractObserver):
            self._observers.add(observer_ref)
            return True
        return False

    def unregister_selection_observation(self, observer_ref):
        """Unregisters the given observer refrence
        as a selection observer for this view.

        @param observer_ref: obj that is to be
        unregistered.

        @return: bool value if the unregistration
        was successful or not.
        """
        if observer_ref in self._observers:
            self._observers.remove(observer_ref)
            return True
        return False

    def notify_selection(self, *args):
        """Notifies the observers that
        a selection has been made.

        @param args: arguments to be
        passed to the observers.

        @return: None
        """
        for observer in self._observers:
            observer.notify(*args)

    def set_model(self, model):
        """Sets the model for the
        display.

        @param model: Gtk.TreeModel
        that stores the data to display.

        @return: None
        """
        self._view.set_model(model)

    def get_selected(self):
        """Gets the iter pointing
        to the selected row.

        @return: Gtk.TreeIter pointing
        to the currently selected row.
        """
        selection = self._view.get_selection()
        model, itr = selection.get_selected()
        return itr

    def set_selected(self, itr):
        """Sets the currently
        selected row.

        @param itr: Gtk.TreeIter
        pointing to the row that
        should be selected.

        @return: None
        """
        selection = self._view.get_selection()
        selection.select_iter(itr)

    def connect_signals(self, connect_ref):
        """Connects the widget signals
        associated with the display widgets.

        @param connect_ref: obj that the
        signals will be connected to.

        @return: None
        """
        self._connector.connect(connect_ref)
