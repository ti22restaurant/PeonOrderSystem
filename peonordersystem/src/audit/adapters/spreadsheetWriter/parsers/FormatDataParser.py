"""This module defines the format data
used in to create the necessary XLFormats

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""


class FormatDataParser(object):
    """Parser that stores and accesses
    format data used to generate
    XLFormats
    """

    _format_data = {
        'left_column':                  {'left': 1,
                                         'align': 'center'},

        'right_column':                 {'right': 1,
                                         'align': 'center'},

        'time_format':                  {'num_format': 'hh:mm',
                                         'valign': 'vcenter',
                                         'align': 'center'},

        'date_format':                  {'num_format': 'mmmm d yyyy',
                                         'valign': 'vcenter',
                                         'align': 'center'},

        'datetime_format':              {'num_format': 'mm/dd/yy hh:mm',
                                         'valign': 'vcenter',
                                         'align': 'center'},

        'title_format_left':            {'bold': True,
                                         'font_size': 10,
                                         'left': 1,
                                         'top': 1,
                                         'bottom': 1,
                                         'valign': 'vcenter',
                                         'align': 'center'},

        'title_format_center':          {'bold': True,
                                         'font_size': 10,
                                         'top': 1,
                                         'bottom': 1,
                                         'valign': 'vcenter',
                                         'align': 'center'},

        'title_format_right':           {'bold': True,
                                         'font_size': 10,
                                         'right': 1,
                                         'top': 1,
                                         'bottom': 1,
                                         'valign': 'vcenter',
                                         'align': 'center'},

        'subtitle_format_left':         {'bold': True,
                                         'font_size': 8,
                                         'left': 1,
                                         'top': 1,
                                         'bottom': 1,
                                         'valign': 'vcenter',
                                         'align': 'center',
                                         'font_color': 'gray'},

        'subtitle_format_center':       {'bold': True,
                                         'font_size': 8,
                                         'top': 1,
                                         'bottom': 1,
                                         'valign': 'vcenter',
                                         'align': 'center',
                                         'font_color': 'gray'},

        'subtitle_format_right':       {'bold': True,
                                        'font_size': 8,
                                        'right': 1,
                                        'top': 1,
                                        'bottom': 1,
                                        'valign': 'vcenter',
                                        'align': 'center',
                                        'font_color': 'gray'},

        'main_title_data_format':       {'bold': True,
                                         'valign': 'vcenter',
                                         'align': 'center',
                                         'border': 1,
                                         'font_size': 15},

        'title_data_format':            {'bold': True,
                                         'valign': 'vcenter',
                                         'align': 'center',
                                         'top': 1,
                                         'bottom': 1,
                                         'font_size': 11},

        'subtitle_data_format':         {'font_color': 'gray',
                                         'valign': 'vcenter',
                                         'align': 'center',
                                         'top': 1,
                                         'bottom': 1,
                                         'left': 1,
                                         'font_size': 8},

        'total_data_format':            {'num_format': '$#,##0.00;[Red]-$#,##0.00',
                                         'valign': 'vcenter',
                                         'align': 'center',
                                         'right': 1,
                                         'bold': True},

        'subtotal_data_format':         {'font_color': 'gray',
                                         'font_size': 8,
                                         'align': 'center',
                                         'top': 1,
                                         'bottom': 1,
                                         'right': 1,
                                         'num_format': '$#,##0.00'},

        'item_data_format_left':        {'left': 1,
                                         'bold': True,
                                         'font_size': 12},

        'item_data_format_right':       {'right': 1,
                                         'font_size': 10},

        'subitem_data_format_left':     {'left': 1,
                                         'font_size': 8,
                                         'font_color': 'gray',
                                         'valign': 'vjustify',
                                         'align': 'center'},

        'subitem_data_format_center':   {'font_color': 'gray',
                                         'font_size': 8,
                                         'valign': 'vjustify',
                                         'align': 'center'},

        'subitem_data_format_right':    {'right': 1,
                                         'font_size': 8,
                                         'font_color': 'gray',
                                         'valign': 'vjustify',
                                         'align': 'center'},

        'subitem_data_total_format':    {'right': 1,
                                         'font_size': 8,
                                         'font_color': 'gray',
                                         'num_format': '$#,##0.00',
                                         'valign': 'vjustify',
                                         'align': 'center'}
    }

    def get_format_data(self):
        """

        @return:
        """
        return self._format_data
