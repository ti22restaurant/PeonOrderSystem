"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""

from abc import ABCMeta, abstractmethod


class FormatData(object):
    """Abstract Base Class

    FormatData represents the base class
    that provides the functionality for
    storing and retrieving format data
    associated with a connected workbook.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """initializes a new FormatData"""
        self._workbook = None
        self._format_info = self._get_format_info()
        self._format_data = {}

    @abstractmethod
    def _get_format_info(self):
        """abstract method.

        Gets the format info used to populate
        the format data when connected to a
        workbook.

        @return: dict of str keys to dict
        values that represent formats.
        """
        pass

    def keys(self):
        """Gets the keys associated
        with the formats.

        @return: list of str representing
        the keys.
        """
        return self._format_data.keys()

    def __getitem__(self, item):
        """Gets the value at the given
        item index.

        @param item: str representing the
        key.

        @return: xlsxwriter.Format object
        that represents the associated
        format.
        """
        return self._format_data[item]

    def _check_null_workbook(self):
        """Checks that the current workbook
        is empty and has the None value.

        @raise StandardError: if the workbook
        isn't None.

        @return: bool value representing if
        the test was passed.
        """
        if self._workbook:
            raise StandardError('Cannot perform this operation if FormatData '
                                'already has a Workbook connected.')
        return True

    def connect(self, workbook):
        """Connects the format data
        to a workbook.

        @param workbook: xlsxwriter.Workbook
        object that represents the workbook
        to have the data added to.

        @return: None
        """
        self._check_null_workbook()
        self._workbook = workbook
        self._add_workbook_data()

    def _add_workbook_data(self):
        """Adds the format info to the workbook

        @return: None
        """
        self._format_data = self._update_format_data()

    def _update_format_data(self):
        """updates the workbooks format
        data by parsing the format info.

        @return: dict of str to
        xlsxwriter.Format objects that
        represent the created formats.
        """
        format_data = {}

        for key, data in self._format_info.items():
            frmt = self._workbook._add_format(data)
            format_data[key] = frmt

        return format_data

    def __iter__(self):
        """@return: iter over the format keys"""
        return iter(self._format_data)


class StandardFormatData(FormatData):
    """StandardFormatData represents format data
    that is commonly used.
    """

    #================================================================================
    # This block represents formatting constants used in the standard data format
    #================================================================================
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

    def _get_format_info(self):
        """Gets the format info used to
        generate the format data.

        @return: dict that maps str to
        dict. Each value represents the
        info that will be a specific format.
        """
        format_dict = {}
        format_dict['left_column'] = self.LEFT_COL_FORMAT
        format_dict['right_column'] = self.RIGHT_COL_FORMAT

        format_dict['time_format'] = self.TIME_FORMAT
        format_dict['date_format'] = self.DATE_FORMAT
        format_dict['datetime_format'] = self.DATE_TIME_FORMAT

        format_dict['title_format_left'] = self.TITLE_FORMAT_LEFT
        format_dict['title_format_center'] = self.TITLE_FORMAT_CENTER
        format_dict['title_format_right'] = self.TITLE_FORMAT_RIGHT

        format_dict['subtitle_format_left'] = self.SUBTITLE_FORMAT_LEFT
        format_dict['subtitle_format_center'] = self.SUBTITLE_FORMAT_CENTER
        format_dict['subtitle_format_right'] = self.SUBTITLE_FORMAT_RIGHT

        format_dict['main_title_data_format'] = self.MAIN_TITLE_DATA_FORMAT
        format_dict['title_data_format'] = self.TITLE_DATA_FORMAT
        format_dict['subtitle_data_format'] = self.SUBTITLE_DATA_FORMAT
        format_dict['total_data_format'] = self.TOTAL_DATA_FORMAT
        format_dict['subtotal_data_format'] = self.SUBTOTAL_DATA_FORMAT

        format_dict['item_data_format_left'] = self.ITEM_DATA_FORMAT_LEFT
        format_dict['item_data_format_right'] = self.ITEM_DATA_FORMAT_RIGHT

        format_dict['subitem_data_format_left'] = self.SUBITEM_DATA_FORMAT_LEFT
        format_dict['subitem_data_format_center'] = self.SUBITEM_DATA_FORMAT_CENTER
        format_dict['subitem_data_format_right'] = self.SUBITEM_DATA_FORMAT_RIGHT

        format_dict['subitem_data_total_format'] = self.SUBITEM_DATA_TOTAL_FORMAT

        return format_dict