"""This module defines an adapter
that faces the external library to
wrap the libraries workbook into a
useable AuditWorkbook.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
#Imported external library objects that are being replaced
import xlsxwriter

from .abc.AuditWorkbook import AuditWorkbook

from .XLChart import XLChart
from .XLFormat import XLFormat
from .XLFormatter import XLFormatter
from .XLWorksheet import XLWorksheet

from .parsers.ChartDataParser import ChartDataParser


class XLWorkbook(AuditWorkbook):
    """XLWorkbook is used as an
    implementation of the external
    facing interface that integrates
    external library functions into a
    useable form for the audit.
    """

    def __init__(self, file_name):
        """Initializes the XLWorkbook with
        the given file name

        @param file_name: str representing
        the file name
        """
        self._workbook = xlsxwriter.Workbook(file_name)
        self._format_data = self._create_format_data()
        self._datasheet = self._create_data_worksheet()

    def _create_format_data(self):
        """Creates the format data
        that will be stored in this
        object.

        @return: XLFormat object that
        represents the formats that
        can be displayed.
        """
        # ref is necessary because xlsxwriter requires
        # the formats to be written to the workbook.
        # This is the most lightweight way of passing
        # the needed information to the separate formats
        # object.
        add_format_ref = self._add_format
        return XLFormatter(add_format_ref)

    def _add_format(self, format_properties):
        """

        @param format_options:
        @return:
        """
        frmt = self._workbook.add_format(format_properties)
        return XLFormat(frmt)

    def _create_data_worksheet(self):
        """Creates the datasheet area

        @return: XLWorksheet that represents
        the datasheet.
        """
        worksheet = self.add_worksheet('datasheet')
        return worksheet

    @property
    def datasheet(self):
        """Gets the hidden datasheet
        that is used for hidden value
        storage and calculations.

        @return: XLWorksheet that
        represents the datasheet.
        """
        return self._datasheet

    @property
    def formats(self):
        """Gets the format data that
        represents the formats that
        may be applied to cells.

        @return: XLFormat that represents
        the associated formats.
        """
        return self._format_data

    def add_worksheet(self, sheet_name):
        """Adds a worksheet with the given
        name to the workbook.

        @param sheet_name: str representing
        the name that the created worksheet
        should have.

        @return: XLWorksheet that represents
        the created worksheet.
        """
        ws = self._workbook.add_worksheet(sheet_name)
        self._check_hide_datasheet(ws)
        return XLWorksheet(ws, self.formats)

    def _check_hide_datasheet(self, worksheet):
        """Checks and hides the datasheet.

        @param worksheet: xlsxwriter.Worksheet
        to be hidden.

        @return: None
        """
        if self._datasheet._worksheet.hidden:
            self._datasheet._worksheet.hide()
            worksheet.activate()

    def add_chart(self, name=''):
        """Adds a chart with the given options
        and name to the workbook.

        @param chart_options: dict representing the
        options that are associated with the newly
        created chart.

        @keyword name: str representing the name that
        can be associated with the chart. Default is
        None.

        @return: XLChart that represents the newly
        created chart.
        """

        chart_options = ChartDataParser.default_chart_options()
        chrt = self._workbook.add_chart(chart_options)
        return XLChart(chrt, name)

    def close(self):
        """Closes the workbook.

        @return: None
        """
        self._workbook.close()
