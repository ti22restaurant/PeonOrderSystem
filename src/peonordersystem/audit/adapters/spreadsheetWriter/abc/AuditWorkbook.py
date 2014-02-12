"""This module defines the abstract
base class that is the interface through
which the audit operates on a workbook.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class AuditWorkbook(object):
    """Describes the required
    properties and methods for
    a class to be a useable
    AuditWorkbook.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def formats(self):
        """Gets the formats that
        apply formatting to a
        given cell.

        @return: AuditFormat object.
        """
        pass

    @abstractproperty
    def datasheet(self):
        """Gets the datasheet
        that represents the hidden
        sheet through which data
        and necessary calculations
        can be made.

        @return: AuditWorksheet object.
        """
        pass

    @abstractmethod
    def add_worksheet(self, sheet_name):
        """Adds a worksheet to the workbook
        with the given name

        @param sheet_name: str representing
        the name to be associated with the
        created worksheet.

        @return: AuditWorksheet object
        """
        pass

    @abstractmethod
    def add_chart(self, chart_options, name=None):
        """Adds a chart to the workbook with
        the given data and name.

        @param chart_options: dict representing
        the options associated with the chart.

        @keyword name: str representing the name
        that the chart should be associated with.

        @return: AuditChart object.
        """
        pass

    @abstractmethod
    def close(self):
        """Closes the workbook.

        @return: None
        """
        pass
