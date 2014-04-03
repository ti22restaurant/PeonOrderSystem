"""This module defines the abstract base
class for containers.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AreaContainer(object):
    """Describes the required methods
    for a container to be useable as
    such.
    """

    __metaclass__ = ABCMeta

    @abstractmethod
    def update(self, data):
        """Updates the data of the
        container.

        @param data: data to be
        updated.

        @return: None
        """
        pass

    @abstractmethod
    def finalize(self):
        """Finalizes the component.

        @return: None
        """
        pass
