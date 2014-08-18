"""This module defines the abstract external
facing interface for the model

@author: Carl McGraw
@contact: cjmcgraw(- at -)u.washington.edu
@version: 1.x
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class AbstractModel(object):
    """Describes the required functionality
    for a class to be a useable Model
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def model(self):
        """Gets the model

        @return: Gtk.TreeModel
        """
        pass

    @abstractmethod
    def append(self, row):
        """Appends the given row
        to the model

        @param row: tuple representing
        the values of the row to be
        added

        @return: Gtk.TreeIter pointing
        to the row added
        """
        pass

    @abstractmethod
    def insert(self, itr, row):
        """Insers the given row
        at the given iter

        @param itr: Gtk.TreeIter

        @param row: tuple representing
        the values of the row to be
        inserted

        @return: Gtk.TreeIter pointing
        to the row inserted
        """
        pass

    @abstractmethod
    def __getitem__(self, itr):
        """Gets the row stored at
        the location of the given
        iter

        @param itr: Gtk.TreeIter
        pointing to a row

        @return: tuple of values
        representing the row
        """
        pass

    @abstractmethod
    def __setitem__(self, itr, row):
        """Sets the item at the given
        iter to the given row.

        @param itr: Gtk.TreeIter
        pointing to the row to set

        @param row: tuple of values
        representing the row data

        @return: Gtk.TreeIter pointing
        to the value set
        """
        pass

    @abstractmethod
    def __delitem__(self, itr):
        """Deletes the data at the
        given iter

        @param itr: Gtk.TreeIter to
        be deleted

        @return: bool value representing
        if the row was removed
        """
        pass

    @abstractmethod
    def __iter__(self):
        """Gets an iter over the
        rows of the model

        @return: iterator
        """
        pass

    @abstractmethod
    def __len__(self):
        """Gets the length of
        the models data

        @return: int
        """
        pass