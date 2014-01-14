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
from src.peonordersystem.SpreadsheetAreas import GeneralDateSheetOrderArea
from src.peonordersystem.PackagedData import PackagedDateData, PackagedItemData, \
    PackagedOrderData

from src.peonordersystem.Settings import SQLITE_DATE_TIME_FORMAT_STR
from src.peonordersystem.MenuItem import MenuItem

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
                        'indent': 1,
                        'font_color': 'gray'}

SUBTITLE_FORMAT_RIGHT = {'bold': True,
                         'font_size': 8,
                         'right': 1,
                         'top': 1,
                         'bottom': 1,
                         'valign': 'vcenter',
                         'indent': 1,
                         'font_color': 'gray'}

SUBTITLE_FORMAT_CENTER = {'bold': True,
                          'font_size': 8,
                          'top': 1,
                          'bottom': 1,
                          'valign': 'vcenter',
                          'indent': 1,
                          'font_color': 'gray'}

TOTAL_DATA_FORMAT = {'num_format': '$#,##0.00;[Red]-$#,##0.00',
                     'valign': 'vcenter',
                     'right': 1}

MAIN_TITLE_DATA_FORMAT = {'bold': True,
                          'valign': 'vcenter',
                          'align': 'center',
                          'border': 1,
                          'font_size': 11}

TITLE_DATA_FORMAT = {'bold': True,
                     'valign': 'vcenter',
                     'align': 'center',
                     'top': 1,
                     'bottom': 1,
                     'font_size': 11}

SUBTITLE_DATA_FORMAT = {'font_color': 'gray',
                        'valign': 'vcenter',
                        'indent': 1,
                        'top': 1,
                        'bottom': 1,
                        'left': 1,
                        'font_size': 8}

SUBTOTAL_DATA_FORMAT = {'font_color': 'gray',
                        'font_size': 8,
                        'align': 'right',
                        'top': 1,
                        'bottom': 1,
                        'right': 1,
                        'num_format': '$#,##0.00'}

LEFT_COL_FORMAT = {'left': 2,
                   'align': 'left'}

RIGHT_COL_FORMAT = {'right': 2,
                    'align': 'right'}

DATE_FORMAT = {'num_format': 'd mmmm yyyy',
               'valign': 'vcenter',
               'align': 'center'}

DATE_TIME_FORMAT = {'num_format': 'dd/mm/yy hh:mm:ss',
                    'valign': 'vcenter',
                    'align': 'center'}

TIME_FORMAT = {'num_format': 'hh:mm:ss',
               'valign': 'vcenter',
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

    def add_general_date_worksheet(self, name, packaged_data):
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

        g = GeneralDateSheetOrderArea(packaged_data, self.format_dict)
        worksheet.add_area(g)

        return worksheet



if __name__ == '__main__':
    letters = 'abcdefghijklmnopqrstuvwxyz'
    workbook = Workbook('abcdefg.xlsx')

    c = PackagedOrderData(
        (random.randint(1, 100),
         datetime.now().strftime(SQLITE_DATE_TIME_FORMAT_STR),
         random.choice(letters),
         95.0,
         5.0,
         100.0,
         False,
         jsonpickle.encode([]),
         jsonpickle.encode([]),
         True,
         False,
         jsonpickle.encode(
             [MenuItem(random.choice(letters), 10.0) for x in xrange(1)])))

    workbook.add_general_date_worksheet('test', c)
    workbook.close()