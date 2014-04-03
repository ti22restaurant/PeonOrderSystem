"""This module defines the outside facing
adapter that wraps external library functionality
to allow for the audit to be performed.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.AuditWorksheet import AuditWorksheet


class XLWorksheet(AuditWorksheet):
    """Provides the functionality for
    accessing external library functions
    """

    def __init__(self, xlsx_worksheet, formats):
        """Initializes the worksheet

        @param xlsx_worksheet: xlsxwriter.Worksheet
        whose functionality this worksheet is
        wrapping.

        @param formats: XLFormatter that represents
        the cell formats.
        """
        self._worksheet = xlsx_worksheet
        self._formats = formats

        self._row = 0
        self._col = 0

        self._areas = []

    @property
    def formats(self):
        """Gets the formats
        that allow for formatting
        cells.

        @return: XLFormatter object
        """
        return self._formats

    @property
    def row(self):
        """Gets the row that
        the worksheet is currently
        pointing to.

        @return: int representing
        the row.
        """
        return self._row

    @property
    def col(self):
        """Gets the column that
        the worksheet is currently
        point to.

        @return: int representing
        the column.
        """
        return self._col

    @staticmethod
    def _get_chart(chart):
        """Gets the chart data
        from the given XLChart

        @param chart: XLChart that
        stores the chart.

        @return: xlsxwriter.Chart class
        that represents the chart.
        """
        if chart:
            return chart._chart

    @staticmethod
    def _get_format(format):
        """Gets the format data from
        the given format.

        @param format: AuditFormat
        that stores the format data.

        @return: xlsxwriter.Format class
        that represents the data.
        """
        if format:
            return format.format_data

    def add_area(self, area):
        """Adds the given area to the
        worksheet.

        @param area: Area to be added to
        the worksheet.

        @return: None
        """
        self._areas.append(area)
        self._row, self._col = area.connect(self)

    def write(self, row, col, data, format=None):
        """Writes the specified data to the cell
        represented by the row and column.

        @param row: int representing the row that
        the data should be written to.

        @param col: int representing the column
        that the data should be written to.

        @param data: writeable data.

        @param format: XLFormat that represents
        the format to be applied to the cell.

        @return: int value representing if the
        data was successfully added.
        """
        frmt = self._get_format(format)
        return self._worksheet.write(row, col, data, frmt)

    def insert_chart(self, row, col, chart):
        """Inserts the chart are the given
        location.

        @param row: int representing the row

        @param col: int representing the column

        @param chart: XLChart that is to added
        to the given cell.

        @return: None
        """
        chrt = self._get_chart(chart)
        return self._worksheet.insert_chart(row, col, chrt)

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
        frmt = self._get_format(format)
        self._worksheet.set_row(row_number, row_height, cell_format=frmt)

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
        frmt = self._get_format(format)
        self._worksheet.set_column(first_col, last_col, col_width,
                                   cell_format=frmt)

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
        frmt = self._get_format(format)
        self._worksheet.write_column(row, col, data, frmt)

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
        frmt = self._get_format(format)
        self._worksheet.merge_range(first_row, first_col, last_row, last_col,
                                    data=data, cell_format=frmt)

    def get_name(self):
        """Gets the name associated
        with the worksheet.

        @return: None
        """
        return self._worksheet.get_name()




