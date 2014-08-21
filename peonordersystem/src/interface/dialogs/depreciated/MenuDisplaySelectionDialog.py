"""This module provides a dialog
window for altering the categories
used to display the menu on the
main GUI.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from .views.abc.SelectionObserver import AbstractObserver

from peonordersystem.src.interface.dialogs.depreciated.Dialog import SelectionDialog
from peonordersystem.src.interface.dialogs.depreciated.models import UniqueModel, CategoriesModel, KeyModel
from peonordersystem.src.interface.dialogs.depreciated.views import MainView, PropertiesView, SecondaryView


class MenuDisplaySelectionDialog(SelectionDialog, AbstractObserver):
    """Provides the functionality for updating
    the menu display layout. Required connection
    to function that stores the display data, and
    input from function that pulls the display data.
    """
    TITLE = 'Menu Display Dialog'

    MAIN_AREA_NAME = 'Pages'
    SECONDARY_AREA_NAME = 'Categories'
    PROPERTIES_AREA_NAME = 'Remaining Unused Categories'

    def __init__(self, parent, confirm_func, category_data, categories):
        """Initializes the dialog window.

        @param parent: Gtk.Container that represents the
        parent this window will be called on.

        @param confirm_func: function to be called upon
        confirmation of this dialog window. Will be given
        a dict representing the updated menu display data.

        @param category_data: dict of str key to list
        of str keys representing the page and category
        data respectively.

        @param categories: list of str representing the
        potential categories for display.
        """
        self._observed = []

        self._confirm_func = confirm_func
        self._main_view = MainView.MainView('Page Keys')
        self._secondary_view = SecondaryView.SecondaryView('Display Categories')
        self._properties_view = PropertiesView.PropertiesView('Unused Categories')

        unused_categories = self._get_unused_categories(category_data, categories)

        self._main_model = KeyModel.KeyModel(category_data.keys())
        self._secondary_model = CategoriesModel.CategoriesModel(category_data)
        self._properties_model = UniqueModel.UniqueModel(unused_categories)

        self._set_up()
        super(MenuDisplaySelectionDialog, self).__init__(parent, self.TITLE)

    def _connect(self):
        """Connects the widget areas
        together.

        @return: None
        """
        self._main_view.connect_signals(self)
        self._secondary_view.connect_signals(self)
        self._properties_view.connect_signals(self)

        self._register_observers()

    def _register_observers(self):
        """Registers the observers

        @return: None
        """
        self._main_view.register_selection_observation(self)
        self._observed.append(self._main_view)

    def notify(self, *args):
        """Notifies the necessary areas
        that a selection change has occurred.

        @param args: wildcard keyword that
        represents the selection data given

        @return: None
        """
        itr = self._parse_notify_args(*args)
        data = self._main_model[itr]
        self._secondary_model.set_key(data)

    def _parse_notify_args(self, *args):
        """Parses the arguments from
        the notify method.

        @param args: wildcard catchall
        that represents the arguments
        passed intot he notify method.

        @return: Gtk.TreeIter representing
        the row selected.
        """
        itr = args[1]
        return itr

    def _get_unused_categories(self, category_data, categories):
        """Gets the unused categories.

        @param category_data: dict of str keys
        mapped to list of strs representing the
        pages and categories to display under the
        pages respectively.

        @param categories: list of str representing
        all potential categories.

        @return: set of categories that haven't been
        chosen to be displayed yet in the category
        data.
        """
        curr_categories = []
        potential_categories = set(categories)

        for categories in category_data.values():
            curr_categories += categories

        return potential_categories - set(curr_categories)

    def _set_up(self):
        """Sets up the model data and
        view widgets.

        @return: None
        """
        self._main_view.set_model(self._main_model.model)
        self._secondary_view.set_model(self._secondary_model.model)
        self._properties_view.set_model(self._properties_model.model)

        self._set_initial_display()
        self._connect()

    def _set_initial_display(self):
        """Sets up the initial display

        @return: None
        """
        itr = iter(self._main_model).iter
        if itr:
            value = self._main_model[itr]
            self._secondary_model.set_key(value)

    def add_key(self, obj, entry):
        """Adds the key stored in the
        given entry to the keys model.

        @param entry: Gtk.Entry that stores
        the key data

        @return: None
        """
        key = self._get_key_value(entry)
        if key:
            itr = self._main_model.add(key)
            self._main_view.set_selected(itr)
            self._secondary_model.set_key(key)

    def _get_key_value(self, entry):
        """Gets the key value stored
        in the entry.

        @param entry: Gtk.Entry that
        stores the key value.

        @return: str representing the
        key value.
        """
        text = entry.get_text()
        entry.set_text('')
        return self._parse_text(text)

    def _parse_text(self, text):
        """Parses the given text
        to be in storable format.

        @param text: str to be
        parsed

        @return: str
        """
        text = text.strip()
        return text.upper()

    def remove_selected_key(self, *args):
        """Removes the selected key from
        the data.

        @return: None
        """
        itr = self._main_view.get_selected()
        key = self._main_model.remove(itr)
        categories = self._secondary_model.remove_key(key)
        self._update_properties(categories)

    def _update_properties(self, categories):
        """Updates the properties model
        with the given categories data

        @param categories: list of str
        representing categories that
        need to be moved into the propreties
        display.

        @return: None
        """
        for category in categories:
            self._properties_model.add(category)

    def push_category(self, *args):
        """Push the category from the
        display category under the current
        key to the unused categories.

        @param args: wildcard catchall used
        to catch the widget that called this
        method.

        @return: None
        """
        itr = self._secondary_view.get_selected()
        category = self._secondary_model.remove(itr)
        self._properties_model.add(category)

    def pull_category(self, *args):
        """Pull the currently selected
        category displayed in the unused
        categories and add it to the display
        categories under the current key.

        @param args: wildcard catchall used
        to catch the widget that called this
        method.

        @return: None
        """
        itr = self._properties_view.get_selected()
        category = self._properties_model.remove(itr)
        self._secondary_model.add(category)

    def generate_main_selection_area(self):
        """Generates the main selection area
        widgets.

        @return: Gtk.Widget holding all widgets
        to be displayed in the main selection
        area.
        """
        return self._main_view.main_widget

    def generate_secondary_selection_area(self):
        """Generates the secondary selection area
        widgets.

        @return: Gtk.Widget holding all widgets
        to be displayed in the secondary selection
        area.
        """
        return self._secondary_view.main_widget

    def generate_properties_selection_area(self):
        """Generates the properties selection area
        widgets.

        @return: Gtk.Widget holding all widgets
        to be displayed in the properties selection
        area.
        """
        return self._properties_view.main_widget

    def confirm_data(self, *args):
        """Confirms the data and calls
        the confirmation function.

        @param args: wildcard catchall
        used to catch the widget that
        called this method.

        @return: None
        """
        data = self._secondary_model.data
        self._confirm_func(data)