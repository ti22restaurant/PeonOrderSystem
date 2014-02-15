"""This module provides the Abstract Base Class
for a component.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from abc import ABCMeta, abstractproperty


class Component(object):
    """This class defines the
    base functionality required
    to be a component for a container.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def data(self):
        """Abstract Property.

        Defines the data stored
        in the component.
        """
        pass
