"""

"""

import xlsxwriter
from copy import copy, deepcopy
from abc import ABCMeta, abstractmethod


class SpreadsheetArea(object):
    """

    """
    #================================================================================
    # Constants used for generating the columns area.
    #================================================================================
    AREA_COL_NUM = 3
    AREA_COL_WIDTH = 20

    #================================================================================
    # Constants used for generating the title area.
    #================================================================================
    NUM_OF_MAIN_TITLE_ROWS = 1
    NUM_OF_SUBTITLE_ROWS = 1

    # Subtract one because of zero based indexing.
    TITLE_AREA_START = 0
    TITLE_AREA_END = TITLE_AREA_START + NUM_OF_MAIN_TITLE_ROWS + \
                     NUM_OF_SUBTITLE_ROWS - 1

    TITLE_AREA_ROW_HEIGHT = 30

    #================================================================================
    # Constants used for generating the total area.
    #================================================================================
    NUM_OF_MAIN_TOTAL_ROWS = 1
    NUM_OF_SUBTOTAL_ROWS = 2

    # Alter by one because of zero based indexing
    TOTAL_AREA_START = TITLE_AREA_END + 1
    TOTAL_AREA_END = TOTAL_AREA_START + NUM_OF_MAIN_TOTAL_ROWS + \
                     NUM_OF_SUBTOTAL_ROWS - 1

    TOTAL_AREA_ROW_HEIGHT = 20

    #================================================================================
    # Constants used for generating the data area.
    #================================================================================
    # Alter by one because of zero based indexing
    DATA_AREA_START = TOTAL_AREA_END + 1

    __metaclass__ = ABCMeta

    def __init__(self, format_dict):
        """Initializes a new SpreadsheetArea class
        """
        self.format_dict = format_dict
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

    @property
    def worksheet(self):
        """Gets the worksheet associated
        with the area.

        @return: xlsxwriter.worksheet.Worksheet
        object representing the worksheet associated
        with this area.
        """
        return self._worksheet

    def connect(self, worksheet):
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
        self._check_worksheet(worksheet)
        self.row = worksheet.row
        self.col = worksheet.col

        self._initial_row = self.row
        self._initial_col = self.col

        self._worksheet = worksheet
        self.format_area()

        return self.row, self.col + self.AREA_COL_NUM

    def _check_worksheet(self, worksheet):
        """Checks that the worksheet is
        an instance of xlsxwriter.Worksheet
        class.

        @raise ValueError: If the given
        worksheet is not a subclass member or
        instance or xlsxwriter.Worksheet

        @return: bool value representing if
        the test was passed.
        """
        if not worksheet or not isinstance(worksheet, xlsxwriter.worksheet.Worksheet):
            curr_type = type(worksheet)
            exp_type = xlsxwriter.worksheet.Worksheet
            raise ValueError('Expected connected worksheet to be an instance or'
                             'subclass of {} ---> got {} instead'.format(curr_type,
                                                                         exp_type))
        return True

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
        format = self.format_dict['left_column']
        self.worksheet.set_column(self.col, self.col, self.AREA_COL_WIDTH, format)

    def _format_area_columns_ends_right(self):
        """Formats the right most end column for
        the area.

        @return: None
        """
        format = self.format_dict['right_column']
        self.worksheet.set_column(self.area_end_col, self.area_end_col,
                                   self.AREA_COL_WIDTH, format)

    def _format_area_columns_center(self):
        """Formats the center most columns for the
        area.

        @return: None
        """
        self.worksheet.set_column(self.col + 1, self.area_end_col - 1,
                                   self.AREA_COL_WIDTH)

    def _format_title_area(self):
        """formats the title area which
        represents the first part of the
        area that displays title data.

        @return: two-tuple of (int, int)
        representing the row and column
        that the title area terminates at.
        """
        self._format_title_area_cells()
        return self.TITLE_AREA_END + self.initial_row + 1, self.initial_col

    def _format_title_area_cells(self):
        """Formats the cells for the title
        area.

        @return: None
        """
        formats = self._get_row_title_formats()

        area_start = self.TITLE_AREA_START + self.initial_row
        area_end = self.TITLE_AREA_END + self.initial_row

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
        return self.TOTAL_AREA_END + self.initial_row + 1, self.initial_col

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

        area_start = self.TOTAL_AREA_START + self.initial_row
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

        area_start = self.TOTAL_AREA_START + self.initial_row
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
            self.worksheet.write_blank(row, j + self.initial_col, '', format)

    def _format_cells_row_height(self, row, row_height):
        """Formats the cell row height.

        @param row: int representing the cell row to
        have its height formatted.

        @param row_height: int representing the height
        for the cell row to be formatted to.

        @return: None
        """
        self.worksheet.set_row(row, row_height)

    def _get_row_title_formats(self):
        """Gets the row title formats. This
        gives a list representing the formats
        for the left, center, and right most cells
        of a title area.

        @return: list of n xlsxwriter.Format objects
        where n is the number of columns in this area.
        """
        cols = self.AREA_COL_NUM - 2
        formats = [self.format_dict['title_format_left']] + \
                  [self.format_dict['title_format_center'] for x in range(cols)] + \
                  [self.format_dict['title_format_right']]
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
        formats = [self.format_dict['subtitle_format_left']] + \
                  [self.format_dict['subtitle_format_center'] for x in range(cols)] + \
                  [self.format_dict['subtitle_format_right']]
        return formats

    @abstractmethod
    def add(self, *args):
        """Abstract Method.

        Adds the given data to the
        area.

        @return: None
        """
        pass



class GeneralDatesheetOrderArea(SpreadsheetArea):
    """

    """

    def __init__(self, packaged_data, format_dict):
        """

        @param packaged_data:
        @param format_dict:
        @return:
        """
        self.packaged_data = packaged_data
        super(GeneralDatesheetOrderArea, self).__init__(format_dict)

    def create_title_area(self):
        """

        @return:
        """
        super(GeneralDatesheetOrderArea, self).create_title_area()

    def create_total_area(self):
        """

        @return:
        """
        super(GeneralDatesheetOrderArea, self).create_total_area()

    def add(self):
        """

        @return:
        """
        pass