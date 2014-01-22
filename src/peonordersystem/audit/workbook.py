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
from src.peonordersystem.audit.FormatData import StandardFormatData


class Workbook(object):
    """Workbook class defines the basic workbook
    that represents the xlsx file to be displayed.
    """
    def __init__(self, file_name):
        """Initializes the workbook with the given
        name.

        @param file_name: str representing the file
        name that the workbook should be saved as.
        """
        self._workbook = xlsxwriter.Workbook(file_name)
        self.format_data = self._generate_format_data()
        self.datasheet = self._add_data_worksheet()

    def _generate_format_data(self):
        """Generates standard format
        data.

        @return: FormatData object that
        represents the formats associated
        with this workbook.
        """
        format = StandardFormatData()
        format.connect(self)
        return format

    def _add_data_worksheet(self):
        """Adds a hidden data worksheet to
        the current workbook.

        @return: DataWorksheet object that
        represents the data worksheet.
        """
        ws = self.add_worksheet()
        return DataWorksheet(ws, self.format_data)

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
        return Worksheet(ws, self.format_data)

    def add_chart(self, *args, **kwargs):
        """Adds a chart to the workbook

        @param args: represents potential arguments
        to be associated with the chart.

        @param kwargs: represents potential keyword
        arguments to be associated with the chart.

        @return: xlsxwriter.Workbook
        """
        return self._workbook.add_chart(*args)

    def _add_format(self, format_data):
        """Adds the given format information to
        the workbook.

        @param format_data: dict representing
        the format data to be associated with
        the format.

        @return: xlsxwriter.Format that represents
        the associated format.
        """
        return self._workbook.add_format(format_data)

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

    from src.peonordersystem.audit.DatasheetAreas import (OrdersTimeKeyToValueDataArea,
                                                          ItemsTimeKeyToValueDataArea,
                                                          TotalsTimeKeyToValueDataArea)

    print 'Generating OrdersArea...',
    t = datetime.now()

    area1 = OrdersTimeKeyToValueDataArea(datesheet._time_keys_area.data)
    area2 = ItemsTimeKeyToValueDataArea(datesheet._time_keys_area.data)
    area3 = TotalsTimeKeyToValueDataArea(datesheet._time_keys_area.data)

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
