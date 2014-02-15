"""This Module defines the abstract base
class for any AuditComponent.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class AuditComponent(object):
    """Describes the abstract base
    classes required methods to be
    useable as an AuditComponent.
    """

    __metaclass__ = ABCMeta

    def __init__(self, worksheet):
        """Initializes a new AuditComponent
        with the given worksheet.
        """
        self._worksheet = worksheet

    @abstractmethod
    def update(self, data):
        """Updates the component with
        the given data.
        """
        pass

    @abstractmethod
    def finalize(self):
        """Finalizes the component"""
        pass