"""This module provides the components used
in generating date keys.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from datetime import datetime, time, timedelta

from .abc.Component import Component
from .abc.Creator import Creator
from peonordersystem.src.standardoperations import check_date_range


class DateCreator(Component, Creator):
    """Defines the functionality for
    generating Date keys.
    """
    DATE_INCREMENT = timedelta(days=1)

    def __init__(self, start_date, end_date):
        """Initializes a new DateCreator component,
        over which date keys will be generated.

        @param start_date: datetime.datetime that
        represents the starting date.

        @param end_date: datetime.datetime that
        represents the ending date.
        """
        self._start_date = start_date.date()
        self._end_date = end_date.date()
        self._data = tuple(self._create_date_keys())

    @property
    def data(self):
        """Gets the stored date
        keys data.

        @return: tuple of datetime.dates
        that represents the generated date
        keys.
        """
        return self._data

    def get_data_format(self, format_data):
        """Gets the format used to display the
        stored data entries.

        @param format_data: FormatData object
        representing the stored format data.

        @return: format that is used to display
        any given data index.
        """
        return format_data['date_format']

    def _create_date_keys(self):
        """Creates the date keys data.

        @return: list of datetime.dates that
        represents the date keys.
        """
        check_date_range(self._start_date, self._end_date)

        data = []
        curr_date = datetime.combine(self._start_date, time.min)

        while curr_date.date() < self._end_date:
            data.append(curr_date.date())
            curr_date += self.DATE_INCREMENT
        data.append(curr_date.date())

        return data

