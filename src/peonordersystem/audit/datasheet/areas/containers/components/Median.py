"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from collections import Counter


class CategoryMedian(object):
    """

    """

    def __init__(self):
        """

        @return:
        """
        self._data = Counter()

    @property
    def data(self):
        """

        @return:
        """
        return self._get_median()

    def _get_median(self):
        """

        @return:
        """
        if len(self._data) > 0:
            return self._get_median_data()
        return 0.0

    def _get_median_data(self):
        """

        @return:
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
        """

        @return:
        """
        values = self._data.values()
        return sorted(values)

    def update(self, category, value):
        """

        @param category:
        @param value:
        @return:
        """
        self._data[category] += value
