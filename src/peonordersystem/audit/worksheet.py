"""Defines worksheet classes that are
used to wrap worksheet data and allow
worksheet data to be written to by
SpreadsheetAreas.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from peonordersystem.audit.areas.KeyAreas import TimeKeysArea


class Worksheet(object):
    """Worksheet object is used to contain
    relevant worksheet data and provides the
    functionality of adding areas to the worksheet.

    @var row: int representing the current row
    that is considered valid for the worksheet.

    @var col: int representing the current column
    that is considered valid for the worksheet.

    @var areas: list of SpreadsheetArea objects
    that represent the areas associated with this
    worksheet.
    """

    def __init__(self, xlsx_worksheet, format_data):
        """Initialzies the Worksheet with
        the given xlsxwriter.worksheet.

        @param xlsx_worksheet: xlsxwriter.worksheet.Worksheet
        that this class will use as its baseline worksheet to
        perform the functionality on.
        """
        self.areas = []

        self._worksheet = xlsx_worksheet
        self.format_data = format_data

        self.row = 0
        self.col = 0

    def add_area(self, area):
        """Adds the given Area to
        the worksheet.

        @param spreadsheet_area: SpreadsheetArea
        subclass that represents the area to be
        added.

        @return: None
        """
        self.areas.append(area)
        self.row, self.col = area.connect(self, self.format_data, row=self.row,
                                          col=self.col)

    def write(self, row, column, data, format):
        """Writes the given data to the specified area.

        @param row: int representing the row that
        the data should be written to.

        @param column: int representing the column
        that the data should be written to.

        @param data: data to be written.

        @param format: xlsxwriter.Format object
        that represents the format for the cell
        to display.

        @return: int value representing if the data
        was successfully added.
        """
        return self._worksheet.write(row, column, data, format)

    def insert_chart(self, row, column, chart):
        """Inserts at the given row and column the
        given chart into the worksheet.

        @param row: int representing the row that
        the chart will be inserted at.

        @param column: int representing the column
        that the chart will be inserted at.

        @param chart: xlsxwriter.Chart object
        that is to be inserted.

        @return: None
        """
        self._worksheet.insert_chart(self.row, self.col, chart)

    def set_row(self, row_number, row_height, **kwargs):
        """Sets the given row to the given height with the
        specified keyword arguments.

        @param row_number: int representing the row
        number to set.

        @param row_height: int representing the height
        of the row to be set.

        @param kwargs: wildcard catchall used to catch
        any keyword arguments. Potential keywords may be
        data or format.

        @return: None
        """
        self._worksheet.set_row(row_number, row_height, **kwargs)

    def set_column(self, first_column, last_column, col_width, **kwargs):
        """Sets the given column range to the given column width and
        associated with it any potential keywords.

        @param first_column: int representing the first
        column of the range to be set.

        @param last_column: int representing the last column
        of the range to be set.

        @param col_width: int representing the width of each
        column in the range.

        @param kwargs: wildcard catchall used to pass keyword
        arguments. Potential format keyword.

        @return: None
        """
        self._worksheet.set_column(first_column, last_column, col_width, **kwargs)

    def write_column(self, row, column, data, **kwargs):
        """Write the given data set in a column starting at
        the specific row column specified.

        @param row: int representing the first row
        that the data column should be written to.

        @param column: int representing the column that
        the data should be written to.

        @param data: iterable collcetion of data to be
        written.

        @param kwargs: potential keyword arguments.

        @return: None
        """
        self._worksheet.write_column(row, column, data, **kwargs)

    def merge_range(self, first_row, first_column, last_row, last_column, **kwargs):
        """Merges the given range.

        @param first_row: int representing the first row of the
        range to be merged

        @param first_column: int representing the first column
        of the range to be merged.

        @param last_row: int representing the last row of the
        column to be merged.

        @param last_column: int representing the last column
        of the range to be merged.

        @param kwargs: potential keywords to be associated with
        the merged range. Format applies the format to the cells
        and data adds the given data to the merged cells.

        @return: None
        """
        self._worksheet.merge_range(first_row, first_column, last_row,
                                    last_column, **kwargs)

    def __str__(self):
        """Gets a string representation
        of the worksheet.

        @return: str representing the
        worksheet. By default this value
        is the worksheets name.
        """
        return self.get_name()

    def get_name(self):
        """Gets the name associated with
        the worksheet.

        @return: str representing the
        worksheets name.
        """
        return self._worksheet.get_name()


class DataWorksheet(Worksheet):
    """DataWorksheet class creates a hidden
    worksheet that is used to store and access
    data that represents intermediate steps for
    display data in specific forms.
    """
    HIDDEN_WORKSHEET_NAME = 'HiddenDataWorksheet'

    def __init__(self, worksheet, format_data):
        """ Initializes the DataWorksheet object.

        @param worksheet: xlsxwriter.Worksheet subclass
        that will provide this area with its base
        functionality.

        @param format_data: dict of xlsxwriter.Format
        objects that represent the formats for display
        data.
        """
        super(DataWorksheet, self).__init__(worksheet, format_data)
        self.format_data = format_data

        self.time_keys = self._create_time_keys()
        #self._date_keys_area = self._create_date_keys()

        self.items_data = {}
        self.orders_data = {}

        self._worksheet.name = self.HIDDEN_WORKSHEET_NAME
        #self._worksheet.hide()

    def _create_time_keys(self):
        """

        @return:
        """
        time_keys_area = TimeKeysArea()
        self.add_area(time_keys_area)
        return time_keys_area


def check_worksheet(worksheet):
    """Checks that the worksheet is
    an instance or subclass member
    of the Worksheet class

    @raise ValueError: If the given
    worksheet is not a subclass member or
    instance or Worksheet

    @return: bool value representing if
    the test was passed.
    """
    exp_type = Worksheet
    if not worksheet or not isinstance(worksheet, exp_type):
        curr_type = type(worksheet)
        raise ValueError('Expected connected worksheet to be an instance or '
                         'subclass of {} got {} instead'.format(exp_type,
                                                                curr_type))
    return True
