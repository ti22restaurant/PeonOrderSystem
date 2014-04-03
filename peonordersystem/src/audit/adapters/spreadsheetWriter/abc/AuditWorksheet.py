"""This module defines the abstract base
class for an object to be useable as an
AuditWorksheet.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class AuditWorksheet(object):
    """Describes the base methods
    and properties to provide the
    functionality of an AuditWorksheet.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def formats(self):
        """Gets the formats that
        are useable by this
        AuditWorksheet.

        @return: XLFormat object
        """
        pass

    @abstractproperty
    def row(self):
        """Gets the row that the
        AuditWorksheet is currently
        operating on

        @return: int representing
        the row.
        """
        pass

    @abstractproperty
    def col(self):
        """Gets the col that the
        AuditWorksheet is currently
        operating on.

        @return: int representing
        the column
        """
        pass

    @abstractmethod
    def add_area(self, area):
        """Adds the given area
        to the worksheet.

        @param area: Area that
        is to be added to the
        worksheet.

        @return: None
        """
        pass

    @abstractmethod
    def write(self, row, col, data, format=None):
        """Writes the specified data at the specified
        row and column with the given format.

        @param row: int representing the row that the
        data should be written at

        @param col: int representing the column that
        the data should be written at.

        @param data: writeable data type.

        @param format: XLFormat that represents the
        format to be applied to the cell.

        @return: int value representing if the
        data was successfully added.
        """
        pass

    @abstractmethod
    def insert_chart(self, row, col, chart):
        """Inserts the chart are the given
        location.

        @param row: int representing the row

        @param col: int representing the column

        @param chart: XLChart that is to added
        to the given cell.

        @return: None
        """
        pass

    @abstractmethod
    def set_row(self, row_number, row_height, format=None):
        """Sets the given row to the given height and
        applies the given keywords

        @param row_number: int representing the row
        number to be set.

        @param row_height: int representing the height
        of the row to be set.

        @keyword format: XLFormat to be applied to
        the row. Default is None

        @return: None
        """
        pass

    @abstractmethod
    def set_column(self, first_col, last_col, col_width, format=None):
        """Sets the given column to the given width and applies
        the given keywords.

        @param first_col: int representing the first column
        to be set. Inclusive.

        @param last_col: int representing the last column
        to be set. Inclusive.

        @param col_width: int representing the width of the column
        to be set.

        @param format: XLFormat representing the format to be
        set.

        @return: None
        """
        pass

    @abstractmethod
    def write_column(self, row, col, data, format=None):
        """Write the given data set in a column starting at
        the specific row column specified.

        @param row: int representing the first row
        that the data column should be written to.

        @param col: int representing the column that
        the data should be written to.

        @param data: iterable data collection

        @keyword format: XLFormat representing the
        format to apply to each cell.

        @return: None
        """
        pass


    @abstractmethod
    def merge_range(self, first_row, first_col, last_row, last_col, data=None,
                    format=None):
        """Merges the range of cells between the given first row and column
        to the given last row and column. Applies the given keywords to the
        merged range.

        @param first_row: int representing the starting row

        @param first_col: int representing the starting column

        @param last_row: int representing the last row

        @param last_col: int representing the last column

        @keyword data: Data to apply to the merged range. Default is None

        @param format: XLFormat to apply to merged range. Default is None.

        @return: None
        """
        pass

    @abstractmethod
    def get_name(self):
        """Gets the name associated
        with the worksheet.

        @return: None
        """
        pass