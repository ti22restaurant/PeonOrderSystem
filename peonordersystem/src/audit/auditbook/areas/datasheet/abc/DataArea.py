"""This module defines the abstract base
class for the DataArea.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import abstractmethod, abstractproperty

from peonordersystem.src.audit.auditbook.areas.abc.Area import Area


class AbstractDataArea(Area):
    """Describes the required functionality
    for an Area to be a DataArea.
    """

    @abstractproperty
    def data(self):
        """Gets the data associated
        with the area.

        @return: data associated
        with the area.
        """
        pass

    @abstractmethod
    def get_data_cells_reference(self):
        """Gets the data cells reference.

        @return: str
        """
        pass
