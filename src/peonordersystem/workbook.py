"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
import random
import jsonpickle
import xlsxwriter
from copy import copy
from collections import deque
from datetime import datetime, date, time, timedelta

from src.peonordersystem.worksheet import DataWorksheet, Worksheet, DisplayWorksheet
from src.peonordersystem.SpreadsheetAreas import (GeneralDatesheetOrderArea,
                                                  GeneralDatesheetFrequencyArea)
from src.peonordersystem.PackagedData import PackagedDateData, PackagedItemData, \
    PackagedOrderData

from src.peonordersystem.Settings import SQLITE_DATE_TIME_FORMAT_STR
from src.peonordersystem.MenuItem import MenuItem, OptionItem

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
    """

    """
    def __init__(self, file_name):
        """

        @return:
        """
        super(Workbook, self).__init__(file_name)

        self.default_init_data = {
            'index': 0,
            'str_table': self.str_table,
            'worksheet_meta': self.worksheet_meta,
            'optimization': self.optimization,
            'tmpdir': self.tmpdir,
            'date_1904': self.date_1904,
            'strings_to_numbers': self.strings_to_numbers,
            'strings_to_formulas': self.strings_to_formulas,
            'strings_to_urls': self.strings_to_urls,
            'default_date_format': self.default_date_format,
            'default_url_format': self.default_url_format,
        }

        self.format_dict = self._generate_format_data()

        self.data_worksheet = self._add_data_worksheet()

    def _generate_format_data(self):
        """

        @return:
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

    def _add_data_worksheet(self):
        """

        @return:
        """
        init_data = copy(self.default_init_data)
        init_data['name'] = self._check_sheetname('DataWorksheet', False)

        worksheet = DataWorksheet(self.format_dict)
        worksheet._initialize(init_data)

        self.worksheets_objs.append(worksheet)
        self.sheetnames.append(init_data['name'])

        return worksheet

    def add_general_date_worksheet(self, name, d, c):
        """

        @param name:
        @return:
        """
        init_data = copy(self.default_init_data)
        init_data['name'] = self._check_sheetname('test', False)

        worksheet = DisplayWorksheet(self.format_dict)
        worksheet._initialize(init_data)

        self.worksheets_objs.append(worksheet)
        self.sheetnames.append(init_data['name'])

        g = GeneralDatesheetFrequencyArea(datetime.now(), c, self.format_dict)
        worksheet.add_area(g)

        for packaged_data in d:
            g = GeneralDatesheetOrderArea(packaged_data, self.format_dict)
            worksheet.add_area(g)

        return worksheet



if __name__ == '__main__':
    letters = 'abcdefghijklmnopqrstuvwxyz'
    workbook = Workbook('abcdefg.xlsx')

    def _generate_random_name(num):
        while True:
            yield ''.join(random.sample(list(letters), num))

    def _generate_menu_items():
        rand_name = _generate_random_name(10)
        other_rand_name = _generate_random_name(5)

        while True:
            name = rand_name.next()
            price = random.randint(1, 100)

            item = MenuItem(name, price)
            item.notes = rand_name.next()

            for x in xrange(10):
                name = other_rand_name.next()
                category = 'Test'
                price = random.randint(1, 100)

                option = OptionItem(name, category, price)
                item.options.append(option)

            yield item

    def _generate_random_datetime():
        while True:
            yield datetime.now() + timedelta(minutes=random.randint(-1000, 1000))

    def _generate_packaged_data():
        rand_date = _generate_random_datetime()
        rand_name = _generate_random_name(7)
        rand_items = _generate_menu_items()

        while True:

            data = (
                random.randint(1, 100),
                rand_date.next().strftime(SQLITE_DATE_TIME_FORMAT_STR),
                rand_name.next(),
                1000.0,
                9.0,
                910.0,
                False,
                jsonpickle.encode([]),
                jsonpickle.encode([]),
                1,
                0,
                jsonpickle.encode([rand_items.next() for x in range(12)])
            )

            yield PackagedOrderData(data)

    rand_data = _generate_packaged_data()

    d = [rand_data.next() for x in range(2)]

    from collections import Counter

    c = Counter()
    for letter in letters:
        c[letter] = random.randint(1, 100)


    workbook.add_general_date_worksheet('test', d, c)
    workbook.close()