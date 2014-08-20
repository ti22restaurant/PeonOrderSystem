"""This module defines the AbstractController
class

@author: Carl McGraw
@contact: cjmcgraw(- at -)u.washington.edu
@version: 1.x
"""
from abc import ABCMeta, abstractmethod


class AbstractController(object):
    """Describes the required functionality
    for an object to be a useable Controller
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def set_properties(self, **kwargs):
        """Sets the properties associated
        with the controller

        @param args: catchall for all standard
        arguments

        @param kwargs: catchall for all keyword
        arguments
        """
        pass

    @abstractmethod
    def get_properties(self):
        """Gets the properties associated
        with the dialog window. This is where
        the results of the confirmation window
        will be stored - including what response
        was emitted.

        @return: dict representing the properties
        associated with the dialog window
        """
        pass

    @abstractmethod
    def run(self):
        """Runs the dialog window
        with the set properties.

        @return: Gtk.ResponseType
        representing if the dialog
        was confirmed or
        """
        pass