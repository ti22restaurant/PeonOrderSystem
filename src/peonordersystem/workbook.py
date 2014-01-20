"""Defines workbook classes that are
used to generate workbooks that present
data in an easy to digest format for users.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

import xlsxwriter
from collections import Counter

from src.peonordersystem.worksheet import Worksheet

from src.peonordersystem.DatesheetAreas import (OrderArea, FrequencyArea,
                                                       NotificationArea, OverviewArea)

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


class Workbook(xlsxwriter.Workbook):
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
        super(Workbook, self).__init__(file_name)
        self.format_dict = self._generate_format_data()

    def add_worksheet(self, *args):
        """Adds a new worksheet to the workbook.

        @param args: represents potential arguments
        to be associated with the worksheet

        @return: Worksheet class that represents
        the worksheet. This wrapper is expected
        to be interacted with by adding
        SpreadsheetAreas directly to it.
        """
        ws = super(Workbook, self).add_worksheet(*args)
        return Worksheet(ws)

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


class AuditWorkbook(Workbook):
    """AuditWorkbook class defines the standard
    audit style workbook. This includes three
    types of sheets:

        1. Audit Overview Sheet :   which represents the overview
                                    of the data covered in the audit.

        2. Date Overview Sheet  :   which represents the overview
                                    of the data covered on a specific
                                    date.

        3. Date Sheet          :    which represents the order data
                                    for a specific date.

    Each sheet is divided into multiple areas which are generated
    and added in their respective methods.
    """

    def add_date_sheet(self, date_data, packaged_data):
        """Adds a new date sheet to the workbook with the
        given date and populates the sheet with the given
        data.

        @param date_data: datetime.date that represents the
        date associated with this data.

        @param packaged_data: PackagedOrderData that represents
        the dat associated with this sheet.

        @return: None
        """
        name = str(date_data)
        worksheet = self.add_worksheet(name)
        self._add_date_sheet_areas(date_data, worksheet, packaged_data)

    def _add_date_sheet_areas(self, date_data, worksheet, packaged_data):
        """Creates and adds the date sheet areas to the given worksheet.

        @param date_data: datetime.date that represents the date associated
        with the packaged data.

        @param worksheet: Worksheet object that represents the worksheet
        that the areas that contain the data will be added to.

        @param packaged_data: PackagedOrderData that represents
        the data to be added to the areas.

        @return:
        """
        overview_area = self._create_date_sheet_overview_area(date_data, worksheet)
        freq_area = self._create_date_sheet_frequency_area(date_data, worksheet)
        notif_area = self._create_date_sheet_notification_area(date_data, worksheet)

        item_freq = Counter()
        notif_data = []

        for packaged_order in self._generate_date_sheet_order_area(packaged_data,
                                                                   worksheet):
            item_freq.update(packaged_order.item_frequency)
            notif_data += packaged_order.notification_data
            overview_area.add(packaged_order)

        freq_area.add(item_freq)
        notif_area.add(notif_data)

    def _create_date_sheet_overview_area(self, date_data, worksheet):
        """Creates the OverviewArea in the given worksheet.

        @param date_data: datetime.date that represents the date that
        the OverviewArea will be associated with.

        @param worksheet: Worksheet object that the OverviewArea will
        be added to.

        @return: OverviewArea object that has been added to the
        given worksheet.
        """
        overview_area = OverviewArea(date_data, self.format_dict)
        worksheet.add_area(overview_area)
        return overview_area

    def _create_date_sheet_frequency_area(self, date_data, worksheet):
        """Creates the FrequencyArea in the given worksheet.

        @param date_data: datetime.date that represents the date
        associated with the data.

        @param worksheet: Worksheet object that the area is to be
        added to.

        @return: FrequencyArea that has been added to the given
        worksheet.
        """
        freq_area = FrequencyArea(date_data, Counter(), self.format_dict)
        worksheet.add_area(freq_area)
        return freq_area

    def _create_date_sheet_notification_area(self, date_data, worksheet):
        """Creates the NotificationArea in the given worksheet.

        @param date_data: datetime.date that represents the date
        associated with the data.

        @param worksheet: Worksheet object that the area is to be
        added to.

        @return:NotificationArea that has been added to the given
        worksheet.
        """
        notif_area = NotificationArea(date_data, [], self.format_dict)
        worksheet.add_area(notif_area)
        return notif_area

    def _generate_date_sheet_order_area(self, packaged_data, worksheet):
        """Generates the order areas for the date sheet.

        @param packaged_data: PackagedOrderData that represents data to
        be added to the order areas.

        @param worksheet: Worksheet that the areas should be added to.

        @return: Generator object that yields packaged order data.
        @yield: PackagedOrderData that has had an order area created
        for it.
        """
        for packaged_order in packaged_data:
            order_area = OrderArea(packaged_order, self.format_dict)
            worksheet.add_area(order_area)
            yield packaged_order

    def add_overview_date_sheet(self):
        """Adds a new date overview sheet to the workbook,
        and populates the sheet with the given data.

        @return:
        """
        pass

    def add_overview_audit_sheet(self):
        """Adds a new audit overview sheet to the workbook,
        and populates the sheet with the given data.

        @return:
        """
        pass




if __name__ == "__main__":
    import string
    import jsonpickle
    from random import randint
    from datetime import datetime, timedelta, time

    from src.peonordersystem.CheckOperations import (get_total, get_order_subtotal,
                                                     get_total_tax)

    from src.peonordersystem.PackagedData import PackagedOrderData
    from src.peonordersystem.Settings import SQLITE_DATE_TIME_FORMAT_STR

    from test.TestingFunctions import (generate_random_menu_items,
                                       generate_random_times,
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

    data = [rand_data.next() for x in range(338)]


    workbook = AuditWorkbook('test_audit.xlsx')
    t = datetime.now()

    workbook.add_date_sheet(datetime.now().date(), data)
    print datetime.now() - t
    workbook.close()
