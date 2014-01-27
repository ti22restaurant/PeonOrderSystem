"""This module defines the CollectionDataBundle
that represents orders data collected into
a bundle.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod, abstractproperty

from .DataBundle import DataBundle


class CollectionDataBundle(DataBundle):
    """CollectionDataBundle represents
    data packaged into a bundle that represents
    a single or multiple orders.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def togo_orders(self):
        """Gets the number of togo orders
        associated with this bundle.

        @return: int representing the number
        of togo orders associated with the
        bundle.
        """
        pass

    @abstractproperty
    def standard_orders(self):
        """Gets the number of standard
        orders associated with this
        bundle.

        @return: int representing the number
        of standard orders associated with
        the bundle.
        """
        pass
