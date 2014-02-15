"""This module contains classes
used for generating Datasheet
areas.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from xlsxwriter.utility import xl_range_abs

from src.peonordersystem.audit.auditbook.areas.datasheet.abc.DataArea \
    import AbstractDataArea
from .containers.abc.Container import check_container


class DataArea(AbstractDataArea):
    """Abstract Base Class

    Represents an area used for displaying
    data inside of the data sheet.
    """

    def __init__(self, container):
        """Initializes a new DataArea with
        the given container.

        @param container: Container object
        that stores and accesses the data.
        """
        check_container(container)
        self._container = container

        self.format_data = None
        self._worksheet = None
        self._initial_row = None
        self._initial_col = None

    @property
    def data(self):
        """Gets the data associated
        with the DataArea.

        @return: tuple of values
        representing the data stored
        in this DataArea.
        """
        return self._container.data

    def insert(self, data):
        """Inserts the given data
        into the data area.

        @param data: DataBundle representing
        the data to be added to the given area.

        @return: None
        """
        row = self._container.add(data)
        self._update_row(row)

    def _update_row(self, row):
        """Updates the worksheets row.

        @param row: int representing the
        row to update.

        @return: None
        """
        try:
            self._write_row_data(self.data[row], row=row)
        except TypeError:
            pass

    def _write_row_data(self, value, row):
        """Writes the given value to the respective
        row.

        @param value: value representing the data
        to be written to the row.

        @keyword row: int representing the row to
        be written to. By default is self.row.

        @return: None
        """
        self._check_worksheet_write_data()
        self._worksheet.write(row, self._initial_col, value)

    def connect(self, worksheet):
        """Connects the worksheet to the data
        area.

        @param worksheet: Worksheet object that
        is to have the data area written to it.

        @return: 2 tuple of (int, int) representing
        the row and column that this data area
        terminates and is safe to add another area.
        """
        self._check_worksheet(worksheet)
        row = worksheet.row
        col = worksheet.col

        self._initial_row = row
        self._initial_col = col
        self._worksheet = worksheet
        self.format_data = worksheet.formats

        self._write_data_column()
        return row, col + 1

    def _write_data_column(self):
        """Writes the data column.

        @return: None
        """
        self._check_worksheet_write_data()

        format = self._get_data_format()
        self._worksheet.write_column(self._initial_row, self._initial_col,
                                     self.data, format=format)

    def _get_data_format(self):
        """Gets the format for displaying
        the containers data.

        @return: format used to displaying
        the data.
        """
        return self._container.get_data_format(self.format_data)

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

    def get_data_cells_reference(self):
        """Gets an absolute cell reference
        to the cells and worksheet stored
        in this area.

        @return: str representing the data
        stored in the area.
        """
        self._check_worksheet_data_cells_reference()
        data_ref = xl_range_abs(self._initial_row, self._initial_col,
                                len(self.data), self._initial_col)

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

