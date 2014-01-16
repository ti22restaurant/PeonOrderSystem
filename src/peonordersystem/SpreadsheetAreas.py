"""

"""

import xlsxwriter
from abc import ABCMeta, abstractmethod

from src.peonordersystem.MenuItem import is_menu_item, MenuItem
from src.peonordersystem.CheckOperations import (get_total,
                                                 get_total_tax,
                                                 get_order_subtotal)


class SpreadsheetArea(object):
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

    @var format_dict: dict that maps str to xlsxwriter.Formats. This
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
    TOTAL_AREA_ROW_HEIGHT = 30

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
    DATA_ROW_HEIGHT = 20

    #////////////////////////////////////////////////////////////////////////////////
    # These constants shouldn't be edited. They are relative to other defined
    # constants and any changes in the editable constants will be reflected here
    #////////////////////////////////////////////////////////////////////////////////
    # Alter by one because of zero based indexing
    _DATA_AREA_START = _TOTAL_AREA_END + 1

    #////////////////////////////////////////////////////////////////////////////////

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

        self.row = self._DATA_AREA_START + self.initial_row
        return self.initial_row, self.initial_col + self.AREA_COL_NUM

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
        self._set_worksheet_column(first_col=self.col, last_col=self.col,
                                   width=self.AREA_COL_WIDTH, format=format)

    def _format_area_columns_ends_right(self):
        """Formats the right most end column for
        the area.

        @return: None
        """
        format = self.format_dict['right_column']
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
        return self.format_dict['main_title_data_format']

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
        return self.format_dict['datetime_format']

    def _get_format_date_title(self):
        """Gets the format for the date title

        @return xlsxwriter.Format object that
        represents the format for the displayed
        date title.
        """
        return self.format_dict['title_format_left']

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
        if not totals_data or not len(totals_data) == expected_length:
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
        return self.format_dict['title_format_left']

    def _get_format_total_data(self):
        """Gets the format for the total data.

        @return: xlsxwriter.Format that represents
        the format for the total data.
        """
        return self.format_dict['total_data_format']

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
        return self.format_dict['subtitle_format_left']

    def _get_format_subtotal_data(self):
        """Gets the format for displaying the subtotal data.

        @return: xlsxwriter.Format object that is used
        to display the format of the subtotal data.
        """
        return self.format_dict['subtotal_data_format']

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
            print 'boom'
        if last_col < 0:
            last_col = self.area_end_col
        if not width:
            width = self.AREA_COL_WIDTH

        self._worksheet.set_column(first_col, last_col, width, cell_format=format)


class GeneralDatesheetOrderArea(SpreadsheetArea):
    """GeneralDatesheetOrderArea represents a general
    order that is described through a PackagedOrderData
    object and stores information regarding a single order.

    This order area is used to parse and display data from
    the PackagedOrderData.

    @var: packaged_data: PackagedOrderData information that
    this area should display.
    """

    def __init__(self, packaged_data, format_dict):
        """Initializes the GeneralDatesheetOrderArea
        object with the packaged data.

        @param packaged_data: PackagedOrderData object
        that represents the order areas data.

        @param format_dict: dict that maps str to
        xlsxwriter.Formats that represent the formats
        for cells.
        """
        self.packaged_data = packaged_data
        super(GeneralDatesheetOrderArea, self).__init__(format_dict)

    def connect(self, worksheet):
        """Override Method.

        Connects the area to the worksheet.

        @param worksheet: xlsxwriter.worksheet.Worksheet
        object that represents the worksheet where
        the area will be added.

        @return: 2 tuple of (int, int) representing the
        row and column that the area terminates at. This
        is the coordinates for the upper right hand corner
        where another area could be added.
        """
        values = super(GeneralDatesheetOrderArea, self).connect(worksheet)
        self.update_title_data()
        self.update_total_data()
        self.update_items_data()
        return values

    def _update_items_data(self):
        """Updates the items data by adding
        all the data stored in the packaged
        data to the data area.

        @return: None
        """
        for item in self.packaged_data.data:
            self._write_item(item)

    def update_title_data(self):
        """Override Method.

        Updates the title data

        @return: None
        """
        name = self.packaged_data.name
        date = self.packaged_data.datetime

        super(GeneralDatesheetOrderArea, self).update_title_data(name, date)

    def update_total_data(self):
        """Override Method.

        Updates the total data.

        @return: None
        """
        totals = self._get_total_data()
        subtotals = self._get_subtotal_data()

        super(GeneralDatesheetOrderArea, self).update_total_data(totals,subtotals)

    def _get_total_data(self):
        """Gets the total data stored in this
        areas packaged data.

        @return: tuple where each entry represents the
        (str, float) where the values are the total name
        and total data respectively.
        """
        return ('total', self.packaged_data.totals['total']),

    def _get_subtotal_data(self):
        """Gets the subtotal data stored in this
        areas packaged data.

        @return: tuple where each entry represents the
        (str, float) where the values are the subtotal name
        and the subtotal data respectively.
        """
        return (
            ('tax', self.packaged_data.totals['tax']),
            ('subtotal', self.packaged_data.totals['subtotal'])
        )

    def add(self, menu_item):
        """Adds the given item to the
        data area and updates the totals.

        @raise ValueError: If non MenuItem
        object is given.

        @param menu_item: MenuItem object
        that represents the item to be
        displayed.

        @return: None
        """
        is_menu_item(menu_item)
        self._add_menu_item(menu_item)
        self.update_total_data()

    def _add_menu_item(self, menu_item):
        """Adds the menu_item data to the
        data area.

        @param menu_item: MenuItem object
        that is to be added to the data area.

        @return: None
        """
        self._update_packaged_data(menu_item)
        self._write_item(menu_item)

    def _update_packaged_data(self, menu_item):
        """Updates the packaged data item area
        and data totals areas respectively.

        @param menu_item: MenuItem object that
        is to be used to update the packaged
        data.

        @return: None
        """
        self._update_packaged_data_item(menu_item)
        self._update_packaged_data_totals(menu_item)

    def _update_packaged_data_item(self, menu_item):
        """Updates the packaged data item list with
        the given MenuItem.

        @param menu_item: MenuItem object that is
        to be added to the packaged data's item list.

        @return: MenuItem object that was added.
        """
        self.packaged_data.data.append(menu_item)
        return menu_item

    def _update_packaged_data_totals(self, menu_item):
        """Updates the packaged data totals area with
        the given MenuItems data.

        @param menu_item: MenuItem object that is
        used to update the totals.

        @return: 3 tuple of (float, float, float)
        representing the total, tax, and subtotal
        associated with the MenuItem respectively.
        """
        subtotal = get_order_subtotal((menu_item,))
        tax = get_total_tax(subtotal)
        total = get_total((menu_item,))

        self.packaged_data.totals['total'] += total
        self.packaged_data.totals['tax'] += tax
        self.packaged_data.totals['subtotal'] += subtotal

        return total, tax, subtotal

    def _write_item(self, menu_item):
        """Writes the MenuItems data to the data
        area.

        @param menu_item: MenuItem object that is
        to be added to the area.

        @return: 2 tuple of (int, int) representing the
        row and column that it is safe to append more data
        to after the item has been written.
        """
        row, col = self._write_item_name(menu_item.get_name())
        row, col = self._write_item_price(menu_item.get_price())
        self.row = row

        row, col = self._write_item_stars(menu_item.stars)
        self.row = row

        row, col = self._write_item_options(menu_item.options)
        self.row = row

        row, col = self._write_item_note(menu_item.notes)
        self.row = row

        return self.row, col

    def _write_item_name(self, item_name):
        """Writes the items name to the data
        area.

        @param item_name: str representing the
        items name.

        @return: 2 tuple of (int, int) representing
        the row and column that it is safe to
        append more data to after this procedure.
        """
        format = self._get_item_name_format()
        self.write_data(item_name, format=format)
        return self.row + 1, self.col

    def _get_item_name_format(self):
        """Gets the format associated with the
        item name.

        @return: xlsxwriter.Format that represents
        the format for the name data.
        """
        return self.format_dict['item_data_format_left']

    def _write_item_price(self, item_price):
        """Writes the items price data to the
        data area.

        @param item_price: float representing
        the items price.

        @return:2 tuple of (int, int) representing
        the row and column that it is safe to
        append more data to after this procedure.
        """
        format = self._get_item_price_format()
        self.write_data(item_price, col=self.area_end_col, format=format)
        return self.row + 1, self.col

    def _get_item_price_format(self):
        """Gets the format for the item price.

        @return: xlsxwriter.Format that represents
        the format for the price to be written.
        """
        return self.format_dict['total_data_format']

    def _write_item_stars(self, item_stars):
        """Writes the item stars data to the
        data area.

        @param item_stars: int representing the
        number of stars associated with the item.

        @return:2 tuple of (int, int) representing
        the row and column that it is safe to
        append more data to after this procedure.
        """
        self._write_item_stars_name()
        self._write_item_stars_value(item_stars)
        return self.row + 1, self.col

    def _write_item_stars_name(self):
        """Writes the item stars name data.

        @return: None
        """
        format = self._get_item_stars_name_format()
        self.write_data('stars', format=format)

    def _get_item_stars_name_format(self):
        """Gets the format associated with the
        item stars name.

        @return: xlsxwriter.Format that represents
        the format for displaying the item stars name.
        """
        return self.format_dict['subitem_data_format_left']

    def _write_item_stars_value(self, value):
        """Writes the item stars value to the
        data area.

        @param value: int representing the stars
        value.

        @return: None
        """
        format = self._get_item_stars_value_format()
        self.write_data(value, col=self.col + 1, format=format)

    def _get_item_stars_value_format(self):
        """Gets the format for displaying the
        item stars value.

        @return: xlsxwriter.Format that represents
        the format to display the item stars value.
        """
        return self.format_dict['subitem_data_format_center']

    def _write_item_options(self, item_options):
        """Writes the item options to the data area.

        @param item_options: list of OptionItem
        objects that represents the options to be
        written to the data area.

        @return:2 tuple of (int, int) representing
        the row and column that it is safe to
        append more data to after this procedure.
        """
        col = self.col + 1
        row_counter = self.row

        self._write_item_options_title()

        for item in item_options:
            name = item.get_name()
            price = item.get_price()

            format = self._get_item_option_name_format()
            self.write_data(name, row=row_counter, col=col,
                            format=format)

            format = self._get_item_option_price_format()
            self.write_data(price, row=row_counter, col=self.area_end_col,
                            format=format)

            row_counter += 1

        return row_counter, self.col

    def _write_item_options_title(self):
        """Writes the item options title to
        the data area.

        @return: None
        """
        format = self._get_item_options_title_format()
        self.write_data('options', format=format)

    def _get_item_options_title_format(self):
        """Gets the format associated with the
        item options title.

        @return: xlsxwriter.Format that is used
        to display the item options title.
        """
        return self.format_dict['subitem_data_format_left']

    def _get_item_option_name_format(self):
        """Gets the format that is used to
        display the item options name

        @return: xlsxwriter.Format that represents
        the format to display the item options name.
        """
        return self.format_dict['subitem_data_format_center']

    def _get_item_option_price_format(self):
        """Gets the format that is used to
        display the item option price.

        @return: xlsxwriter.Format that is used
        to display the item option price.
        """
        return self.format_dict['subitem_data_total_format']

    def _write_item_note(self, item_note):
        """Writes the item note data to the
        data area.

        @param item_note: str representing the
        note associated with the item

        @return:2 tuple of (int, int) representing
        the row and column that it is safe to
        append more data to after this procedure.
        """
        self._write_item_note_title()
        self._write_item_note_data(item_note)

        return self.row + 1, self.col

    def _write_item_note_title(self):
        """Writes the item note title to the
        data area.

        @return: None
        """
        format = self._get_item_note_title_format()
        self.write_data('note', format=format)

    def _get_item_note_title_format(self):
        """Gets the format used to display
        the item note title.

        @return: xlsxwriter.Format that is
        used to display the item note title.
        """
        return self.format_dict['subitem_data_format_left']

    def _write_item_note_data(self, data):
        """Writes the item note data to the
        data area.

        @param data: str representing the item
        note data to be written.

        @return: None
        """
        format = self._get_item_note_data_format()
        self.write_data(data, col=self.col + 1, format=format)

    def _get_item_note_data_format(self):
        """Gets the format used to display
        the item note data.

        @return: xlsxwriter.Format that is used
        to display the item note data.
        """
        return self.format_dict['subitem_data_format_center']