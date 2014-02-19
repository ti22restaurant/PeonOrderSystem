"""This module provides the
CategoriesModel class that
is designed to store keys and
categories data and display the
categories dependent on which key
is given.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from gi.repository import Gtk
from collections import OrderedDict

from .abc.Model import AbstractModel


class CategoriesModel(AbstractModel):
    """Stores and controls the categories
    data that is linked to a set of keys.
    """

    def __init__(self, categories_data):
        """Initializes the model.

        @param categories_data: dict
        of categories data that maps
        str key values to lists of str
        categories values.
        """
        self._data = OrderedDict(categories_data)
        self._current_key = None
        self._model = self._set_up()

    @property
    def data(self):
        """Gets the data associated
        with this object.

        @return: OrderedDict representing
        the stored keys to categories.
        """
        return self._data

    @property
    def model(self):
        """Gets the model used
        for displaying the data
        in a view.

        @return: Gtk.TreeModel
        """
        return self._model

    def _set_up(self):
        """Sets up the model

        @return: Gtk.TreeModel
        """
        return Gtk.ListStore(str)

    def set_key(self, key):
        """Sets the categories to
        display as those under the
        given key. If that key isnt
        present it is added.

        @param key: str representing
        the key to display.

        @return: None
        """
        if not key in self._data:
            self._add_key(key)

        self._set_key(key)

    def _set_key(self, key):
        """Sets the display to
        display the given categories
        associated with the key.

        @param key: str representing
        the key to display.

        @return: None
        """
        self.model.clear()

        for category in self._data[key]:
            self.model.append((category,))

        self._current_key = key

    def _add_key(self, key):
        """Adds the key to the
        data with an empty category
        list.

        @param key: str representing
        the key.

        @return: None
        """
        self._data[key] = []

    def remove_key(self, key):
        """Removes the given
        key from the display and
        data.

        @param key: str representing
        the key to be removed.

        @return: list of str representing
        the categories associated with the
        removed key.
        """
        self._remove_key_model()
        categories = self._remove_key_data(key)
        return categories

    def _remove_key_model(self):
        """Removes the key from
        the display model.

        @return: None
        """
        self.model.clear()

    def _remove_key_data(self, key):
        """Removes the key data

        @param key: str representing
        the key.

        @return: list of str representing
        the categories associated with the
        removed key.
        """
        categories = self._data[key]
        self._data.pop(key)
        return categories

    def add(self, category):
        """Adds the given data
        to the currently selected
        keys as a category.

        @param category: str representing
        the category to add to the
        keys categories.

        @return: Gtk.TreeIter pointing
        to the row added.
        """
        self._add_data(category)
        return self._add_model(category)

    def _add_data(self, category):
        """Adds the given data to
        the categories.

        @param category: str representing
        the category to be added.

        @return: None
        """
        categories = self._data[self._current_key]
        categories.append(category)

    def _add_model(self, category):
        """Adds the given category
        to the display model.

        @param category: str
        representing the category
        to be added to the display.

        @return: Gtk.TreeIter pointing
        to the row that was added.
        """
        return self.model.append((category,))

    def remove(self, itr):
        """Removes the category
        pointed to by the given
        iter.

        @param itr: Gtk.TreeIter
        pointing to the row to be
        removed.

        @return: str representing
        the category that was removed.
        """
        category = self._remove_model(itr)
        self._remove_data(category)
        return category

    def _remove_model(self, itr):
        """Removes the row from
        the display model.

        @param itr: Gtk.TreeIter
        pointing to the row to
        be removed.

        @return: str representing
        the category removed from
        the model.
        """
        value, = self.model[itr]
        self.model.remove(itr)
        return value

    def _remove_data(self, category):
        """Removes the given category
        from the stored categories
        associated with the current
        key.

        @param category: str representing
        the category to be removed.

        @return: None
        """
        categories = self._data[self._current_key]
        categories.remove(category)