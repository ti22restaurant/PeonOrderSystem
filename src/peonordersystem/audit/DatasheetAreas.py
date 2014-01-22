"""THis module contains classes
used for generating Datasheet
areas.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from copy import copy
from abc import ABCMeta, abstractmethod
from xlsxwriter.utility import xl_range_abs

from src.peonordersystem.audit.PackageValues import (PackageValue,
                                                     ItemsTimePackageValue,
                                                     OrdersTimePackageValue,
                                                     TotalsTimePackageValue)


class DatasheetArea(object):
    """Abstract Base Class

    Represents an area used for displaying
    data inside of the data sheet.
    """

    __metaclass__ = ABCMeta

    def __init__(self, data):
        """Initializes the DatasheetArea with the
        given data keys.

        @keyword data: list representing the data
        associated with the area. The data is expected
        to already have been parsed such that it holds
        a one to one correspondence with the keys.
        """
        self.format_data = None
        self._data = data
        self.row = len(self._data)

        self._initial_row = None
        self._initial_col = None
        self._worksheet = None

    @property
    def data(self):
        """

        @return:
        """
        return copy(self._data)

    def __getitem__(self, index):
        """Gets the stored value at the
        given index.

        @param index: int representing the associated
        index that data should be gathered from.

        @return: data stored at the specified index.
        """
        return self._data[index]

    def __setitem__(self, key, value):
        """Sets the item value at the given
        index.

        @param key: int representing the index

        @param data: data representing the
        value to be set.

        @return: None
        """
        self._data[key] = value
        self._update_row(key)

    @abstractmethod
    def _get_data_value(self, data):
        """Abstract Method.

        Gets the associated data from the
        value.

        @param data: representing the
        data to have its value extracted.

        @return: value representing the
        value associated with the data.
        """
        pass

    def _update_row(self, row):
        """Updates the worksheets row.

        @param row: int representing the
        row to update.

        @return: None
        """
        if self._worksheet:
            self._write_row_data(self._data[row], row=row)

    def _write_row_data(self, value, row=-1):
        """Writes the given value to the respective
        row.

        @param value: value representing the data
        to be written to the row.

        @keyword row: int representing the row to
        be written to. By default is self.row.

        @return: None
        """
        if row < 0:
            row = self.row
        self._worksheet.write(row, self._initial_col, value)

    def connect(self, worksheet, format_data, row=0, col=0):
        """Connects the worksheet to the data
        area.

        @param worksheet: Worksheet object that
        is to have the data area written to it.

        @return: 2 tuple of (int, int) representing
        the row and column that this data area
        terminates and is safe to add another area.
        """
        self._initial_row = row
        self._initial_col = col
        self._worksheet = worksheet
        self.format_data = format_data

        self._write_data_column()
        return 0, col + 1

    def _write_data_column(self, format=None):
        """Writes the data column.

        @return: None
        """
        self._worksheet.write_column(self._initial_row, self._initial_col,
                                     self._data, cell_format=format)

    def __iter__(self):
        """Gets an iter over the
        data values.

        @return iter over data values.
        """
        return iter(self._data)

    def __len__(self):
        """Gets the length of
        the data values.

        @return: int representing
        the length of the data values.
        """
        return len(self._data)

    def __str__(self):
        """Gets a str representation
        that represents an absolute
        reference to the worksheet and
        data cells associated with this
        area.

        @return: str representing the
        data.
        """
        return self.get_data_cells_reference()

    def get_data_cells_reference(self):
        """Gets an absolute cell reference
        to the cells and worksheet stored
        in this area.

        @return: str representing the data
        stored in the area.
        """
        data_ref = xl_range_abs(self._initial_row, self._initial_col, self.row,
                                self.col)
        return self._worksheet.get_name + '!' + data_ref


class KeyToValueDataArea(DatasheetArea):
    """Represents a KeyToValueDataArea stored
    inside of the datasheet that is used
    to display a column of data.

    This area categorized the data by the
    key value's range it is within.
    """

    def __init__(self, package_value, data_keys):
        """Initializes the KeyToValueDataArea with the
        given data keys.

        @param package_value: PackageValue subclass
        that represents the functions for pulling
        values from given package data.

        @param data_keys: list representing the
        data keys associated with the area. This
        list is expected to be in pre-categorized
        order.
        """
        self._check_package_value(package_value)
        self._package_value = package_value
        self._data_keys = tuple(data_keys)
        data = self._fill_data_list_values()
        super(KeyToValueDataArea, self).__init__(data)

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
        PackageValue

        @return: bool representing if the test was
        passed.
        """
        if not package_value or not isinstance(package_value, PackageValue):
            curr_type = type(package_value)
            raise ValueError('Expected instance of PackageValue to be given for '
                             'KeyToValueDataArea. Received {} instead.'.format(curr_type))

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
            elif value >= mid_value:
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
        return self._package_value.get_data_value(data)

    def _get_data_comparison_value(self, data):
        """Gets the value associated with the
        data comparison.

        @param data: PackagedData to have the
        value obtained from it.

        @return: value representing the data
        comparison.
        """
        return self._package_value.get_data_comparison_value(data)


class ItemsTimeKeyToValueDataArea(KeyToValueDataArea):
    """This class represents an area used
    for storing the items data by time
    keys
    """

    def __init__(self, data_keys):
        """Initializes a new ItemsTimeKeyToValueDataArea
        object.

        @param data_keys: list of datetime.time
        representing the keys associated with
        the data.
        """
        package_value = ItemsTimePackageValue()
        super(ItemsTimeKeyToValueDataArea, self).__init__(package_value, data_keys)


class OrdersTimeKeyToValueDataArea(KeyToValueDataArea):
    """This class represents an area used
    for storing orders data by time keys.
    """

    def __init__(self, data_keys):
        """Initializes a new OrdersTimeKeyToValueDataArea
        object.

        @param data_keys: list of datetime.time
        representing the keys associated with the data.
        """
        package_value = OrdersTimePackageValue()
        super(OrdersTimeKeyToValueDataArea, self).__init__(package_value, data_keys)


class TotalsTimeKeyToValueDataArea(KeyToValueDataArea):
    """This class represents an area
    used for storing totals data by time
    keys.
    """

    def __init__(self, data_keys, data=[]):
        """Initializes a new TotalsTimeKeyToValueDataArea
        object.

        @param data_keys: list of datetime.time
        representing the keys associated with the data.
        """
        package_value = TotalsTimePackageValue()
        super(TotalsTimeKeyToValueDataArea, self).__init__(package_value, data_keys)