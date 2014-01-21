"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from copy import copy
from abc import ABCMeta, abstractmethod
from xlsxwriter.utility import xl_range_abs


class DatasheetArea(object):
    """

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

    def connect(self, worksheet, row=0, col=0):
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
