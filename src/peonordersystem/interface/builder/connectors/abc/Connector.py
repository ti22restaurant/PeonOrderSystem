"""This module provides the
abstract base class used in
defining the functionality for
a Connector object.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AbstractConnector(object):
    """Describes the required
    functionality for an object
    to be a useable Connector.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def connect(self, ref):
        """Connects the registered
        objects to the reference.

        @param ref: obj that contains
        the required functions for
        the registered object to connect
        to.

        @return: None
        """
        pass

    @abstractmethod
    def register(self, obj, flag, func_name, *args):
        """Registers an object for the connector
        to be connected with the given data.

        @param obj: Gtk.Object that is to be
        registered.

        @param flag: str repersenting the flag
        associated with the Gtk.Object that is
        to be registered.

        @param func_name: str representing the
        function name that the Gtk.Objecy will
        be connected to. This func_name is
        expected to be present in a connected
        reference.

        @param args: Wildcard used to catch
        and pass in any additional arguments
        that will be supplied to the function
        when the flag is triggered.

        @return: None
        """
        pass

