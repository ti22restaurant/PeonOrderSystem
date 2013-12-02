"""DataAudit module holds the necessary functions and
information for auditing previous orders and compiling
them into an xls document that is more human readable.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

from src.peonordersystem.ConfirmationSystem import parse_standardized_file_name
from src.peonordersystem import CheckOperations
from src.peonordersystem import path
from src.peonordersystem.Settings import AUDIT_FILE_TYPE, \
    CLOSING_AUDIT_DEFAULT_NAME

import jsonpickle
import datetime
import xlwt
import time
import os

#================================================
# This block in the module generates and
# checks the necessary directories, as well as
# creates the module wide constants.
#================================================

ORDERS_DIRECTORY = path.SYSTEM_ORDERS_PATH
AUDIT_DIRECTORY = path.SYSTEM_AUDIT_PATH

TODAY_DIRECTORY = AUDIT_DIRECTORY

TODAYS_DATE = time.localtime()[:3]

for value in TODAYS_DATE:
    TODAY_DIRECTORY += "/{}".format(value)
    if not os.path.exists(TODAY_DIRECTORY):
        os.mkdir(TODAY_DIRECTORY)

REQUEST_DIRECTORY = AUDIT_DIRECTORY  + "/requests"

if not os.path.exists(REQUEST_DIRECTORY):
    os.mkdir(REQUEST_DIRECTORY)


MERGED_STYLE = xlwt.easyxf('pattern: pattern solid, fore_colour white;'
                           'align: vertical center, horizontal center;'
                           'font: height 200, bold on; border: left thin, '
                           'right thin, top thin, bottom thin')

ORDER_LEFT_BORDER = xlwt.easyxf('border: left thick')
ORDER_RIGHT_BORDER = xlwt.easyxf('border: right thick')

ORDERS_COLUMN_WIDTH = 5


def closing_audit():
    """Initiates a closing audit which generates
    the daily audit information and stores it in the
    specified audit area under the directory associated
    with the current date.

    @return: None
    """
    today = datetime.date(TODAYS_DATE[0], TODAYS_DATE[1], TODAYS_DATE[2])
    print today
    workbook = audit_data(today, today)

    closing_audit_filepath = TODAY_DIRECTORY + '/' + CLOSING_AUDIT_DEFAULT_NAME
    closing_audit_filepath = get_acceptable_filepath(closing_audit_filepath)
    workbook.save(closing_audit_filepath)


def request_audit(from_date, until_date, location=REQUEST_DIRECTORY,
                  name='Audit'):
    """Performs an audit over the selected date
    period.

    @param from_date: datetime.date object that represents
    the starting date that the audit should begin on, inclusive.

    @param until_date: datetime.date object that represents
    the ending date that the audit should conclude on, inclusive.

    @param name: str representing the name of the file that will
    be stored in the audit requests area.

    @return: None
    """
    from_date_str = str(from_date.month) + '-' + str(from_date.day) + '-' + \
                    str(from_date.year)
    until_date_str = str(until_date.month) + '-' + str(until_date.day) + '-' \
                     + str(until_date.year)

    str_date_range = '[' + from_date_str + ',' + until_date_str + ']'

    request_audit_filepath = location + '/' + name + str_date_range

    request_audit_filepath = get_acceptable_filepath(request_audit_filepath)

    workbook = audit_data(from_date, until_date)

    workbook.save(request_audit_filepath)


def get_acceptable_filepath(file_path):
    """checks if the given filepath is
    able to be used. Returns an updated file
    path that should be acceptable to be used
    without overwriting other files.

    @param file_path: str representing the
    entire file path that is to be checked.

    @return: str representing the updated file
    path.
    """
    counter = 1

    new_file_path = file_path.split('.')[0] + AUDIT_FILE_TYPE

    print os.path.exists(file_path)

    while os.path.exists(new_file_path):
        new_file_path = file_path.split('.')[0] + "(" + str(counter) + ")" + \
                        AUDIT_FILE_TYPE
        counter += 1

    return new_file_path


def audit_data(from_date, until_date):
    """Audits the data by retrieving the
    necessary information and parsing it
    into a human readable .xls file.

    @warning: Compiling these .xls files is
    costly and as such this function should
    only be called sparingly.

    @param from_date: datetime.date object
    that represents the starting date for
    the data to be gathered from, inclusive.

    @param until_date: datetime.date object
    that represents the ending date for the
    data to be gathered until, inclusive.

    @return: xlwt.Workbook representing the
    workbook that all of the information was
    added to.
    """
    workbook = xlwt.Workbook()
    data_files = _get_data(from_date, until_date)

    subtotal_by_audit = 0.0
    tax_by_audit = 0.0

    frequency_by_audit = {}
    total_items_by_audit = 0

    start_date = '{}/{}/{}'.format(from_date.month, from_date.day,
                                   from_date.year)
    end_date = '{}/{}/{}'.format(until_date.month, until_date.day,
                                 until_date.year)

    audit_sheet = workbook.add_sheet('AUDIT SHEET')

    # The structure of this spreadsheet file is kind of difficult to grasp.
    # Therefore this will be a handy guide.
    #
    # First there is an 'AUDIT SHEET' that represents data collected
    # from all orders in the date frame specified for this audit.
    #
    # For any given audit there will only be a single AUDIT SHEET that
    # will act as the summary of the data. This will be the first sheet.
    #
    # Every subsequent sheet can be seen as "children" (weak sense,
    # as in as a structural child). As such each additional sheet represents a
    # single date in between the from_date to the until_date which offers
    # more in depth information regarding the orders that day.
    #
    # Each AUDIT SHEET contains two areas:
    #
    # Total area:
    #
    #     This area is designed to display every MenuItem
    #     associated with the entire audit, and sum them all for a
    #     grand audit total that tells how much subtotal/tax/total
    #     was obtained during this audit period.
    #
    #     It is expected that the Total area will be the first area
    #     generated as it is most likely of the most interest. This
    #     doesn't necessarily have to be the case though. Its columns
    #     may be edited via its column area constants.
    #
    #     For the sake of speed and limiting redundancy the total
    #     is generated and appended to throughout to kept a running
    #     update of the MenuItems. As such there will be a defined
    #     total area that will remain a constant in that will refer
    #     to this areas columns.
    #
    #
    # Breakdown area:
    #
    #     This area is designed to display every MenuItem that was
    #     ordered and a frequency representing the number of times it
    #     was ordered. Finally it will also calculate their frequency as
    #     a percentage and display that information
    #
    #     It is expected that the Breakdown area will be the second area
    #     generated. This doesn't necessarily have to be the case though.
    #     Its columns may be edited via its column area constants.
    #
    #     All generation of the breakdown area is done via accessing both
    #     an updating dict that contains all menu item information regarding
    #     frequency and a running total for quick percentage calculations.
    #     The breakdown generation is expected after other methods of
    #     processing data are complete, but its location is stored to give
    #     it priority. As such there will be a defined breakdown area that
    #     will remain constant and will refer to the area columns.
    #
    #
    # Sheet structure:
    #
    # Each column counter represents a width of columns that
    #  are considered all at once:
    #
    #   0th row ->  |******|*****|******|*/.../**|******|
    #       |       |******|*****|******|*/.../**|******|
    #       |       |******|*****|******|*/.../**|******|
    #       |       |******|*****|******|*/.../**|******|
    #       V       ...
    #   nth row ->  |******|*****|******|*/.../**|******|
    #               0th column  ------------>     nth column
    #
    #     Each segment holds n total rows.
    #     Each row segment is controlled via updating counters throughout
    #     each updating phase. All have been named appropriately. All functions
    #     that are called to update rows return the updated row, except for
    #     finalize functions which sometimes return unique data.
    #
    #     Finally rows/cols are inclusive. So when counters update they must
    #     add += ORDERS_COLUMN_WIDTH + 1
    #
    #     Each segment holds n total columns.
    #     Each column segment is contains ORDERS_COLUMN_WIDTH number of
    #     columns. As such:
    #
    #         column_counter - ORDERS_COLUMN_WIDTH = 0th column in the segment
    #         (first column)
    #
    #         column_counter = nth column in the segment (final column)
    #
    # NOTE: AUDIT SHEET updating areas that are mixed in with DATE SHEET
    # updating areas will be enclosed by comment blocks to allow for simply
    # future editing.

    audit_column_counter = ORDERS_COLUMN_WIDTH

    # Generate audit wide total area.
    audit_total_title = 'TOTAL for ' + start_date + ' to ' + end_date
    AUDIT_TOTAL_AREA = (audit_column_counter - ORDERS_COLUMN_WIDTH,
                        audit_column_counter)
    audit_total_row = _add_order_header(audit_sheet, 0, AUDIT_TOTAL_AREA[0],
                                        AUDIT_TOTAL_AREA[1], audit_total_title)
    audit_column_counter += ORDERS_COLUMN_WIDTH + 1

    # Reserve audit wide breakdown area.
    audit_breakdown_title = 'Menu Item Breakdown for ' + start_date + ' to ' +\
                           end_date
    AUDIT_BREAKDOWN_AREA = (audit_column_counter - ORDERS_COLUMN_WIDTH,
                            audit_column_counter)

    audit_column_counter += ORDERS_COLUMN_WIDTH + 1

    for date in sorted(data_files):
        sheet_name = 'Orders {}-{}-{}'.format(date.month, date.day, date.year)
        ws = workbook.add_sheet(sheet_name)

        subtotal_by_date = 0.0
        tax_by_date = 0.0

        frequency_by_date = {}
        items_total = 0

        # Each specific DATE SHEET is generated here and populated.
        #
        # Each DATE SHEET has a similar structure to the AUDIT SHEET.
        # only deals in more specific information by parsing every
        # single order made and displaying their times, etc.
        #
        # DATE SHEETs share in the following areas. But their scope
        # is limited only to that specific DATE. See AUDIT SHEET area
        # for more information on these areas.
        #
        #     - Total Area
        #     - Breakdown Area
        #     - Display Area: Specifically displays each order made in DATE.
        #

        column_counter = ORDERS_COLUMN_WIDTH

        # Generate date wide total area.
        total_area = (column_counter - ORDERS_COLUMN_WIDTH, column_counter)
        total_area_title = 'TOTALS for ' + sheet_name
        order_total_row = _add_order_header(ws, 0, total_area[0],
                                            total_area[1], total_area_title)
        column_counter += ORDERS_COLUMN_WIDTH + 1

        # Save date wide breakdown area.
        breakdown_title = 'Menu Item Breakdown for ' + sheet_name
        breakdown_area = (column_counter - ORDERS_COLUMN_WIDTH, column_counter)
        column_counter += ORDERS_COLUMN_WIDTH + 1

        for name, order in data_files[date]:
            start_column = column_counter - ORDERS_COLUMN_WIDTH

            # Add header to the selected area. This displays order info for
            #  order that will be populated below.
            row = _add_order_header(ws, 0, start_column, column_counter, name)

            for menu_item in order:

                # Update data for breakdown
                items_total += 1.0
                name = menu_item.get_name()
                if name in frequency_by_date:
                    frequency_by_date[name] += 1.0
                else:
                    frequency_by_date[name] = 1.0

                # Update worksheet for menu item.
                row = _add_menu_item(ws, row, start_column, column_counter,
                                     menu_item)

                order_total_row = _add_menu_item(ws, order_total_row,
                                                 total_area[0], total_area[1],
                                                 menu_item)
                #===============================================================
                # AUDIT UPDATE: Audit wide total display area is updated here
                #===============================================================
                audit_total_row = _add_menu_item(audit_sheet, audit_total_row,
                                                 AUDIT_TOTAL_AREA[0],
                                                 AUDIT_TOTAL_AREA[1],
                                                 menu_item)
                #===============================================================
                #===============================================================

            # Update worksheet for item totals
            subtotal, tax, total = _finalize_order(ws, row, start_column,
                                                   column_counter, order)

            subtotal_by_date += subtotal
            tax_by_date += tax

            column_counter += ORDERS_COLUMN_WIDTH + 1

        # Generate date breakdown area and finalize date total area.
        _generate_breakdown_total_area(ws, 0, breakdown_area[0],
                                       breakdown_area[1], frequency_by_date,
                                       items_total, title=breakdown_title)

        _finalize_order(ws, order_total_row, total_area[0], total_area[1],
                        [], subtotal=subtotal_by_date,
                        tax=tax_by_date)

        #========================================================
        # AUDIT UPDATE: Audit wide variables updated in this block
        #========================================================
        subtotal_by_audit += subtotal_by_date
        tax_by_audit += tax_by_date

        for key in frequency_by_date:

            if key in frequency_by_audit:
                frequency_by_audit[key] += frequency_by_date[key]
            else:
                frequency_by_audit[key] = frequency_by_date[key]

        total_items_by_audit += items_total
        #=========================================================
        #=========================================================

    # Generate audit wide breakdown area and finalize audit wide total area.
    _generate_breakdown_total_area(audit_sheet, 0, AUDIT_BREAKDOWN_AREA[0],
                                   AUDIT_BREAKDOWN_AREA[1], frequency_by_audit,
                                   total_items_by_audit, title=audit_breakdown_title)

    print subtotal_by_audit
    print tax_by_audit
    _finalize_order(audit_sheet, audit_total_row, AUDIT_TOTAL_AREA[0],
                    AUDIT_TOTAL_AREA[1], [], subtotal=subtotal_by_audit,
                    tax=tax_by_audit)

    return workbook


def _generate_breakdown_total_area(worksheet, start_row, start_column,
                                   end_column, order_breakdown, total_items,
                                   title='Breakdown Area'):
    """Generates the MenuItem breakdown area that is to be displayed. This
    area will give a breakdown of every menu item that is contained in the
    data passed in. Displaying the total number made, and the number as
    a percentage.

    @param worksheet: xlwt.Worksheet that is to have the breakdown data
    generated on. The data will be generated inbetween the the given columns
    starting on the given row.

    @param start_row: int representing the row from which the breakdown area
    should be generated. This row will be consumed.

    @param start_column: int representing the left most column that is to
    be consumed by the breakdown area.

    @param end_column: int representing the right most column that is to
    be consumed by the breakdown area.

    @param order_breakdown: dict of str representing a Menuitem object that
    is mapped to a key of float values representing the number times that
    MenuItem was ordered.

    @param total_items: float number representing the total number of MenuItems
    contained in the order_breakdown dict.

    @keyword title: str representing the title that should be given to this
    breakdown area. By default is 'Breakdown Area'

    @return: int representing the row that it is safe to add data to after this
    breakdown area.
    """
    row = _add_order_header(worksheet, start_row, start_column, end_column,
                            title)
    running_percentage = 0.0
    running_total = 0.0

    percentage_column = end_column - 1

    for item_name in order_breakdown:

        number_of_orders = order_breakdown[item_name]
        number_as_percentage = round(number_of_orders / total_items, 4)

        worksheet.write(row, start_column, item_name)
        worksheet.write(row, percentage_column, number_as_percentage)
        worksheet.write(row, end_column,  number_of_orders)

        row += 2
        running_percentage += number_as_percentage
        running_total += number_of_orders

    style = xlwt.easyxf('font: bold on;')

    worksheet.write(row, start_column, 'totals', style=style)
    worksheet.write(row, percentage_column, running_percentage, style=style)
    worksheet.write(row, end_column, running_total, style=style)

    return row + 1


def _add_order_header(worksheet, start_row, start_column, end_column,
                      order_name):
    """Adds the header associated with the parsed given order name as
    the header under which all associated data should be displayed.

    @param worksheet: xlwt.Worksheet that is to have the associated
    header displayed on the given start row + 1, between the given
    columns that is associated with the given order name.

    @warning: The displayed header will spawn two rows, so the given
    row and the row beneath it will be consumed and merged to display
    the full header. As such this method will return an int representing
    the associated row that is safe to add to after the header has been
    added.

    @param start_row: int representing the row to have the header added
    to it. This row and the subsequent row underneath this will be consumed
    within the start and end columns. This method will return an int
    that represents which row is safe to add to after the header has been
    added.

    @param start_column: int representing the left most column that this
    header should occupy.

    @param end_column: int representing the right most column that this
    header should occupy

    @param order_name: standardized file name for the order.

    @return: int representing the row that it is safe to begin inserting
    new data at, which is underneath this header.
    """
    time, name, order_type = parse_standardized_file_name(order_name)

    order_label = name
    if len(time) > 0:
        order_label += ' at ' + time

    worksheet.write_merge(start_row, start_row + 1, start_column,
                          end_column - 1, order_label, style=MERGED_STYLE)
    worksheet.write_merge(start_row, start_row + 1, end_column,
                          end_column, 'TOTAL', style=MERGED_STYLE)

    return start_row + 2


def _add_menu_item(worksheet, start_row, start_column, end_column, menu_item):
    """Adds the given menu item, to the given worksheet with the given
    conditions. Expecting at least 3 columns that are accessible and
    to be filled with data regarding the menu item and its associated
    options, notes, and stars, etc.

    @param worksheet: xlwt.Worksheet that is to have the information
    contained in this menu item added to it at the specified row, and
    between the specified columns.

    @param start_row: int representing the row that this menu items
    associated information should be added at.

    @param start_column: int representing the starting column that
    will be the left most boundary for the data to be displayed.

    @param end_column: int representing the ending column that will
    be the right most boundary for the data to be displayed.

    @warning: end_column - start_column >= 3 for this function to
    operate appropriately.

    @param menu_item: MenuItem object that is to have its data
    displayed in the associated areas.

    @return: int representing the next safe row to add data to
    after this MenuItem has had its data added.
    """
    worksheet.write(start_row, start_column, menu_item.get_name())
    worksheet.write(start_row, end_column, str(menu_item.get_price()))

    row_counter = start_row + 1
    column = start_column + 1

    for option in menu_item.options:
        name = option.get_option_relation() + " " + option.get_name()
        worksheet.write(row_counter, column, name)
        worksheet.write(row_counter, end_column, option.get_price())
        row_counter += 1

    notes = menu_item.notes
    stars = str(menu_item.stars)

    return 1 + row_counter


def _finalize_order(worksheet, start_row, start_column, end_column, order,
                    subtotal=None, tax=None):
    """Finalizes the current selected order displayed between the columns
    by adding the given order total information to the given worksheet. This
    is expected to occur at the end of the order when no more items need to
    be added to the bottom of the row.

    @warning: This function expects to be the final function called and as
    such it doesn't return an updated row. Instead it returns data regarding
    the totals associated with the order.

    @param worksheet: xlwt.Worksheet object that is to have the associated
    order totals data written to it at the specified row, using the specified
    start column to store a descriptor and the end column to store the totals

    @param start_row: int representing the row which should have the order
    information added to it from this point on.

    @param start_column: int representing the first column that should
    hold the str descriptors for the totals that will be displayed on the
    furthest columns

    @param end_column: int representing the furthest column that will display
    the totals associated with their descriptors.

    @param order: list of MenuItem objects that is to be parsed and have its
    associated subtotal, tax, and total displayed respectively.

    @return: tuple of type (int, int, int) that represents the associated
    orders (subtotal, tax, total) respectively. This function is expected
    to be called as the final row of an order, therefore doesn't return
    an updated row.
    """
    if not subtotal:
        subtotal = CheckOperations.get_order_subtotal(order)
    if not tax:
        tax = CheckOperations.get_total_tax(subtotal)

    total = subtotal + tax

    style = xlwt.easyxf('font: bold on;')

    updated_row = start_row
    for total_name, total in zip(['subtotal', 'tax', 'total'],
                                 (subtotal, tax, total)):
        worksheet.write(updated_row, start_column, total_name, style=style)
        worksheet.write(updated_row, end_column, total, style=style)

        updated_row += 1

    return subtotal, tax, total


def _get_data(start_date, end_date):
    """Gets the data the data currently stored in
    the orders log area between the given start
    dates inclusive.

    @param start_date: datetime.date object that
    represents hte stored date that will be the
    beginning point.

    @param end_date: datetime.date object that
    represents the stored date that will be the
    ending point.

    @return: dict of str keys that represent the
    filename associated with the data, and are mapped
    to values which are lists of MenuItems that represent
    the order specified by the key.
    """
    data = {}

    curr_date = start_date
    while curr_date <= end_date:
        data_path = os.path.join(ORDERS_DIRECTORY, str(curr_date.year),
                                 str(curr_date.month), str(curr_date.day))
        if os.path.exists(data_path):
            data_files = []

            for dirpath, dirnames, filenames in os.walk(data_path):

                for filename in filenames:

                    data_file = open(dirpath + '/' + filename, 'r')
                    order_data = jsonpickle.decode(data_file.read())
                    data_files.append((filename, order_data))


            data[curr_date] = sorted(data_files)

        curr_date += datetime.timedelta(days=1)

    return data


if __name__ == '__main__':

    start_date = datetime.date(2013, 9, 1)
    end_date = datetime.date(2013, 12, 30)

    data_files = _get_data(start_date, end_date)

    wkbk = audit_data(start_date, end_date)
    wkbk.save(REQUEST_DIRECTORY + '/' + 'test.xls')
