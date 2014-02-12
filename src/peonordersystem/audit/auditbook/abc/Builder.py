"""This module defines the abstract base
class for the Builder.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta

from src.peonordersystem.audit.auditbook.workbooks.workbook import Workbook
from src.peonordersystem.audit.adapters.data.OrderData import OrderData


class Builder(object):
    """Describes the base functionality
    and required methods for an object
    to be a useable builder.
    """

    __metaclass__ = ABCMeta

    def __init__(self, workbook_name):
        """Initializes the builder with the
        given name.

        @param workbook_name: str representing
        the name that the workbook should be
        saved as.

        @return:
        """
        self.workbook = Workbook(workbook_name)
        self._creators = []

    def add(self, creator):
        """Adds a creator to the builder.

        @param creator: Creator subclass
        that is to be added to the builder.

        @return: None
        """
        self._creators.append(creator)

    def update(self, data):
        """Updates the creator data
        with the given data.

        @param data: data to be updated.

        @return: None
        """
        wrapped_data = self._wrap_data(data)
        for creator in self._creators:
            creator.update(wrapped_data)

    def _wrap_data(self, data):
        """Wraps the given data as
        an OrderData adapter.

        @param data: CollectionDataBundle
        subclass that can be wrapped by
        OrderData

        @return: OrderData that has wrapped
        the given data.
        """
        return OrderData(data)

    def finalize(self):
        """Finalizes the creators.

        @return: None
        """
        for creator in self._creators:
            creator.finalize()

