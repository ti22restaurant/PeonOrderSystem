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
from src.peonordersystem.audit.Area import Area


class DataArea(Area):
    """Abstract Base Class

    Represents an area used for displaying
    data inside of the data sheet.
    """

    __metaclass__ = ABCMeta

    def __init__(self, data):
        """Initializes the DataArea with the
        given data keys.

        @keyword data: list representing the data
        associated with the area. The data is expected
        to already have been parsed such that it holds
        a one to one correspondence with the keys.
        """
        self.format_data = None
        self._data = data
        self.row = len(self._data)
        self.col = None

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
        try:
            self._write_row_data(self._data[row], row=row)
        except TypeError:
            pass

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
        self._check_worksheet_write_data()
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
        self._check_worksheet(worksheet)
        self._initial_row = row
        self._initial_col = col
        self._worksheet = worksheet
        self.format_data = format_data

        self.col = col

        self._write_data_column()
        return row, col + 1

    def _write_data_column(self, format=None):
        """Writes the data column.

        @return: None
        """
        self._check_worksheet_write_data()
        self._worksheet.write_column(self._initial_row, self._initial_col,
                                     self._data, cell_format=format)

    def _check_worksheet_write_data(self):
        """Checks if the worksheet may have the data
        written to it.

        @raise TypeError: if the stored worksheet is not
        an instance or subclass of Worksheet.

        @return: bool value representing if the test was
        passed.
        """
        error_msg = 'Worksheet must be connected before this area can be written!'
        self._check_worksheet(self._worksheet, message=error_msg)

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

    def get_data_cells_reference(self):
        """Gets an absolute cell reference
        to the cells and worksheet stored
        in this area.

        @return: str representing the data
        stored in the area.
        """
        self._check_worksheet_data_cells_reference()
        data_ref = xl_range_abs(self._initial_row, self._initial_col, self.row,
                                self.col)
        return '=' + self._worksheet.get_name() + '!' + data_ref

    def _check_worksheet_data_cells_reference(self):
        """Checks if the worksheet data cells reference may
        be obtained.

        @raise TypeError: if the current worksheet is not
        an instance or subclass of Worksheet

        @return: bool value representing if the test was passed.
        """
        error_msg = 'Worksheet must be connected to this area before an absolute ' \
                    'reference the cells may be created!'
        return self._check_worksheet(self._worksheet, message=error_msg)

