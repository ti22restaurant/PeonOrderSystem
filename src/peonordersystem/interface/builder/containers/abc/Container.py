"""This module defines the abstract base
class for containers.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AbstractContainer(object):
    """Describes the abstract base
    class that defines the necessary
    functionality for an object to
    be a useable container.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def add(self, component):
        """Adds the component to the
        container.

        @param component: AbstractComponent
        subclass that is to be added to
        this container.

        @return: None
        """
        pass
