"""This module stores the Abstract Base Class
used for defining the base functionality for
a Container object.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class Container(object):
    """Container objects store
    and process data for areas to
    display.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def data(self):
        """Gets the data associated
        with the container.
        """
        pass

    @abstractmethod
    def add(self, data):
        """Adds and processes the
        given data to the containers
        data.

        @param data: dataBundle object
        that represents the data to be
        added.
        """
        pass

    def get_data_format(self, format_data):
        """Gets the format used to display
        the containers data.

        @return: None
        """
        return None


def check_container(other_container):
    """Checks whether the given other container
    is a subclass of this Container base class.

    @raise TypeError: If given object is not a
    subclass of this Container defined here.

    @param other_container: object to be tested.

    @return: bool value representing if the
    test was passed.
    """
    if not other_container or issubclass(other_container, Container):
        curr_type = type(other_container)
        raise TypeError('Expected a Container subclass implementation. Received '
                        '{} instead.'.format(curr_type))
    return True
