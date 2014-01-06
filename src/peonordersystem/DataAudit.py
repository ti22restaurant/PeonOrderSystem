"""DataAudit module holds the necessary functions and
information for auditing previous orders and compiling
them into an xls document that is more human readable.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""
import os
import jsonpickle
import xlsxwriter
from datetime import time, date, datetime, timedelta

from src.peonordersystem.PackagedData import PackagedOrderData
from src.peonordersystem.Settings import SQLITE_DATE_TIME_FORMAT_STR
from src.peonordersystem import path
from src.peonordersystem.MenuItem import MenuItem, DiscountItem
from src.peonordersystem import ConfirmationSystem

#====================================================================================
# This block in the module generates and checks the necessary directories,
# as well as creates the module wide constants.
#====================================================================================
ORDERS_DIRECTORY = path.SYSTEM_ORDERS_PATH
AUDIT_DIRECTORY = path.SYSTEM_AUDIT_PATH

TODAY = datetime.now()
TODAY_DIRECTORY = AUDIT_DIRECTORY + '/' + TODAY.strftime('%Y/%m/%d')

if not os.path.exists(TODAY_DIRECTORY):
    os.mkdir(TODAY_DIRECTORY)

REQUEST_DIRECTORY = AUDIT_DIRECTORY + "/requests"

if not os.path.exists(REQUEST_DIRECTORY):
    os.mkdir(REQUEST_DIRECTORY)

#====================================================================================
# This block represents constants utilized in generating the title area
#====================================================================================
TITLE_ROW_START = 0
TITLE_ROW_END = 2

TITLE_AREA_ROW_HEIGHT = 30

TITLE_AREA_FORMAT = {'bottom': 1,
                     'bold': True,
                     'align': 'center',
                     'valign': 'vcenter',
                     'font_size': 10}

DATE_FORMAT = {'num_format': 'd mmmm yyyy'}
DATE_TIME_FORMAT = {'num_format': 'dd/mm/yy hh:mm:ss'}

#====================================================================================
# This block represents constants utilized in generating the totals area
#====================================================================================
TOTAL_AREA_ROW_START = TITLE_ROW_END
TOTAL_AREA_ROW_END = TOTAL_AREA_ROW_START + 2

TOTAL_AREA_ROW_HEIGHT = 20

TOTAL_DATA_FORMAT = {'top': 1,
                     'bottom': 1,
                     'bold': True,
                     'valign': 'vcenter',
                     'font_size': 10}

SUBTOTAL_DATA_FORMAT = {'top': 1,
                        'bottom': 1,
                        'font_color': 'gray',
                        'valign': 'vcenter',
                        'font_size': 8}

MONEY_FORMAT = {'num_format': '$#,##0.00;[Red]-$#,##0.00'}

#====================================================================================
# This block represents constants utilized in generating an arbitrary area.
#====================================================================================
AREA_COL_NUM = 2
AREA_COL_WIDTH = 20

#====================================================================================
# This block represents constants utilized in generating formats
#====================================================================================
format_dict = {}

BOLD_TOP_BORDER_FORMAT = {'top': 2,
                          'bold': True}

BOLD_BOTTOM_BORDER_FORMAT = {'bottom': 2,
                             'bold': True}

LEFT_COL_FORMAT = {'left': 1,
                   'align': 'left'}

RIGHT_COL_FORMAT = {'right': 1,
                    'align': 'right'}

ITEM_NOTE_FORMAT = {'text_wrap': True,
                    'font_color': 'gray',
                    'font_size': 9}

ITEM_INFO_FORMAT = {'font_color': 'gray',
                    'font_size': 10,
                    'indent': 1}

NOTIF_TIME_FORMAT = {'font_color': 'gray',
                     'font_size': 10,
                     'indent': 1,
                     'num_format': 'hh:mm:ss'}

ORDER_SUBTOTAL_FORMAT = {'font_color': 'gray',
                         'font_size': 8,
                         'num_format': '$#,##0.00'}


#====================================================================================
# This block represents all functions generally usable by any type of sheet.
#====================================================================================
def create_formats(workbook):
    """Creates the formats and stores them in a dict
    that is globally accessible.

    @param workbook: xlsxwriter.Workbook object that
    represents the workbook to have the format data
    added to it.

    @return: None
    """
    global format_dict

    format_dict = {}

    format_dict['title_format'] = workbook.add_format(TITLE_AREA_FORMAT)

    format_dict['total_data_format'] = workbook.add_format(TOTAL_DATA_FORMAT)
    format_dict['subtotal_data_format'] = workbook.add_format(SUBTOTAL_DATA_FORMAT)

    format_dict['date_format'] = workbook.add_format(DATE_FORMAT)
    format_dict['datetime_format'] = workbook.add_format(DATE_TIME_FORMAT)
    format_dict['notif_time_format'] = workbook.add_format(NOTIF_TIME_FORMAT)

    format_dict['money_format'] = workbook.add_format(MONEY_FORMAT)
    format_dict['orders_subtotals_format'] = workbook.add_format(ORDER_SUBTOTAL_FORMAT)

    format_dict['note_format'] = workbook.add_format(ITEM_NOTE_FORMAT)
    format_dict['item_info_format'] = workbook.add_format(ITEM_INFO_FORMAT)

    format_dict['top_border'] = workbook.add_format(BOLD_TOP_BORDER_FORMAT)
    format_dict['bottom_border'] = workbook.add_format(BOLD_BOTTOM_BORDER_FORMAT)

    format_dict['left_column'] = workbook.add_format(LEFT_COL_FORMAT)
    format_dict['right_column'] = workbook.add_format(RIGHT_COL_FORMAT)


def create_standard_worksheet_format(worksheet):
    """Creates the general format for the first
    rows of the worksheet. This format is standard
    to all worksheets.

    @param worksheet: xlsxwriter.Worksheet object
    that represents the worksheet to be formatted.

    @return: None
    """
    title_format = format_dict['title_format']

    total_area = format_dict['total_data_format']
    subtotal_area = format_dict['subtotal_data_format']

    top_format = format_dict['top_border']
    bottom_format = format_dict['bottom_border']

    #================================================================================
    # Generate title area rows formatting.
    #================================================================================
    start_row = TITLE_ROW_START

    for x in range(TITLE_ROW_END - TITLE_ROW_START):
        worksheet.set_row(start_row + x, TITLE_AREA_ROW_HEIGHT, title_format)


    #================================================================================
    # Generate total area rows formatting.
    #================================================================================
    start_row = start_row + TITLE_ROW_END

    change_in_rows = TOTAL_AREA_ROW_END - TOTAL_AREA_ROW_START
    format_data = [total_area] + [subtotal_area for x in range(change_in_rows)]

    index = 0
    for frmt in format_data:
        worksheet.set_row(start_row + index, TOTAL_AREA_ROW_HEIGHT, frmt)
        index += 1

    return None


def _format_columns(worksheet, start_column, end_column):
    """Formats the columns within the range.

    @param start_column: int representing the starting
    column.

    @param end_column: int representing the ending
    column.

    @return: None
    """
    left_col = format_dict['left_column']
    right_col = format_dict['right_column']

    #================================================================================
    # Generate columns format.
    #================================================================================
    worksheet.set_column(start_column, start_column, AREA_COL_WIDTH, left_col)

    if (end_column - start_column) > 0:
        worksheet.set_column(start_column + 1, end_column - 1, AREA_COL_WIDTH)

    worksheet.set_column(end_column, end_column, AREA_COL_WIDTH, right_col)


def _generate_title_area(worksheet, start_row, start_column, curr_date, title):
    """Generates the title area with the given date and title.

    @param worksheet: xlsxwriter.Worksheet object that
    represents the worksheet that the title area should
    be generated in.

    @param start_column: int representing the starting
    column for the title area to populate.

    @param start_row: int representing the starting
    row for the title area to populate

    @param curr_date: datetime.datetime object representing
    the time of the order.

    @param title: str representing the name associated with
    the order.

    @return: tuple of (int, int) representing the
    row and column that the title area terminates at
    respectively.
    """
    last_column = start_column + AREA_COL_NUM
    curr_row = start_row
    title_format = format_dict['title_format']
    date_format = format_dict['datetime_format']

    #================================================================================
    # Generate main title and date
    #================================================================================
    worksheet.merge_range(start_row, start_column, start_row, last_column,
                          data=title, cell_format=title_format)
    curr_row += 1

    worksheet.write(curr_row, start_column, 'Date: ', title_format)
    worksheet.write_datetime(curr_row, start_column + 1, curr_date, date_format)
    curr_row += 1

    return curr_row, start_column


#====================================================================================
# This block represents all functions that are used for generating data for the
# general date sheet which displays orders for that date, notification data for
# the date and every associated order in three distinct areas.
#
#   These areas are known as:
#
#   1. main area: Displays the overview for that date.
#   2. notification area: Displays overview of all notification items on that date.
#   3. order area: Displays n areas where each area represents an order,
#                  with n orders for that date. This allows for a more
#                  comprehensive view of all orders made.
#====================================================================================
def generate_date_sheet(worksheet, row, column, curr_date, packaged_orders_data):
    """Generates the date sheet area including main area, notification area and
    order data areas. All of this data will be pulled from the supplied packaged
    orders data.

    @param worksheet: xlsxwriter.Worksheet that represents
    the worksheet the data should be added to.

    @param row: int representing the row number the data
    should be generated at.

    @param column: int representing the starting column
    number the data should be generated at.

    @param curr_date: Datetime.date object representing
    the date of this date audit.

    @param packaged_orders_data: list of PackagedOrderData
    objects that represents the order data.

    @return: None
    """
    last_column = column + AREA_COL_NUM

    _format_columns(worksheet, column, last_column)
    curr_row, curr_col = _generate_title_area(worksheet, row, column, curr_date,
                                              'Orders for Date')

    #================================================================================
    # Generate constants utilized for building totals area.
    #================================================================================
    totals_area = curr_row
    curr_row += TOTAL_AREA_ROW_END - TOTAL_AREA_ROW_START + 1

    total = 0.0
    subtotal = 0.0
    tax = 0.0

    #================================================================================
    # Generate constants utilized for building notifications area.
    #================================================================================
    notification_area = last_column + 1
    curr_col = notification_area + AREA_COL_NUM + 1

    notification_data = []

    #================================================================================
    # Generate orders data
    #================================================================================
    for packaged_order in packaged_orders_data:
        order_name = packaged_order.name
        order_date = packaged_order.date
        totals = packaged_order.totals

        #============================================================================
        # update constants
        #============================================================================
        total += totals['total']
        subtotal += totals['subtotal']
        tax += totals['tax']

        notification_data += packaged_order.notification_data

        #============================================================================
        # add remaining data to orders table
        #============================================================================
        curr_row, col = add_order_data(worksheet, curr_row, column, order_name,
                                       order_date, totals)

        #============================================================================
        # Generate data for specific order beyond notification area.
        #============================================================================
        date_sheet_create_order_area(worksheet, row, curr_col, packaged_order)
        curr_col += AREA_COL_NUM + 1

    #================================================================================
    # Generate totals area
    #================================================================================
    money_format = format_dict['money_format']

    worksheet.write(totals_area, column, 'Date Total:')
    worksheet.write(totals_area, last_column, total, money_format)
    totals_area += 1

    worksheet.write(totals_area, column, 'Date Tax: ')
    worksheet.write(totals_area, last_column, tax, money_format)
    totals_area += 1

    worksheet.write(totals_area, column, 'Date Subtotal: ')
    worksheet.write(totals_area, last_column, subtotal, money_format)

    #================================================================================
    # Generate notifications area
    #================================================================================
    date_sheet_create_notification_area(worksheet, row, notification_area, curr_date,
                                        notification_data)

    return curr_row, column


def date_sheet_create_notification_area(worksheet, first_row, first_column,
                                        curr_date, notification_data):
    """Creates the notification area for the date sheet. This
    area is used to display all notification data for the date
    sheet.

    @param worksheet: xlsxwriter.Worksheet object that
    represents the worksheet the area should be written to.

    @param row: int representing the number of the row
    that the area should be added at.

    @param column: int representing the number of the
    column the area should be added at.

    @return: tuple of (int, int) that represents
    the row and column of the bottom left hand corner
    of the area. This is the area where the notification
    area terminates.
    """
    last_column = first_column + AREA_COL_NUM

    _format_columns(worksheet, first_column, last_column)
    curr_row, col = _generate_title_area(worksheet, first_row, first_column,
                                         curr_date, "Notification Data")

    #================================================================================
    # Generate totals area
    #================================================================================
    totals_area = curr_row

    # generate totals area moved lower to increase performance.

    curr_row += TITLE_ROW_END - TITLE_ROW_START + 1

    #================================================================================
    # Generate notification data
    #================================================================================
    num = 0

    for item in notification_data:
        curr_row, col = add_notification_item(worksheet, curr_row, first_column,
                                              curr_date, item)
        if isinstance(item, DiscountItem):
            num += 1

    #================================================================================
    # Generate totals area
    #================================================================================
    worksheet.write(totals_area, first_column, 'Total Notifications:')
    worksheet.write(totals_area, last_column, len(notification_data))
    totals_area += 1

    worksheet.write(totals_area, first_column, 'Total Discounts: ')
    worksheet.write(totals_area, last_column, num)
    totals_area += 1

    worksheet.write(totals_area, first_column, 'Total Comps: ')
    worksheet.write(totals_area, last_column, len(notification_data) - num)
    totals_area += 1

    return curr_row, first_column


def date_sheet_create_order_area(worksheet, first_row, first_column,
                                 packaged_order_data):
    """Creates the order area for displaying orders on the
    date sheet. The area is generated from the given column
    and row.

    @param worksheet: xlsxwriter.Worksheet object
    representing the worksheet to have the order area
    added to it.

    @param first_row: int representing the first
    row where the order area is to be created.

    @param first_column: int representing the
    first column where the order area is to be
    created.

    @return: tuple of (int, int) representing
    the (row, col) as the bottom left hand corner
    of which the created area stops.
    """
    curr_date = packaged_order_data.date
    name = packaged_order_data.name
    data = packaged_order_data.data

    totals = packaged_order_data.totals

    last_column = first_column + AREA_COL_NUM

    _format_columns(worksheet, first_column, last_column)
    curr_row, col = _generate_title_area(worksheet, first_row, first_column,
                                         curr_date, name)
    #================================================================================
    # Generate totals area.
    #================================================================================
    money_format = format_dict['money_format']

    worksheet.write(curr_row, first_column, 'Order Total: ')
    worksheet.write(curr_row, last_column, totals['total'], money_format)
    curr_row += 1

    worksheet.write(curr_row, first_column, 'Order Tax: ')
    worksheet.write(curr_row, last_column, totals['tax'], money_format)
    curr_row += 1

    worksheet.write(curr_row, first_column, 'Order Subtotal: ')
    worksheet.write(curr_row, last_column, totals['subtotal'], money_format)
    curr_row += 1

    #================================================================================
    # Generate menu items data
    #================================================================================

    for item in data:
        row, col = add_menu_item(worksheet, curr_row, first_column, item)
        curr_row = row

    return curr_row, first_column


def add_order_data(worksheet, first_row, first_column, order_name, order_date,
                   totals):
    """Adds the given order data as a set of rows in the specified area.

    @param worksheet: xlsxwriter.Worksheet that represents the
    area where the data should be written to.

    @param first_row: int representing the starting row
    that the data should be written to.

    @param first_column: int representing the starting
    column to which the data should be written.

    @param order_name: str representing the order name
    associated with the order.

    @param order_date: datetime.datetime object representing
    the date and time of the order.

    @param totals: dict that maps strs to keys of float values.
    Expect the totals to contain the keys

        {'total': int representing the total associated with the order,
        'tax': int representing the tax associated with the order,
        'subtotal': int representing the subtotal associated with the order
        }

    @return: tuple of (int, int) representing the row and column
    that terminates the addition. This is the area it is safe to add
    more data.
    """
    money_format = format_dict['money_format']
    time_format = format_dict['notif_time_format']
    subtotals_format = format_dict['orders_subtotals_format']

    curr_row = first_row
    last_column = first_column + AREA_COL_NUM

    worksheet.write(curr_row, first_column, order_name)
    worksheet.write(curr_row, first_column + 1, order_date, time_format)
    worksheet.write(curr_row, last_column, totals['total'], money_format)
    curr_row += 1

    worksheet.write(curr_row, last_column, totals['tax'], subtotals_format)
    curr_row += 1

    worksheet.write(curr_row, last_column, totals['subtotal'], subtotals_format)
    curr_row += 1

    return curr_row + 1, first_column


def add_menu_item(worksheet, first_row, first_column, menu_item):
    """Adds the given MenuItem at the given row and column. The
    menu item data will take up a single row.

    @param worksheet: xlsxwriter.Worksheet object that
    represents the worksheet that the data should be
    added to.

    @param row: int representing the starting row for the
    MenuItem data to be added.

    @param column: int representing the starting column for
    the MenuItem data to be added.

    @param menu_item: MenuItem object representing the data
    to be added.

    @return: tuple of (int, int) that represents the area
    that it is safe to add more data beneath the added menu item.
    """
    money_format = format_dict['money_format']
    worksheet.write(first_row, first_column, menu_item.get_name())
    worksheet.write(first_row, first_column + AREA_COL_NUM, menu_item.get_price(),
                    money_format)

    return first_row + 1, first_column


def add_notification_item(worksheet, first_row, first_column, notification_date,
                          notification_item):
    """Adds a notification item tot he given row, starting at
    the given column.

    @param worksheet: xlsxwriter.Worksheet object that
    represents the worksheet that the area should be
    added to.

    @param first_row: int representing the row that the
    notification item should be added at.

    @param first_column: int representing the column that
    the notification item should be added at.

    @param notification_date: datetime.datetime object that
    represents when the notification item was checked out.

    @param notification_item: MenuItem object that represents
    the notification item.

    @return: tuple of (int, int) representing the row and
    column that it is safe to add additional items or data
    onto. This is the area where the item data has terminated.
    """
    datetime_format = format_dict['notif_time_format']
    money_format = format_dict['money_format']
    note_format = format_dict['note_format']
    item_info_format = format_dict['item_info_format']

    last_column = first_column + AREA_COL_NUM
    curr_row = first_row

    #================================================================================
    # Write standard notification data
    #================================================================================

    worksheet.write(curr_row, first_column, notification_item.get_name())
    worksheet.write(curr_row, first_column + 1, notification_item._notification_message,
                    note_format)
    worksheet.write(curr_row, last_column, notification_item.get_price())
    curr_row += 1

    #================================================================================
    # Write date notification data.
    #================================================================================
    worksheet.write(curr_row, first_column, 'Ordered At: ', item_info_format)
    worksheet.write_datetime(curr_row, first_column + 1, notification_date,
                             datetime_format)
    curr_row += 1

    #================================================================================
    # Write type notification data.
    #================================================================================
    item_type = 'Comped Item'
    if isinstance(notification_item, DiscountItem):
        item_type = 'Discount Item'

    worksheet.write(curr_row, first_column, 'Type:', item_info_format)
    worksheet.write(curr_row, first_column + 1, item_type, item_info_format)

    return curr_row + 1, first_column
