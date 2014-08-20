"""This module defines the StandardModel
which is the basic implementation of a model.

@author: Carl McGraw
@contact: cjmcgraw(- at -)u.washington.edu
@version: 1.x
"""
from itertools import chain

from .abc.AbstractModel import AbstractModel
from peonordersystem.src.interface.dialogs.DialogBuilder import generate_liststore


class StandardModel(AbstractModel):
    """Describes a object that maps a standard
    model onto a more familiar interface.
    """

    def __init__(self, types=(str, str, str)):
        """Initializes the StandardModel

        @keyword types: list of types representing
        the types to be stored in the model
        """
        self._model = generate_liststore(*types)

    @property
    def model(self):
        """Gets the model wrapped
        by this class

        @return: Gtk.TreeModel
        """
        return self._model

    def append(self, values):
        """Appends the given values
        to the model

        @param values: list of values
        matching the types expected

        @return: Gtk.TreeIter pointing
        to the values added
        """
        return self._model.append(values)

    def insert(self, row, values):
        """Inserts the given values
        after the given row

        @param row: Gtk.TreeIter

        @param values: list of values
        that match the expected types

        @return: Gtk.TreeIter pointing
        to the value that was inserted
        """
        return self._model.insert_before(row, values)

    def clear(self):
        """Clears all entries from
        the model
        """
        self._model.clear()

    def __getitem__(self, row):
        """Gets the item at the given
        row

        @param row: Gtk.TreeIter

        @return: tuple of values
        representing the row
        """
        return self._model[row][:]

    def __setitem__(self, row, values):
        """Sets the given values to the
        given values

        @param row:
        @param values:
        @return:
        """
        args = chain.from_iterable(zip(range(0, len(values)), values))
        return self._model.set(row, *args)

    def __iter__(self):
        """Gets an iterator over
        the models values

        @return: iterator
        """
        for row in self._model:
            yield row[:]

    def __delitem__(self, row):
        """Deletes the row at the
        given location

        @param row: Gtk.TreeIter
        """
        self._model.remove(row)

    def __len__(self):
        """Gets the number of rows
        in the model

        @return: int
        """
        return len(self._model)
