"""Defines workbook classes that are
used to generate workbooks that present
data in an easy to digest format for users.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from peonordersystem.src.audit.adapters.spreadsheetWriter.XLWorkbook import \
    XLWorkbook

from peonordersystem.src.audit.auditbook.areas.general.ChartArea import ChartArea
from peonordersystem.src.audit.auditbook.specialitySheets.Datasheet import Datasheet


class Workbook(XLWorkbook):
    """Workbook class defines the basic workbook
    that represents the xlsx file to be displayed.
    """
    def __init__(self, file_name):
        """Initializes the workbook with the given
        name.

        @param file_name: str representing the file
        name that the workbook should be saved as.
        """
        super(Workbook, self).__init__(file_name)

    def _create_data_worksheet(self):
        """Creates the datasheet

        @return: Datasheet area.
        """
        ws = self._workbook.add_worksheet('Datasheet')
        return Datasheet(ws, self.formats)

    def add_chart(self, name=None):
        """

        @param name:
        @return:
        """
        chart = super(Workbook, self).add_chart(name)
        return ChartArea(chart)
