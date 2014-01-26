"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from .areas.KeyAreas import TimeKeysArea, DateKeysArea
from src.peonordersystem.audit.worksheet import Worksheet


class DataWorksheet(Worksheet):
    """DataWorksheet class creates a hidden
    worksheet that is used to store and access
    data that represents intermediate steps for
    display data in specific forms.
    """
    HIDDEN_WORKSHEET_NAME = 'HiddenDataWorksheet'

    def __init__(self, worksheet, format_data):
        """ Initializes the DataWorksheet object.

        @param worksheet: xlsxwriter.Worksheet subclass
        that will provide this area with its base
        functionality.

        @param format_data: dict of xlsxwriter.Format
        objects that represent the formats for display
        data.
        """
        super(DataWorksheet, self).__init__(worksheet, format_data)
        self.format_data = format_data

        self.time_keys = self._create_time_keys()

        self.items_data = {}
        self.orders_data = {}

        self._worksheet.name = self.HIDDEN_WORKSHEET_NAME
        #self._worksheet.hide()

    def _create_time_keys(self):
        """

        @return:
        """
        time_keys_area = TimeKeysArea()
        self.add_area(time_keys_area)
        return time_keys_area
