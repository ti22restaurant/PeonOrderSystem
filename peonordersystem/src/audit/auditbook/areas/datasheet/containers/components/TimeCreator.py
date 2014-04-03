"""This module defines the TimeCreator
object.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from datetime import datetime, time

from .abc.Creator import Creator
from .abc.Component import Component
from peonordersystem.src.standardoperations import check_time_range
from peonordersystem.src.Settings import OPEN_TIME, CLOSE_TIME, TIME_GROUPING


class TimeCreator(Component, Creator):
    """Creates and stores time values
    ranging from the given start time
    until the given stop time.
    """

    TIME_INCREMENT = TIME_GROUPING

    def __init__(self, start_time=OPEN_TIME, end_time=CLOSE_TIME):
        """Initializes the new TimeCreator.

        @keyword start_time: datetime.time representing
        the starting time for the time creator to generate
        time keys over.

        @keyword end_time: datetime.time representing the
        ending time fort he time creator to generate keys
        over.
        """
        self._start_time = start_time
        self._end_time = end_time
        self._data = tuple(self._create_time_keys())

    @property
    def data(self):
        """Gets the stored
        time keys.

        @return: tuple of datetime.time
        objects representing the created
        time.
        """
        return self._data

    def get_data_format(self, format_data):
        """Gets the format data to display the
        created data.

        @param format_data: FormatData object
        that represents the stored format data.

        @return: Format data to be used to display
        the format.
        """
        return format_data['time_format']

    def _create_time_keys(self):
        """Creates the time keys by incrementing the start time with
        the time increment until it reaches end time.

        @param start_time: datetime.time object that represents
        the starting time.

        @param end_time: datetime.time object that represents
        the ending time.

        @return: list of datetime.time objects where each
        index represents a generated grouping.
        """
        check_time_range(self._start_time, self._end_time)
        time_keys = []
        curr_time = self._start_time
        final_time = self._end_time

        while curr_time < final_time:
            time_keys.append(curr_time)
            curr_time = self._get_next_time_step(curr_time)

        return time_keys

    def _get_next_time_step(self, current_time):
        """Gets the next time step beyond the given time step.

        @param current_time: datetime.time that represents
        the current time step.

        @return: datetime.time that represents the next
        time step.
        """
        next_time = datetime.combine(datetime.now(), current_time)
        next_time += self.TIME_INCREMENT
        next_time = next_time.time()

        if next_time < current_time:
            return time.max

        return next_time


