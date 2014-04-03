"""This module defines the
abstract base class of a model.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractModel(object):
    """Desribes the functionality
    necessary for an object to be
    a useable model.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def data(self):
        """Gets the data that is being
        operated on.

        @return: data
        """
        pass

    @abstractproperty
    def model(self):
        """Gets the model that
        is associated with this
        area.

        @return: Gtk.TreeModel
        """
        pass

    def __getitem__(self, itr):
        """Gets the value stored
        at the itr.

        @param itr: Gtk.TreeIter
        that represents the iter
        whose value should be
        retrieved.

        @return: value stored at
        the iter.
        """
        value, = self.model[itr]
        return value

    @abstractmethod
    def add(self, data):
        """Adds the given data
        to the model for storage
        and display

        @param data: data to be
        added.

        @return: Gtk.TreeIter
        pointing to the row
        that was added to the
        model.
        """
        pass

    @abstractmethod
    def remove(self, itr):
        """Removes the value
        at the given iter from
        the model and data.

        @param itr: Gtk.TreeIter
        pointing to the row data
        to be removed.

        @return: value removed at
        the row corresponding to
        the iter given.
        """
        pass

    def __iter__(self):
        """Gets an iter over
        the data stored in the
        model.

        @return: Gtk.TreeRowReference
        """
        return iter(self.model)