"""Defines the abstract base class for all SpreadsheetAreas.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""

from abc import ABCMeta, abstractmethod
from peonordersystem.audit.Area import Area

from src.peonordersystem.audit.worksheet import check_worksheet


class SpreadsheetArea(Area):
    """Abstract Base Class.

    SpreadsheetArea class represents the abstract
    base class that implements the base functionality
    for any area. The base area provides the following
    functionality:

        1.  Formats the cells for the standard for the area.
            including:

            i.      Title area
            ii.     Subtitle area
            iii.    Totals area
            iv.     Subtotals area
            v.      Data area

        2.  Provides functions for adding data to the title
            and subtitle areas. Total and subtotal areas.

        3.  Requires an add class that adds data to the
            Data area.

    @warning: This area class is relatively uncoupled from the worksheet prior
    to using the connect method. Most functionality is inaccessible until a
    worksheet has been coupled with the class. Upon coupling the worksheet
    should be considered a permanent property of this area and not altered
    in any way.

    @var format_data: dict that maps str to xlsxwriter.Formats. This
    is used to access and utilize all format data.

    @var worksheet: xlsxwriter.worksheet.Worksheet object that
    represents the worksheet that this area is connected to. Once
    coupled the worksheet shouldn't be changed.

    @var row: int representing the current row that data can be
    written to.

    @var col: int representing the current col that data can be
    written to.

    @var initial_row: int representing the initial starting row
    for this area on the worksheet.

    @var initial_col: int representing the initial starting col
    for this area on the worksheet.

    @var area_end_col: int representing the final column that data
    can be added to without exceeding the column boundaries for the
    area.
    """
    #================================================================================
    # Constants used for generating the columns area.
    #================================================================================
    AREA_COL_NUM = 3
    AREA_COL_WIDTH = 22

    #================================================================================
    # Constants used for generating the title area.
    #================================================================================
    NUM_OF_MAIN_TITLE_ROWS = 2
    NUM_OF_SUBTITLE_ROWS = 1
    TITLE_AREA_ROW_HEIGHT = 40

    #///////////////////////////////////////////////////////////////////////////////
    # These constants shouldn't be edited. They are relative to other defined
    # constants and any changes in the editable constants will be reflected here
    #////////////////////////////////////////////////////////////////////////////////
    # Subtract one because of zero based indexing.
    _TITLE_AREA_START = 0
    _TITLE_AREA_END = _TITLE_AREA_START + NUM_OF_MAIN_TITLE_ROWS + \
                      NUM_OF_SUBTITLE_ROWS - 1

    #////////////////////////////////////////////////////////////////////////////////

    #================================================================================
    # Constants used for generating the total area.
    #================================================================================
    NUM_OF_MAIN_TOTAL_ROWS = 1
    NUM_OF_SUBTOTAL_ROWS = 2
    TOTAL_AREA_ROW_HEIGHT = 25

    #////////////////////////////////////////////////////////////////////////////////
    # These constants shouldn't be edited. They are relative to other defined
    # constants and any changes in the editable constants will be reflected here
    #////////////////////////////////////////////////////////////////////////////////
    # Alter by one because of zero based indexing
    _TOTAL_AREA_START = _TITLE_AREA_END + 1
    _TOTAL_AREA_END = _TOTAL_AREA_START + NUM_OF_MAIN_TOTAL_ROWS + \
                     NUM_OF_SUBTOTAL_ROWS - 1

    #////////////////////////////////////////////////////////////////////////////////

    #================================================================================
    # Constants used for generating the data area.
    #================================================================================
    DATA_ROW_HEIGHT = 25

    #////////////////////////////////////////////////////////////////////////////////
    # These constants shouldn't be edited. They are relative to other defined
    # constants and any changes in the editable constants will be reflected here
    #////////////////////////////////////////////////////////////////////////////////
    # Alter by one because of zero based indexing
    _DATA_AREA_START = _TOTAL_AREA_END + 1

    #////////////////////////////////////////////////////////////////////////////////

    __metaclass__ = ABCMeta

    def __init__(self):
        """Initializes a new SpreadsheetArea class
        """
        self.format_data = None
        self._worksheet = None
        self.row = None
        self.col = None
        self._initial_col = None
        self._initial_row = None

    @property
    def area_end_col(self):
        """Gets the area end column

        @return: int representing the column
        that represents the end of this area.
        """
        return self.initial_col + self.AREA_COL_NUM - 1

    @property
    def data_area_start(self):
        """Gets the int representing
        the row that the data area starts
        on.

        @return: int representing the
        data area start row.
        """
        return self._DATA_AREA_START

    @property
    def initial_row(self):
        """Gets the initial row that
        represents the first row in the area.

        @return: int representing the
        initial row.
        """
        return self._initial_row

    @property
    def initial_col(self):
        """Gets the initial column that
        represents the first column in the
        area.

        @return: int representing the
        initial column
        """
        return self._initial_col

    def connect(self, worksheet, format_data, row=0, col=0):
        """Connects the worksheet to the
        SpreadsheetArea. The worksheet will
        be connected and coupled with the area.

        @param worksheet: xlsxwriter.Worksheet
        object that represents the worksheet
        that the area should be added to.

        @return: tuple of (int, int) representing
        the row and column that it is safe to add
        additional data to. This row, col pair
        represents the top right hand boundary of
        the area.
        """
        check_worksheet(worksheet)
        self.row = row
        self.col = col
        self.format_data = format_data

        self._initial_row = self.row
        self._initial_col = self.col

        self._worksheet = worksheet
        self.format_area()

        self.row = self.data_area_start + self.initial_row
        return self.initial_row, self.initial_col + self.AREA_COL_NUM

    def format_area(self):
        """Formats the rows and
        columns for the area

        @return: None
        """
        self._format_area_columns()
        self._format_title_area()
        self._format_total_area()

    def _format_area_columns(self):
        """Formats the columns for the
        area.

        @return: None
        """
        self._format_area_columns_ends()
        self._format_area_columns_center()

    def _format_area_columns_ends(self):
        """Formats the left and right end
        columns for the area.

        @return: None
        """
        self._format_area_columns_ends_left()
        self._format_area_columns_ends_right()

    def _format_area_columns_ends_left(self):
        """Formats the left most end column for
        the area.

        @return: None
        """
        format = self.format_data['left_column']
        self._set_worksheet_column(first_col=self.col, last_col=self.col,
                                   width=self.AREA_COL_WIDTH, format=format)

    def _format_area_columns_ends_right(self):
        """Formats the right most end column for
        the area.

        @return: None
        """
        format = self.format_data['right_column']
        self._set_worksheet_column(first_col=self.area_end_col,
                                   last_col=self.area_end_col,
                                   width=self.AREA_COL_WIDTH, format=format)

    def _format_area_columns_center(self):
        """Formats the center most columns for the
        area.

        @return: None
        """
        self._set_worksheet_column(first_col=self.col + 1,
                                   last_col=self.area_end_col - 1,
                                   width=self.AREA_COL_WIDTH)

    def _format_title_area(self):
        """formats the title area which
        represents the first part of the
        area that displays title data.

        @return: two-tuple of (int, int)
        representing the row and column
        that the title area terminates at.
        """
        self._format_title_area_cells()
        return self._TITLE_AREA_END + self.initial_row + 1, self.initial_col

    def _format_title_area_cells(self):
        """Formats the cells for the title
        area.

        @return: None
        """
        formats = self._get_row_title_formats()

        area_start = self._TITLE_AREA_START + self.initial_row
        area_end = self._TITLE_AREA_END + self.initial_row

        for row in range(area_start, area_end + 1):
            self._format_cells_row(row, formats)
            self._format_cells_row_height(row, self.TITLE_AREA_ROW_HEIGHT)

    def _format_total_area(self):
        """Formats the total area which
        is used to display totals data
        about the area.

        @return: two tuple of (int, int)
        representing the row and column
        that the total area terminates at.
        """
        self._format_total_area_cells()
        return self._TOTAL_AREA_END + self.initial_row + 1, self.initial_col

    def _format_total_area_cells(self):
        """Formats the total area cells

        @return: None
        """
        self._format_total_area_cells_main()
        self._format_total_area_cells_subtotal()

    def _format_total_area_cells_main(self):
        """Formats the main cells for the total
        area.

        @return: None
        """
        formats = self._get_row_title_formats()

        area_start = self._TOTAL_AREA_START + self.initial_row
        area_end = area_start + self.NUM_OF_MAIN_TOTAL_ROWS

        for row in range(area_start, area_end + 1):
            self._format_cells_row(row, formats)
            self._format_cells_row_height(row, self.TOTAL_AREA_ROW_HEIGHT)

    def _format_total_area_cells_subtotal(self):
        """Formats the subtotal cells for the total
        area.

        @return: None
        """
        formats = self._get_row_subtitle_formats()

        area_start = self._TOTAL_AREA_START + self.initial_row
        area_end = area_start + self.NUM_OF_SUBTOTAL_ROWS

        for row in range(area_start, area_end + 1):
            self._format_cells_row(row, formats)
            self._format_cells_row_height(row, self.TOTAL_AREA_ROW_HEIGHT)

    def _format_cells_row(self, row, formats):
        """Formats each cell in the given row
        with the given formats.

        @raise ValueError: If the given list
        of formats is less than the number of
        column cells that are in this area.

        @param row: int representing the row
        that is to be formatted.

        @param formats: list of xlsxworksheet.Format
        objects that represent the formats that are
        to be applied. This list is expected

        @return: None
        """
        if len(formats) < self.AREA_COL_NUM:
            curr_value = len(formats)
            exp_value = self.AREA_COL_NUM
            raise ValueError('Number of given formats to format cells in row must '
                             'be atleast as long as area column numbers. Expected '
                             '{} values: formats length --> {}'.format(curr_value,
                                                                       exp_value))

        for j in range(self.AREA_COL_NUM):
            format = formats[j]
            self.write_data('', row=row, col=j + self.initial_col, format=format)

    def _format_cells_row_height(self, row, row_height):
        """Formats the cell row height.

        @param row: int representing the cell row to
        have its height formatted.

        @param row_height: int representing the height
        for the cell row to be formatted to.

        @return: None
        """
        self._set_worksheet_row(row=row, height=row_height)

    def _get_row_title_formats(self):
        """Gets the row title formats. This
        gives a list representing the formats
        for the left, center, and right most cells
        of a title area.

        @return: list of n xlsxwriter.Format objects
        where n is the number of columns in this area.
        """
        cols = self.AREA_COL_NUM - 2
        formats = [self.format_data['title_format_left']] + \
                  [self.format_data['title_format_center'] for x in range(cols)] + \
                  [self.format_data['title_format_right']]
        return formats

    def _get_row_subtitle_formats(self):
        """Gets the row subtitle formats. This
        gives a list representing the formats
        for the left, center, and right most cells
        of a subtitle area.

        @return: list of n xlsxwriter.Format objects
        where n is the number of columns in this area.
        """
        cols = self.AREA_COL_NUM - 2
        formats = [self.format_data['subtitle_format_left']] + \
                  [self.format_data['subtitle_format_center'] for x in range(cols)] + \
                  [self.format_data['subtitle_format_right']]
        return formats

    @abstractmethod
    def add(self, *args):
        """Abstract Method.

        Adds the given data to the
        area.

        @return: None
        """
        pass

    def update_title_data(self, title_data, date_data):
        """Updates the displayed title data with the
        given title and date data.

        @param title_data: str representing the title
        that should be displayed in this area.

        @param date_data: datetime.datetime object
        that represents the date that should be
        displayed in this area.

        @return: None
        """
        self._update_title_data_date(date_data)
        self._update_title_data_main(title_data)

    def _update_title_data_main(self, title_data):
        """Updates the title areas main title data.

        @return: None
        """
        title_start = self._TITLE_AREA_START + self.initial_row
        title_end = self._TITLE_AREA_START + self.NUM_OF_MAIN_TITLE_ROWS - 1 +\
                    self.initial_row

        title_format = self._get_format_main_title()

        self._merge_worksheet_range(title_start, title_end,
                                    first_col=self.initial_col,
                                    last_col=self.area_end_col,
                                    data=title_data, format=title_format)

    def _get_format_main_title(self):
        """Gets the format for the main title.

        @return: xlsxwriter.Format object that
        represents the main title format.
        """
        return self.format_data['main_title_data_format']

    def _update_title_data_date(self, date_data):
        """Updates the title data date area with the
        given date data.

        @return: None
        """
        date_row = self._TITLE_AREA_START + self.NUM_OF_MAIN_TITLE_ROWS + \
                   self.initial_row

        title_format = self._get_format_date_title()
        datetime_format = self._get_format_date_data()

        self.write_data('Date: ', row=date_row, col=self.initial_col,
                        format=title_format)
        self.write_data(date_data, row=date_row, col=self.initial_col + 1,
                        format=datetime_format)

    def _get_format_date_data(self):
        """Gets the format for the date data

        @return: xlsxwriter.Format object that
        represents the format for the displayed
        date data.
        """
        return self.format_data['datetime_format']

    def _get_format_date_title(self):
        """Gets the format for the date title

        @return xlsxwriter.Format object that
        represents the format for the displayed
        date title.
        """
        return self.format_data['title_format_left']

    def update_total_data(self, totals_data, subtotals_data):
        """Updates the displayed total data with the given
        total and subtotal data respectively.

        @raise ValueError: If the given totals data and subtotals data
        do match the expected length of the totals and subtotals area
        within this area.

        @param totals_data: list of (string, float) tuples where
        each index represents the name and number associated with
        the totals data to be displayed.

        @param subtotals_data: list of (string, float) tuples where
        each index represents the name and number associated with
        the subtotals data to be displayed.

        @return: None
        """
        self._check_totals_data(totals_data, self.NUM_OF_MAIN_TOTAL_ROWS)
        self._check_totals_data(subtotals_data, self.NUM_OF_SUBTOTAL_ROWS)

        self._update_totals_data_total(totals_data)
        self._update_totals_data_subtotal(subtotals_data)

    def _check_totals_data(self, totals_data, expected_length):
        """Checks that the given totals datas length is equal to
        the given expected length.

        @raise ValueError: If the length of the given totals data
        doesn't match the given expected length.

        @return: bool value representing if the test was passed.
        """
        if not totals_data or not len(totals_data) <= expected_length:
            exp_value = expected_length
            curr_value = len(totals_data)
            raise ValueError('Expected given totals data to contain an equal number '
                             'of entries to the expected number of total rows. '
                             'Expected: {}, Received: {}'.format(exp_value,
                                                                 curr_value))
        return True

    def _update_totals_data_total(self, totals_data):
        """Updates the total area with the given
        totals data.

        @param totals_data: list of tuple (str, float)
        representing the name and total data associated
        with the name and data that should be added to
        the totals area.

        @return: None
        """
        row = self._TOTAL_AREA_START + self.initial_row

        for total_name, total_data in totals_data:

            title_format = self._get_format_total_title()
            self.write_data(total_name, row=row, col=self.initial_col,
                            format=title_format)

            total_format = self._get_format_total_data()
            self.write_data(total_data, row=row, col=self.area_end_col,
                            format=total_format)

            row += 1

    def _get_format_total_title(self):
        """Gets the format for the total title.

        @return: xlsxwriter.Format that represents
        the format for the total title.
        """
        return self.format_data['title_format_left']

    def _get_format_total_data(self):
        """Gets the format for the total data.

        @return: xlsxwriter.Format that represents
        the format for the total data.
        """
        return self.format_data['total_data_format']

    def _update_totals_data_subtotal(self, subtotals_data):
        """Updates the subtotal data of the totals area.

        @param subtotals_data: list of tuple (str, float)
        representing the subtotal name and subtotal value
        that is associated with the subtotals to be displayed.

        @return: None
        """
        row = self._TOTAL_AREA_START + self.NUM_OF_MAIN_TOTAL_ROWS + self.initial_row

        for subtotal_name, subtotal_data in subtotals_data:

            subtitle_format = self._get_format_subtotal_title()
            self.write_data(subtotal_name, row=row, col=self.initial_col,
                            format=subtitle_format)

            subtotal_format = self._get_format_subtotal_data()
            self.write_data(subtotal_data, row=row, col=self.area_end_col,
                            format=subtotal_format)

            row += 1

    def _get_format_subtotal_title(self):
        """Gets the format to display the subtotal title.

        @return: xlsxwriter.Format that represents
        the subtotal title format.
        """
        return self.format_data['subtitle_format_left']

    def _get_format_subtotal_data(self):
        """Gets the format for displaying the subtotal data.

        @return: xlsxwriter.Format object that is used
        to display the format of the subtotal data.
        """
        return self.format_data['subtotal_data_format']

    #================================================================================
    # This block represents functions that rely on the functionality of worksheet
    # method to operate properly. Any chances in the worksheet functionality may
    # require changes here.
    #================================================================================
    def write_data(self, data, row=-1, col=-1, format=None):
        """Writes the given data to the row, col with the given format.

        @param data: value to be added to the spreadsheet on the
        row, col with the format.

        @keyword row: int representing the row for the data
        to be added at. By default is self.row

        @keyword col: int representing the column for the
        data to be added to. By default is self.col

        @keyword format: xlsxwriter.Format that represents
        the format the data will be written with.

        @return: 2 tuple of (int, int) representing the
        row and column boundary that it is safe to add
        new data to, on the same column.
        """
        if row < 0:
            row = self.row
        if col < 0:
            col = self.col
        self._set_worksheet_row(row)
        self._worksheet.write(row, col, data, format)

        return row + 1, col

    def _merge_worksheet_range(self, start_row, end_row, first_col=None,
                                   last_col=None, data=None, format=None):
        """Merges the given range of the worksheet between
        the two rows and applies other added data.

        @param start_row: int representing the starting
        row to merge.

        @param end_row: int representing the ending row
        to merge.

        @keyword first_col: int representing the first column
        to be in the merged range. By default is the initial
        column of the area.

        @keyword last_col: int representing the last column
        to be in the merged range. By default is the area
        end col of the area.

        @keyword data: data to be added to the merged range.
        By default is empty string.

        @keyword format: xlsxwriter.Format that the merged
        range should be formatted under. Default is None.

        @return: 2 tuple of (int, int) representing the
        row and column that is the boundary of the merged
        range where it is safe to add new data to.
        """
        if not first_col:
            first_col = self.initial_col
        if not last_col:
            last_col = self.area_end_col
        if not data:
            data = ''

        self._worksheet.merge_range(start_row, first_col, end_row, last_col,
                                    data=data, cell_format=format)
        return end_row, first_col

    def _set_worksheet_row(self, row=-1, height=None, format=None):
        """Sets the height and format of a worksheet row.

        @keyword row: int representing the row that should be set.
        By default is self.row.

        @param height: int representing the height of the row that
        is to be set. By default is self.DATA_ROW_HEIGHT

        @param format: xlsxwriter.Format that is to be applied
        to the row. By default is None.

        @return: None
        """
        if row < 0:
            row = self.row
        if not height:
            height = self.DATA_ROW_HEIGHT
        self._worksheet.set_row(row, height, cell_format=format)

    def _set_worksheet_column(self, first_col=-1, last_col=-1, width=None,
                              format=None):
        """Sets the worksheet column range to a width and format.

        @keyword first_col: int representing the first column in the
        range. By default this is self.initial_col

        @keyword last_col: int representing the last column in
        the range. By default this is self.area_end_col

        @keyword width: int representing the width of columns. Default
        is self.AREA_COL_WIDTH

        @keyword format: xlsxwriter.Format object that represents the
        formats to be applied to the worksheet column range.

        @return None
        """
        if first_col < 0:
            first_col = self.initial_col
        if last_col < 0:
            last_col = self.area_end_col
        if not width:
            width = self.AREA_COL_WIDTH

        self._worksheet.set_column(first_col, last_col, width, cell_format=format)




