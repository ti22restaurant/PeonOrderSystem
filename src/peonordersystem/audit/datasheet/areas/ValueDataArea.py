"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from copy import copy
from .DataAreas import DataArea
from src.peonordersystem.audit.datasheet.parsers.PackagedDataParser import \
    PackagedDataParser



class ValueDataArea(DataArea):
    """Represents a ValueDataArea stored
    inside of the datasheet that is used
    to display a column of data.

    This area categorized the data by the
    key value's range it is within.
    """

    def __init__(self, packaged_data_parser, data_keys):
        """Initializes the ValueDataArea with the
        given data keys.

        @param packaged_data_parser: DataParser
        subclass that represents the functions for
        pulling values from given package data.

        @param data_keys: list representing the
        data keys associated with the area. This
        list is expected to be in pre-categorized
        order.
        """
        self._check_package_value(packaged_data_parser)
        self._data_parser = packaged_data_parser
        self._data_keys = tuple(data_keys)
        data = self._fill_data_list_values()
        super(ValueDataArea, self).__init__(data)

    @property
    def data_keys(self):
        """Gets the data keys associated with
        this data area.

        @return: tuple of data keys.
        """
        return self._data_keys

    def _check_package_value(self, package_value):
        """Checks if the given package value is of
        the expected subclass.

        @param package_value: object that is to be
        tested if it is an instance or subclass of
        DataParser

        @return: bool representing if the test was
        passed.
        """
        if not package_value or not isinstance(package_value, PackagedDataParser):
            curr_type = type(package_value)
            raise ValueError('Expected instance of DataParser to be given for '
                             'ValueDataArea. Received {} instead.'.format(curr_type))

        return True

    def _fill_data_list_values(self):
        """Fills the given data list by ensuring it is of equal
        length to the data keys. Each value inserted will be zero.

        @param data: list of values that represent the data
        to be stored as the areas data.

        @return: list of values that represents the data list.
        The length of the list will match the length of the
        stored keys.
        """
        return [0 for x in range(len(self._data_keys))]

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
            else:
                return mid_index + self._find_key_index_helper(sublist[mid_index:],
                                                               value)

        return 0

    def _get_data_value(self, data):
        """Gets the value associated with
        the data.

        @param data: PackagedData that is to
        have its value obtained.

        @return: value associated with the
        PackagedData.
        """
        return self._data_parser.get_data_value(data)

    def _get_data_comparison_value(self, data):
        """Gets the value associated with the
        data comparison.

        @param data: PackagedData to have the
        value obtained from it.

        @return: value representing the data
        comparison.
        """
        return self._data_parser.get_data_comparison_value(data)