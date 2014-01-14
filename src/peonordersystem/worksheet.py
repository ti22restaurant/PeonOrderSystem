"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from copy import copy, deepcopy
from datetime import datetime, time, timedelta
from xlsxwriter.worksheet import Worksheet as xlsx_Worksheet
from xlsxwriter.utility import xl_rowcol_to_cell, xl_range_abs

from src.peonordersystem.Settings import (OPEN_TIME, CLOSE_TIME, TIME_GROUPING)


class Worksheet(xlsx_Worksheet):
    """Worksheet class used for writing Excel
    data as XLSX and tracking row and column
    data.

    @var row: int representing the row that it
    is currently safe to append to.

    @var col: int representing the column that
    it is currently safe to append to.
    """



    def __init__(self, format_dict):
        """

        @return:
        """
        self.format_dict = format_dict
        super(Worksheet, self).__init__()

    def _initialize(self, init_data):
        """

        @param init_data:
        @return:
        """
        self.row = 0
        self.col = 0
        return super(Worksheet, self)._initialize(init_data)


class DisplayWorksheet(Worksheet):
    """

    """

    def __init__(self, format_dict):
        """
        """
        self.areas = []
        super(DisplayWorksheet, self).__init__(format_dict)

    def _initialize(self, init_data):
        """

        @param init_data:
        @return:
        """
        super(DisplayWorksheet, self)._initialize(init_data)

    def add_area(self, spreadsheet_area):
        """
        """
        self.row, self.col = spreadsheet_area.connect(self)


class DataWorksheet(Worksheet):
    """

    """
    HIDDEN_WORKSHEET_NAME = 'HiddenDataWorksheet'

    def __init__(self, format_dict):
        """ Initializes the DataWorksheet object.
        """
        self._time_keys = self._create_time_keys()
        self._time_keys_absolute_reference = None
        self._items_data_absolute_references = {}
        self._orders_data_absolute_referernces = {}
        super(DataWorksheet, self).__init__(format_dict)

    def _initialize(self, init_data):
        """Private Method

        initializes the Worksheet data.

        @param init_data: dict representing
        the keywords for the initialization
        of the xlsxwriter.Worksheet.

        @return: None
        """
        init_data['name'] = self.HIDDEN_WORKSHEET_NAME
        super(DataWorksheet, self)._initialize(init_data)
        #self.hide()

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
        return '=' + self.get_name() + '!' + cell_range

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
            self.write_datetime(curr_row, self.col, time_step,
                                self.format_dict['time_format'])
            curr_row += 1

        data_range = xl_range_abs(self.row, self.col, curr_row, self.col)
        self.row = curr_row

        return data_range


class GeneralDateWorksheet(Worksheet):
    """

    """

    def __init__(self):
        """

        @return:
        """
        pass


class OverviewDateWorksheet(Worksheet):
    """

    """

    def __init__(self):
        """

        @return:
        """
        pass


class OverviewAuditWorksheet(Worksheet):
    """

    """
    def __init__(self):
        """

        @return:
        """
        pass
