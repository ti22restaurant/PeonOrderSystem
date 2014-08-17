"""This module provides the
UniqueModel that is used to
store and display a set of
unique strings that may be
added to or removed.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from gi.repository import Gtk

from .abc.Model import AbstractModel


class UniqueModel(AbstractModel):
    """Stores and provides the display
    for a list of values from which data
    may be added or removed.
    """

    def __init__(self, data):
        """Initializes the model

        @param data: set of str
        """
        self._data = data
        self._model = self._set_up()

    @property
    def data(self):
        """Gets the unique
        data displayed.

        @return: set of str
        """
        return self._data

    @property
    def model(self):
        """Gets the model used
        to display the data in
        a view.

        @return: Gtk.TreeModel
        """
        return self._model

    def _set_up(self):
        """Sets up the model
        for displaying the data.

        @return: Gtk.TreeModel
        """
        model = Gtk.ListStore(str)

        for data in self._data:
            model.append((data,))

        return model

    def add(self, value):
        """Adds the given value to
        the data

        @param value: str representing
        the data to be added.

        @return: Gtk.TreeIter pointing
        to the row added.
        """
        if value not in self._data:
            self._add_data(value)
            return self._add_model(value)

        return self.__iter__().iter

    def _add_model(self, value):
        """Adds the given value to
        the model for display.

        @param value: str to be added.

        @return: Gtk.TreeIter pointing
        to the value to be added.
        """
        return self.model.append((value,))

    def _add_data(self, value):
        """Adds the given value to
        the stored data.

        @param value: str representing
        the value to be added.

        @return: None
        """
        self._data.add(value)

    def remove(self, itr):
        """Removes the given
        row from the data set.

        @param itr: Gtk.TreeIter
        pointing to the data to
        be removed.

        @return: str representing
        the data that was removed.
        """
        value = self._remove_model(itr)
        return self._remove_data(value)

    def _remove_model(self, itr):
        """Removes the given row
        from the display model.

        @param itr: Gtk.TreeIter
        pointing to the row to be
        removed.

        @return: str representing
        the value that was removed.
        """
        value, = self.model[itr]
        self.model.remove(itr)
        return value

    def _remove_data(self, value):
        """Removes the given value
        from the stored data.

        @param value: str representing
        the value to be removed.

        @return: str
        """
        self._data.remove(value)
        return value