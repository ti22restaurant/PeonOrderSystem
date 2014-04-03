"""This module defines the abstract base
class for a container.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AreaContainer(object):
    """Describes the container abstract
    base class that defines the methods
    necessary to be a useable AreaContainer.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, data):
        """Updates the area container.

        @param data: data that the
        container is to be updated
        with.

        @return: None
        """
        pass

    @abstractmethod
    def finalize(self):
        """Finalizes the container.

        @return: None
        """
        pass
