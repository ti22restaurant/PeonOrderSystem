"""Defines workbook classes that are
used to generate workbooks that present
data in an easy to digest format for users.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from collections import Counter

import xlsxwriter


from .worksheet import Worksheet
from .datasheet.DataWorksheet import DataWorksheet
from .formats.FormatData import StandardFormatData
from .generalsheet.areas.ChartArea import DataChartArea


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

    def add_chart(self, chart_data, name=''):
        """Adds a chart to the workbook

        @return: DataChartArea object
        representing the chart.
        """
        chart = self._workbook.add_chart(chart_data)
        return DataChartArea(chart, name)

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

    datasheet = workbook.datasheet

    from peonordersystem.audit.datasheet.areas.StandardAreas import (
        OrdersTimeDataArea, ItemsTimeDataArea, TotalsTimeDataArea)

    print 'Generating OrdersArea...',
    t = datetime.now()

    area1 = OrdersTimeDataArea(datasheet.time_keys)
    area2 = ItemsTimeDataArea(datasheet.time_keys)
    area3 = TotalsTimeDataArea(datasheet.time_keys)

    print datetime.now() - t

    print 'Populating OrdersArea...',

    t = datetime.now()
    for each in data:
        area1.insert(each)
        area2.insert(each)
        area3.insert(each)

    datasheet.add_area(area1)
    datasheet.add_area(area2)

    datasheet.add_area(area3)
    print datetime.now() - t

    chart_sheet = workbook.add_worksheet('chart_sheet')

    chart = workbook.add_chart({'type': 'line'}, name='Order Data')
    chart.add_keys_and_data(datasheet.time_keys, area1)
    chart_sheet.add_area(chart)

    chart = workbook.add_chart({'type': 'line'}, name='Item Data')
    chart.add_keys_and_data(datasheet.time_keys, area2)
    chart_sheet.add_area(chart)

    chart = workbook.add_chart({'type': 'line'}, name='Totals Data')
    chart.add_keys_and_data(datasheet.time_keys, area3)
    chart_sheet.add_area(chart)

    print 'Closing workbook...',
    t = datetime.now()

    workbook.close()
    print datetime.now() - t
