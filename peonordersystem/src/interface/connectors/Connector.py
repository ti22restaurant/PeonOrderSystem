""" This module provides the
Connector class that is used
to register objects that are to
be connected to a reference object.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.Connector import AbstractConnector


class Connector(AbstractConnector):
    """Registers objects in preparation
    for them to be connected to a reference
    object that has the required attributes.
    Upon connection the registered objects are
    connected.
    """

    def __init__(self):
        """initializes the connector"""
        self._connection_data = {}
        self._ref = None

    def connect(self, ref):
        """Connects the registered
        objects to the reference.

        @param ref: obj that contains
        the required functions for
        the registered object to connect
        to.

        @return: None
        """
        self._ref = ref
        self._connect_registered_objs()

    def _connect_registered_objs(self):
        """Connects the registered objects.

        @return: None
        """
        for obj, (signals, func_name, args) in self._connection_data.items():
            func = getattr(self._ref, func_name)
            obj.connect(signals, func, *args)

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
        self._connection_data[obj] = (flag, func_name, args)
