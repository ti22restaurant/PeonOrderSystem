"""KeyAreas represents areas
that specifically are used for
storing key data.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from datetime import time, datetime, timedelta

from .DataAreas import DataArea
from src.peonordersystem.Settings import OPEN_TIME, CLOSE_TIME, TIME_GROUPING


class TimeKeysArea(DataArea):
    """TimeKeysArea represents key data categorized
    by time.
    """

    def __init__(self):
        """Initializes the object.

        @param format_data: dict of str keys
        mapped to xlsxwriter.Format values
        representing the formats available
        for formating cells.
        """
        data = self._create_time_keys()
        super(TimeKeysArea, self).__init__(data)

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
        super(TimeKeysArea, self)._write_data_column(format=format)

    def _get_data_format(self):
        """Gets the data format
        associated with displaying
        the data.

        @return: xlsxwriter.Format
        that is used to format the
        cell data.
        """
        return self.format_data['time_format']


class DateKeysArea(DataArea):
    """DatekeysArea represents the key data
    categorized by date.
    """

    def __init__(self, start_date, end_date):
        """Initializes the DateKeysArea object.

        @param start_date: datetime.date representing
        the start date that the date keys should be
        generated over. Inclusive.

        @param end_date: datetime.date representing the
        end date that the date keys should be generated
        over. Inclusive.
        """
        data = self._create_date_keys(start_date, end_date)
        super(DateKeysArea, self).__init__(data)

    def _get_data_value(self, data):
        """Gets the value associated with
        the relevant data.

        @param data: datetime.datetime that
        represents the data to be parsed

        @return: datetime.date that represents
        the value type associated with these
        keys.
        """
        return data.date()

    def _create_date_keys(self, start_date, end_date):
        """Creates the date keys data.

        @param start_date: datetime.date that represents
        the start date for the date keys. Inclusive.

        @param end_date: datetime.date that represents
        the end date for the date keys. Inclusive.

        @return: list of datetime.date that represents
        the date keys.
        """
        date_keys = []

        curr_date = start_date

        while curr_date <= end_date:
            date_keys.append(curr_date)
            curr_date += timedelta(days=1)

        return date_keys

    def _write_data_column(self):
        """Writes the data to the column
        associated with the DataArea.

        @return: None
        """
        format = self._get_data_format()
        super(DateKeysArea, self)._write_data_column(format)

    def _get_data_format(self):
        """Gets the format associated with
        displaying the data.

        @return: xlsxwriter.Format used to
        display the date keys data.
        """
        return self.format_data['date_format']
