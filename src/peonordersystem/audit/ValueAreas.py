"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from copy import copy
from abc import ABCMeta, abstractmethod

from src.peonordersystem.audit.DatasheetAreas import DatasheetArea

class ValueArea(DatasheetArea):
    """

    """

    __metaclass__ = ABCMeta

    def __init__(self, data_keys, data=[]):
        """Initializes the DatasheetArea with the
        given data keys.

        @param data_keys: list representing the
        data keys associated with the area. This
        list is expected to be sorted.

        @keyword data: list representing the data
        associated with the area. The data is expected
        to already have been parsed such that it holds
        a one to one correspondence with the keys.
        """
        self._data_keys = data_keys
        data = data + [0 for x in range(len(data), len(data_keys))]
        print data
        super(ValueArea, self).__init__(data)

    def keys(self):
        """Gets the a list of keys that
        are associated with this data area.

        @return: list of keys that represent
        the keys associated with the data area.
        """
        return copy(self._data_keys)

    def values(self):
        """Gets a list of values that
        are associated with this data area.

        @return: list of values that represent
        the values associated with the data area.
        """
        return copy(self._data)

    def insert(self, data):
        """Inserts the data into the
        values. The data will have its
        value extracted and placed in the
        representative spot.

        @param data: value representing the
        data to be inserted

        @return: None
        """
        row = self._insert_data_value(data)
        self._update_row(row)

    def _insert_data_value(self, data):
        """Inserts the data value into the
        appropriate spot.

        @param data: data representing the
        data to be inserted into the values.

        @return: None
        """
        index = self._find_key_index(data)
        self[index] += self._get_data_value(data)
        return index

    def _find_key_index(self, data):
        """Finds the associated index that this
        given data should be mapped under the
        keys as.

        @param data: data to find associated
        position.

        @return: int representing the index that
        the data should be associated with.
        """
        value = self._get_data_comparison_value(data)
        return self._find_key_index_helper(self._data_keys, value)

    def _find_key_index_helper(self, sublist, value):
        """Finds the index by parsing the potential
        data keys that this data could be associated
        with.

        @param sublist: collection representing the
        keys data to parse to find an associated
        value.

        @param value: value representing the comparison
        value that should be compared to the keys.

        @return: int representing the index that
        represents the category or key that the
        associated value should be indexed under.
        """
        if len(sublist) > 1:
            mid_index = len(sublist) / 2
            mid_value = sublist[mid_index]

            if value < mid_value:
                return self._find_key_index_helper(sublist[:mid_index], value)
            elif value >= mid_value:
                return mid_index + self._find_key_index_helper(sublist[mid_index:],
                                                               value)

        return 0

    @abstractmethod
    def _get_data_comparison_value(self, data):
        """Gets the value associated with the
        data comparison.

        @param data: data to have the value drawn
        from it.

        @return: value representing the data
        comparison.
        """
        pass


class OrdersTimeArea(ValueArea):
    """

    """
    def __init__(self, data_keys):
        """

        @param data_keys:
        @return:
        """
        super(OrdersTimeArea, self).__init__(data_keys)

    def _get_data_value(self, packaged_data):
        """

        @param packaged_data:
        @return:
        """
        return 1

    def _get_data_comparison_value(self, packaged_data):
        """

        @param packaged_data:
        @return:
        """
        return packaged_data.time


class ItemsTimeArea(ValueArea):
    """

    """
    def __init__(self, data_keys):
        """

        @param data_keys:
        @return:
        """
        super(ItemsTimeArea, self).__init__(data_keys)

    def _get_data_value(self, packaged_data):
        """

        @param packaged_data:
        @return:
        """
        return len(packaged_data)

    def _get_data_comparison_value(self, packaged_data):
        """

        @param packaged_data:
        @return:
        """
        return packaged_data.time


class TotalsTimeArea(ValueArea):
    """

    """
    def __init__(self, data_keys):
        """

        @param data_keys:
        @return:
        """
        super(TotalsTimeArea, self).__init__(data_keys)

    def _get_data_value(self, packaged_data):
        """

        @param packaged_data:
        @return:
        """
        return packaged_data.totals['total']

    def _get_data_comparison_value(self, packaged_data):
        """

        @param packaged_data:
        @return:
        """
        return packaged_data.time