"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from datetime import time, datetime, timedelta

from src.peonordersystem.Settings import OPEN_TIME, CLOSE_TIME, TIME_GROUPING
from src.peonordersystem.audit.DatasheetAreas import DatasheetArea

class TimeKeys(DatasheetArea):
    """

    """

    def __init__(self, format_dict):
        """Initializes the object.

        @param format_dict: dict of str keys
        mapped to xlsxwriter.Format values
        representing the formats available
        for formating cells.
        """
        self.format_dict = format_dict

        data = self._create_time_keys()
        super(TimeKeys, self).__init__(data)

    def _get_data_value(self, data):
        """Gets the value associated
        with the data.

        @param data: datetime.datetime
        object that represents a time.

        @return: datetime.time that represents
        a time.
        """
        return data.time()

    def _create_time_keys(self, start_time=OPEN_TIME, end_time=CLOSE_TIME):
        """Creates the time keys by incrementing the start time with
        the time increment until it reaches end time.

        @param start_time: datetime.time object that represents
        the starting time.

        @param end_time: datetime.time object that represents
        the ending time.

        @return: list of datetime.time objects where each
        index represents a generated grouping.
        """
        time_keys = []
        curr_time = start_time
        final_time = end_time

        while curr_time < final_time:
            time_keys.append(curr_time)
            curr_time = self._get_next_time_step(curr_time)

        return time_keys

    def _get_next_time_step(self, current_time, time_increment=TIME_GROUPING):
        """Gets the next time step beyond the given time step.

        @param current_time: datetime.time that represents
        the current time step.

        @return: datetime.time that represents the next
        time step.
        """
        next_time = datetime.combine(datetime.now(), current_time) + time_increment
        next_time = next_time.time()

        if next_time < current_time:
            return time.max

        return next_time

    def _write_data_column(self):
        """Writes the current data in the
        areas column.

        @return: None
        """
        format = self._get_data_format()
        super(TimeKeys, self)._write_data_column(format=format)

    def _get_data_format(self):
        """Gets the data format
        associated with displaying
        the data.

        @return: xlsxwriter.Format
        that is used to format the
        cell data.
        """
        return self.format_dict['time_format']

