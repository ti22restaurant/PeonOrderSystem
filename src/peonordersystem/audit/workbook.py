"""Defines workbook classes that are
used to generate workbooks that present
data in an easy to digest format for users.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from collections import Counter

import xlsxwriter

from src.peonordersystem.audit.worksheet import Worksheet, DataWorksheet


#====================================================================================
# This block represents formatting constants used in the workbook.
#====================================================================================
TITLE_FORMAT_LEFT = {'bold': True,
                     'font_size': 10,
                     'left': 1,
                     'top': 1,
                     'bottom': 1,
                     'valign': 'vcenter',
                     'align': 'center'}

TITLE_FORMAT_RIGHT = {'bold': True,
                      'font_size': 10,
                      'right': 1,
                      'top': 1,
                      'bottom': 1,
                      'valign': 'vcenter',
                      'align': 'center'}

TITLE_FORMAT_CENTER = {'bold': True,
                       'font_size': 10,
                       'top': 1,
                       'bottom': 1,
                       'valign': 'vcenter',
                       'align': 'center'}

SUBTITLE_FORMAT_LEFT = {'bold': True,
                        'font_size': 8,
                        'left': 1,
                        'top': 1,
                        'bottom': 1,
                        'valign': 'vcenter',
                        'align': 'center',
                        'font_color': 'gray'}

SUBTITLE_FORMAT_RIGHT = {'bold': True,
                         'font_size': 8,
                         'right': 1,
                         'top': 1,
                         'bottom': 1,
                         'valign': 'vcenter',
                         'align': 'center',
                         'font_color': 'gray'}

SUBTITLE_FORMAT_CENTER = {'bold': True,
                          'font_size': 8,
                          'top': 1,
                          'bottom': 1,
                          'valign': 'vcenter',
                          'align': 'center',
                          'font_color': 'gray'}

TOTAL_DATA_FORMAT = {'num_format': '$#,##0.00;[Red]-$#,##0.00',
                     'valign': 'vcenter',
                     'align': 'center',
                     'right': 1,
                     'bold': True}

MAIN_TITLE_DATA_FORMAT = {'bold': True,
                          'valign': 'vcenter',
                          'align': 'center',
                          'border': 1,
                          'font_size': 15}

TITLE_DATA_FORMAT = {'bold': True,
                     'valign': 'vcenter',
                     'align': 'center',
                     'top': 1,
                     'bottom': 1,
                     'font_size': 11}

SUBTITLE_DATA_FORMAT = {'font_color': 'gray',
                        'valign': 'vcenter',
                        'align': 'center',
                        'top': 1,
                        'bottom': 1,
                        'left': 1,
                        'font_size': 8}

SUBTOTAL_DATA_FORMAT = {'font_color': 'gray',
                        'font_size': 8,
                        'align': 'center',
                        'top': 1,
                        'bottom': 1,
                        'right': 1,
                        'num_format': '$#,##0.00'}

LEFT_COL_FORMAT = {'left': 1,
                   'align': 'center'}

RIGHT_COL_FORMAT = {'right': 1,
                    'align': 'center'}

DATE_FORMAT = {'num_format': 'd mmmm yyyy',
               'valign': 'vcenter',
               'align': 'center'}

DATE_TIME_FORMAT = {'num_format': 'dd/mm/yy hh:mm:ss',
                    'valign': 'vcenter',
                    'align': 'center'}

TIME_FORMAT = {'num_format': 'hh:mm:ss',
               'valign': 'vcenter',
               'align': 'center'}

ITEM_DATA_FORMAT_LEFT = {'left': 1,
                         'bold': True,
                         'font_size': 12}

ITEM_DATA_FORMAT_RIGHT = {'right': 1,
                          'font_size': 10}

SUBITEM_DATA_FORMAT_LEFT = {'left': 1,
                            'font_size': 8,
                            'font_color': 'gray',
                            'valign': 'vjustify',
                            'align': 'center'}

SUBITEM_DATA_FORMAT_CENTER = {'font_color': 'gray',
                              'font_size': 8,
                              'valign': 'vjustify',
                              'align': 'center'}

SUBITEM_DATA_FORMAT_RIGHT = {'right': 1,
                             'font_size': 8,
                             'font_color': 'gray',
                             'valign': 'vjustify',
                             'align': 'center'}

SUBITEM_DATA_TOTAL_FORMAT = {'right': 1,
                             'font_size': 8,
                             'font_color': 'gray',
                             'num_format': '$#,##0.00',
                             'valign': 'vjustify',
                             'align': 'center'}


class Workbook(object):
    """Workbook class defines the basic workbook
    that represents the xlsx file to be displayed.

    @var format_dict: dict of str keys mapped to
    values of xlsxwriter.Format that represent
    the formats available to this workbook.
    """
    def __init__(self, file_name):
        """Initializes the workbook with the given
        name.

        @param file_name: str representing the file
        name that the workbook should be saved as.
        """
        self._workbook = xlsxwriter.Workbook(file_name)
        self.format_dict = self._generate_format_data()
        self.datasheet = self._add_data_worksheet()

    def _add_data_worksheet(self):
        """Adds a hidden data worksheet to
        the current workbook.

        @return: DataWorksheet object that
        represents the data worksheet.
        """
        ws = self.add_worksheet()
        return DataWorksheet(ws, self.format_dict)

    def add_worksheet(self, *args, **kwargs):
        """Adds a new worksheet to the workbook.

        @param args: represents potential arguments
        to be associated with the worksheet

        @param kwargs: represents potential keyword
        arguments to be associated with the worksheet.

        @return: Worksheet class that represents
        the worksheet. This wrapper is expected
        to be interacted with by adding
        SpreadsheetAreas directly to it.
        """
        ws = self._workbook.add_worksheet(*args, **kwargs)
        return Worksheet(ws)

    def add_chart(self, *args, **kwargs):
        """Adds a chart to the workbook

        @param args: represents potential arguments
        to be associated with the chart.

        @param kwargs: represents potential keyword
        arguments to be associated with the chart.

        @return: xlsxwriter.Workbook
        """
        return self._workbook.add_chart(*args)

    def add_format(self, format_data):
        """Adds the given format information to
        the workbook.

        @param format_data: dict representing
        the format data to be associated with
        the format.

        @return: xlsxwriter.Format that represents
        the associated format.
        """
        return self._workbook.add_format(format_data)

    def _generate_format_data(self):
        """Generates the format data used
        for formating worksheet cells.

        @return: dict of str keys mapped to
        xlsxwriter.Format objects that represent
        the associated display formats.
        """
        format_dict = {}

        format_dict['left_column'] = self.add_format(LEFT_COL_FORMAT)
        format_dict['right_column'] = self.add_format(RIGHT_COL_FORMAT)

        format_dict['time_format'] = self.add_format(TIME_FORMAT)
        format_dict['date_format'] = self.add_format(DATE_FORMAT)
        format_dict['datetime_format'] = self.add_format(DATE_TIME_FORMAT)

        format_dict['title_format_left'] = self.add_format(TITLE_FORMAT_LEFT)
        format_dict['title_format_center'] = self.add_format(TITLE_FORMAT_CENTER)
        format_dict['title_format_right'] = self.add_format(TITLE_FORMAT_RIGHT)

        format_dict['subtitle_format_left'] = self.add_format(SUBTITLE_FORMAT_LEFT)
        format_dict['subtitle_format_center'] = self.add_format(SUBTITLE_FORMAT_CENTER)
        format_dict['subtitle_format_right'] = self.add_format(SUBTITLE_FORMAT_RIGHT)

        format_dict['main_title_data_format'] = self.add_format(MAIN_TITLE_DATA_FORMAT)
        format_dict['title_data_format'] = self.add_format(TITLE_DATA_FORMAT)
        format_dict['subtitle_data_format'] = self.add_format(SUBTITLE_DATA_FORMAT)
        format_dict['total_data_format'] = self.add_format(TOTAL_DATA_FORMAT)
        format_dict['subtotal_data_format'] = self.add_format(SUBTOTAL_DATA_FORMAT)

        format_dict['item_data_format_left'] = self.add_format(ITEM_DATA_FORMAT_LEFT)
        format_dict['item_data_format_right'] = self.add_format(ITEM_DATA_FORMAT_RIGHT)

        format_dict['subitem_data_format_left'] = self.add_format(SUBITEM_DATA_FORMAT_LEFT)
        format_dict['subitem_data_format_center'] = self.add_format(SUBITEM_DATA_FORMAT_CENTER)
        format_dict['subitem_data_format_right'] = self.add_format(SUBITEM_DATA_FORMAT_RIGHT)

        format_dict['subitem_data_total_format'] = self.add_format(SUBITEM_DATA_TOTAL_FORMAT)

        return format_dict

    def close(self):
        """Closes the workbook and saves
        it to the given name.

        @return: None
        """
        self._workbook.close()


if __name__ == "__main__":
    import string
    import jsonpickle
    from random import randint
    from datetime import datetime, timedelta, time

    from src.peonordersystem.audit.AuditWorkbook import AuditWorkbook

    from src.peonordersystem.CheckOperations import (get_total, get_order_subtotal,
                                                     get_total_tax)

    from src.peonordersystem.PackagedData import PackagedOrderData
    from src.peonordersystem.Settings import SQLITE_DATE_TIME_FORMAT_STR

    from test.TestingFunctions import (generate_random_menu_items,
                                       generate_random_names)

    def generate_random_packaged_data():
        rand_names = generate_random_names(from_chars=string.ascii_letters * 100)
        rand_items = generate_random_menu_items()
        curr_date = datetime.combine(datetime.today().date(), time.min)

        while True:
            notification_data = []
            item_frequency = Counter()
            items = []

            for x in xrange(10):
                item = rand_items.next()
                items.append(item)

                if item.is_notification():
                    notification_data.append(item)

                item_frequency[item.get_name()] += 1

            total = get_total(items)
            subtotal = get_order_subtotal(items)
            tax = get_total_tax(subtotal)

            standard_type = randint(0, 1)
            togo_type = 1 - standard_type

            curr_date += timedelta(minutes=1)
            data = (
                randint(1, 100),
                curr_date.strftime(SQLITE_DATE_TIME_FORMAT_STR),
                rand_names.next(),
                subtotal,
                tax,
                total,
                len(notification_data) > 0,
                jsonpickle.encode(notification_data),
                jsonpickle.encode(item_frequency),
                standard_type,
                togo_type,
                jsonpickle.encode(items)
            )

            yield PackagedOrderData(data)

    d = {}


    rand_data = generate_random_packaged_data()

    data = [rand_data.next() for x in range(1439)]


    workbook = AuditWorkbook('test_audit.xlsx')

    print 'Adding date sheet...',
    t = datetime.now()

    workbook.add_date_sheet(datetime.now().date(), data)
    print datetime.now() - t

    datesheet = workbook.datasheet

    from src.peonordersystem.audit.ValueAreas import OrdersTimeArea, \
        ItemsTimeArea, TotalsTimeArea

    print 'Generating OrdersArea...',
    t = datetime.now()

    area1 = OrdersTimeArea(datesheet._time_keys_area.data)
    area2 = ItemsTimeArea(datesheet._time_keys_area.data)
    area3 = TotalsTimeArea(datesheet._time_keys_area.data)

    print datetime.now() - t

    print 'Populating OrdersArea...',

    t = datetime.now()
    for each in data:
        area1.insert(each)
        area2.insert(each)
        area3.insert(each)

    datesheet.add_area(area1)
    datesheet.add_area(area2)

    datesheet.add_area(area3)
    print datetime.now() - t

    print 'Closing workbook...',
    t = datetime.now()

    workbook.close()
    print datetime.now() - t
