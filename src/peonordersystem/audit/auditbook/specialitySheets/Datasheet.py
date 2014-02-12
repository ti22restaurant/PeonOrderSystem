"""This module defines the special worksheet
that is defined as a Datasheet.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from src.peonordersystem.audit.auditbook.areas.datasheet.DataAreas \
    import DataArea
from src.peonordersystem.audit.auditbook.areas.datasheet.containers.KeyContainer \
    import KeyContainer
from src.peonordersystem.audit.adapters.spreadsheetWriter.XLWorksheet \
    import XLWorksheet


class Datasheet(XLWorksheet):
    """Datasheet class creates a hidden
    worksheet that is used to store and access
    data that represents intermediate steps for
    display data in specific forms.
    """
    HIDDEN_WORKSHEET_NAME = 'Datasheet'

    def __init__(self, worksheet, format_data):
        """ Initializes the Datasheet object.

        @param worksheet: xlsxwriter.Worksheet subclass
        that will provide this area with its base
        functionality.

        @param format_data: dict of xlsxwriter.Format
        objects that represent the formats for display
        data.
        """
        super(Datasheet, self).__init__(worksheet, format_data)
        self.format_data = format_data

        self.time_keys = self._create_time_keys()
        self.date_keys = None

        self.items_data = {}
        self.orders_data = {}

        self._worksheet.name = self.HIDDEN_WORKSHEET_NAME

    def _create_time_keys(self):
        """Creates the time keys
        and stores them in this
        datasheet as an area.

        @return: None
        """
        key_container = KeyContainer('TIMES')
        time_keys_area = DataArea(key_container)
        self.add_area(time_keys_area)
        return time_keys_area

    def create_date_keys(self, start_date, end_date):
        """Creates the date keys spanning the given
        dates and stores them in this datasheet
        as an area.

        @return: None
        """
        key_container = KeyContainer('DATES', start_date, end_date)
        date_keys_area = DataArea(key_container)
        self.add_area(date_keys_area)
        self.date_keys = date_keys_area
        return date_keys_area
