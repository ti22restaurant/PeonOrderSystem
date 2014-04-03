"""This module defines the abstract
base class for the wrapper that
provides an adapter fro the format.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractproperty


class AuditFormat(object):
    """Describes the wrapper
    for format data that provides
    access to the format data when
    necessary
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def format_data(self):
        """Gets the format data
        stored in this AuditFormat.

        @return: xlsxwriter.Format
        data stored in the format
        object.
        """
        pass
