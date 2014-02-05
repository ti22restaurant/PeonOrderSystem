"""This module defines the Median
components used to process and store
median data.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from collections import Counter

from .abc.Component import Component
from .abc.Updater import Updater


class CategoryMedian(Component, Updater):
    """CategoryMedian class stores and processes
    median data based on given categories.
    """

    def __init__(self):
        """Initializes the CategoryMedian"""
        self._data = Counter()

    @property
    def data(self):
        """Gets the data representing
        the associated Median value.

        @return: float representing
        the median associated with
        this component.
        """
        return self._get_median()

    def _get_median(self):
        """Gets the median.

        @return: float representing
        the median.
        """
        if len(self._data) > 0:
            return self._get_median_data()
        return 0.0

    def _get_median_data(self):
        """Gets the median data from
        the stored data.

        @return: float representing the
        median.
        """
        sublist = self._get_data_values()
        if len(sublist) % 2 == 0:
            mid_index = len(sublist) / 2
            value1 = sublist[mid_index - 1]
            value2 = sublist[mid_index]
            return round((value1 + value2) / 2.0, 4)
        else:
            return sublist[len(sublist) / 2]

    def _get_data_values(self):
        """Gets the sorted total
        values stored in this area.
        This is used to generate the
        median.

        @return: list of sorted values
        representing the data set.
        """
        values = self._data.values()
        return sorted(values)

    def update(self, category, value):
        """Updates the given category
        with the given value.

        @param category: key representing
        the category to be updated.

        @param value: float or int representing
        the value to be added to the median data.

        @return: None
        """
        self._data[category] += value
