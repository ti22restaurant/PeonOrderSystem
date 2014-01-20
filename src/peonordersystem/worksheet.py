"""Defines worksheet classes that are
used to wrap worksheet data and allow
worksheet data to be written to by
SpreadsheetAreas.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from copy import copy
from datetime import datetime
from xlsxwriter.utility import xl_range_abs

from src.peonordersystem.Settings import (OPEN_TIME, CLOSE_TIME, TIME_GROUPING)


class Worksheet(object):
    """Worksheet object is used to contain
    relevant worksheet data and provides the
    functionality of adding areas to the worksheet.

    @var row: int representing the current row
    that is considered valid for the worksheet.

    @var col: int representing the current column
    that is considered valid for the worksheet.

    @var areas: list of SpreadsheetArea objects
    that represent the areas associated with this
    worksheet.
    """

    def __init__(self, xlsx_worksheet):
        """Initialzies the Worksheet with
        the given xlsxwriter.worksheet.

        @param xlsx_worksheet: xlsxwriter.worksheet.Worksheet
        that this class will use as its baseline worksheet to
        perform the functionality on.
        """
        self.areas = []
        self._worksheet = xlsx_worksheet
        self.row = 0
        self.col = 0

    def add_area(self, spreadsheet_area):
        """Adds the given SpreadsheetArea to
        the worksheet.

        @param spreadsheet_area: SpreadsheetArea
        subclass that represents the area to be
        added.

        @return: None
        """
        self.areas.append(spreadsheet_area)
        self.row, self.col = spreadsheet_area.connect(self, row=self.row,
                                                      col=self.col)

    def write(self, row, column, data, format):
        """

        @param row:
        @param column:
        @param data:
        @param format:
        @return:
        """
        return self._worksheet.write(row, column, data, format)

    def set_row(self, row_number, row_height, **kwargs):
        """

        @param row_number:
        @param row_height:
        @param kwargs:
        @return:
        """
        return self._worksheet.set_row(row_number, row_height, **kwargs)

    def set_column(self, first_column, last_column, col_width, **kwargs):
        """

        @param first_column:
        @param last_column:
        @param col_width:
        @param kwargs:
        @return:
        """
        return self._worksheet.set_column(first_column, last_column, col_width,
                                          **kwargs)

    def merge_range(self, first_row, first_column, last_row, last_column, **kwargs):
        """

        @param first_row:
        @param first_column:
        @param last_row:
        @param last_column:
        @param kwargs:
        @return:
        """
        return self._worksheet.merge_range(first_row, first_column, last_row,
                                           last_column, **kwargs)


class DataWorksheet(Worksheet):
    """DataWorksheet class creates a hidden
    worksheet that is used to store and access
    data that represents intermediate steps for
    display data in specific forms.
    """
    HIDDEN_WORKSHEET_NAME = 'HiddenDataWorksheet'

    def __init__(self, worksheet, format_dict):
        """ Initializes the DataWorksheet object.

        @param worksheet: xlsxwriter.Worksheet subclass
        that will provide this area with its base
        functionality.

        @param format_dict: dict of xlsxwriter.Format
        objects that represent the formats for display
        data.
        """
        super(DataWorksheet, self).__init__(worksheet, format_dict)
        self._worksheet.name = self.HIDDEN_WORKSHEET_NAME
        self._worksheet.hide()

        self._time_keys = self._create_time_keys()
        self._time_keys_absolute_reference = None
        self._items_data_absolute_references = {}
        self._orders_data_absolute_referernces = {}

    def _generate_data(self, init_data):
        """Private Method

        initializes the Worksheet data.

        @param init_data: dict representing
        the keywords for the initialization
        of the xlsxwriter.Worksheet.

        @return: None
        """

        time_keys_range = self._create_time_keys_area(self._time_keys)
        self._time_keys_data_absolute_reference = \
            self._create_absolute_area_reference(time_keys_range)

    @property
    def time_keys(self):
        """Gets a copy of the time keys data.

        @return: list of datetime.time objects
        that represent the time keys.
        """
        return copy(self._time_keys)

    @property
    def time_keys_data(self):
        """Get the time keys data

        @return: str representing the
        cell reference to the time keys
        data.
        """
        return self._time_keys_data

    @property
    def items_data(self):
        """Gets the item data associated
        with this worksheet.

        @return: dict that maps datetime
        objects to str representing the cell
        data reference.
        """
        return copy(self._items_data)

    @property
    def orders_data(self):
        """Gets the order data associated
        with this worksheet.

        @return: dict that maps datetime objects
        to str representing the cell data reference.
        """
        return copy(self._orders_data)

    def _create_absolute_area_reference(self, cell_range):
        """Creates an absolute area reference separate from
        this worksheet.

        @param cell_range: str representing an absolute
        reference to the cell range.

        @return: str representing a reference independent
        of the worksheet or relative cell range.
        """
        return '=' + self._worksheet.get_name() + '!' + cell_range

    @staticmethod
    def _create_time_keys(start_time=OPEN_TIME, end_time=CLOSE_TIME,
                            time_increment=TIME_GROUPING):
        """Creates the time keys by incrementing the start time with
        the time increment until it reaches end time.

        @param start_time: datetime.time object that represents
        the starting time.

        @param end_time: datetime.time object that represents
        the ending time.

        @param time_increment: datetime.timedelta that
        represents the time increment grouping.

        @return: list of datetime.time objects where each
        index represents a generated grouping.
        """
        time_keys = []
        curr_time = datetime.combine(datetime.now(), start_time)
        final_time = datetime.combine(datetime.now(), end_time)

        while curr_time < final_time:
            time_keys.append(curr_time)
            curr_time += time_increment

        return time_keys

    def _create_time_keys_area(self, time_keys):
        """Creates the time keys area that displays
        the time keys steps in the DataWorksheet.

        @param time_keys: list of datetime.time objects
        that represents each time step.

        @return: str representing the absolute range of
        the created time keys area.
        """
        curr_row = self.row
        for time_step in time_keys:
            self._worksheet.write_datetime(curr_row, self.col, time_step,
                                          self.format_dict['time_format'])
            curr_row += 1

        data_range = xl_range_abs(self.row, self.col, curr_row, self.col)
        self.row = curr_row

        return data_range


def check_worksheet(worksheet):
    """Checks that the worksheet is
    an instance or subclass member
    of the Worksheet class

    @raise ValueError: If the given
    worksheet is not a subclass member or
    instance or Worksheet

    @return: bool value representing if
    the test was passed.
    """
    exp_type = Worksheet
    if not worksheet or not isinstance(worksheet, exp_type):
        curr_type = type(worksheet)
        raise ValueError('Expected connected worksheet to be an instance or '
                         'subclass of {} got {} instead'.format(exp_type,
                                                                curr_type))
    return True
