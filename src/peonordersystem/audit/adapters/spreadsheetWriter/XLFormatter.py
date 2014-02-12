"""This module defines the XLFormatter
that is used to wrap and retrieve XLFormat
data easily.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.AuditFormatter import AuditFormatter

from .parsers.FormatDataParser import FormatDataParser


class XLFormatter(AuditFormatter):
    """Provides the basic functionality
    for storing, creating and retrieving
    XLFormat objects.
    """

    def __init__(self, add_format_ref):
        """Initializes the formatter.

        @param add_format_ref: function reference
        that is used to add new formats.
        """
        self._add_format_ref = add_format_ref
        self._format_data_parser = FormatDataParser()
        self._formats = self._create_formats()

    def _create_formats(self):
        """Creates the formats that will be
        stored in the formatter object.

        @return: dict that represents the
        key and XLFormat values respectively.
        """
        data = {}
        format_data = self._format_data_parser.get_format_data()
        for key_name, values in format_data.items():
            data[key_name] = self._add_format_ref(values)

        return data

    def __getitem__(self, key):
        """Gets the format stored
        at the given key.

        @param key: str representing
        the key that the format is
        stored under.

        @return: XLFormat that is
        associated with the given key.
        """
        return self._formats[key]
