"""This module defines the wrapper
for wraping Format objects so that
they can be passed through the audit
system without interference.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.AuditFormat import AuditFormat


class XLFormat(AuditFormat):
    """Provides the functionality
    for accessing and processing
    xlsxwriter format data.
    """

    def __init__(self, xlsx_format_data):
        """Initializes the format with
        the given format data

        @param xlsx_format_data: xlsxwriter.Format
        object that represents the format data.
        """
        self._xlsx_format_data = xlsx_format_data

    @property
    def format_data(self):
        """Gets the stored format
        data.

        @return: xlsxwriter.Format
        object that represents
        the format data.
        """
        return self._xlsx_format_data
