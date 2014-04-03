"""This module provides the KeyModel
that is used for storing and modifying
a collection of unique keys.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from gi.repository import Gtk
from .abc.Model import AbstractModel


class KeyModel(AbstractModel):
    """Stores given key data for
    modification and display via
    a TreeView.
    """

    def __init__(self, key_data):
        """Initializes the KeyModel

        @param key_data: collection
        of str values representing
        the stored keys.
        """
        self._keys = set(key_data)
        self._model = self._set_up()

    @property
    def data(self):
        """Gets the keys data
        stored in the model.

        @return: set of str
        """
        return self._keys

    @property
    def model(self):
        """Gets the model used
        for displaying the data.

        @return: Gtk.TreeModel
        """
        return self._model

    def _set_up(self):
        """Sets up the model

        @return: Gtk.TreeModel
        """
        model = Gtk.ListStore(str)

        for key in self._keys:
            model.append((key,))

        return model

    def add(self, key):
        """Adds the given key
        to the model and data.

        @param data: str representing
        the key to be added.

        @return: Gtk.TreeIter pointing
        to the row in the model that
        the data was added to.
        """
        if key not in self._keys:
            return self._add_data(key)
        else:
            return self.__iter__().iter

    def _add_data(self, key):
        """Adds the given data to
        the object.

        @param key: str representing
        the key to be added.

        @return: Gtk.TreeIter pointing
        to the row in the model
        that the data was added to.
        """
        self._add_to_data(key)
        return self._add_to_model(key)

    def _add_to_model(self, key):
        """Adds the given key to
        the model.

        @param key: str representing
        the key to be added.

        @return: Gtk.TreeIter pointing
        to the row in the model that
        the data was added to.
        """
        return self.model.append((key,))

    def _add_to_data(self, key):
        """Adds the given key to
        the data.

        @param key: str representing
        the data

        @return: None
        """
        self._keys.add(key)

    def remove(self, itr):
        """Removes the given
        data at iter from the
        model and data.

        @param itr: Gtk.TreeIter
        representing the row
        that stores the data to
        be removed.

        @return: str representing
        the key that was removed.
        """
        key = self._remove_from_model(itr)
        self._remove_from_data(key)
        return key

    def _remove_from_model(self, itr):
        """Removes the associated
        row from the model.

        @param itr: Gtk.TreeIter
        pointing to the row to be
        removed.

        @return: str representing
        the value removed from the
        row.
        """
        value, = self.model[itr]
        self.model.remove(itr)
        return value

    def _remove_from_data(self, key):
        """Removes the given key
        from the data.

        @param key: str representing
        the given key to be removed.

        @return: None
        """
        self._keys.remove(key)