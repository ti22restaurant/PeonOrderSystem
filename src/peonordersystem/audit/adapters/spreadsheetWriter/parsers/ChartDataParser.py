"""This module defines classes that
are used to generate data in the proper
format for displaying in charts.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from src.peonordersystem.audit.auditbook.areas.datasheet.abc.DataArea import \
    AbstractDataArea


class ChartDataParser(object):
    """Defines a class that stores
    functionality for obtaining chart
    data.
    """

    NUM_OF_ROWS = 29
    CHART_HEIGHT = 576

    NUM_OF_COLS = 17
    CHART_WIDTH = 1400

    TREND_LINE_ORDER = 5
    TREND_LINE_WIDTH = 1.5

    X_AXIS_FONT_SIZE = 8
    X_AXIS_FONT_ROTATION = 45

    def __init__(self, chart_name):
        """Initializes the ChartDataParser

        @param chart_name: str representing
        the name associated with this object.
        """
        self.chart_name = chart_name

    @staticmethod
    def _check_data(data):
        """Checks if the data can be
        parsed.

        @raise TypeError: if the given
        data is not a subclass of
        AbstractDataArea.

        @param data: object to be
        checked.

        @return: bool value representing
        if the test was passed.
        """
        if not data or not isinstance(data, AbstractDataArea):
            raise TypeError('Chart data can only be parsed if it is a subclass of '
                            'AbstractDataArea!')
        return True

    @staticmethod
    def _check_keys_and_data(keys, data):
        """Checks that the keys and data
        can both be parsed.

        @raise ValueError: If the given
        keys and data to not have a matching
        number of indices

        @param keys: object to be checked
        as the keys.

        @param data: object to be checked
        as the values.

        @return: bool value representing
        if the test was passed.
        """
        ChartDataParser._check_data(keys)
        ChartDataParser._check_data(data)

        if len(keys.data) != len(data.data):
            raise ValueError('Cannot perform this operation if the stored keys '
                             'indices do not have a one to one correspondence to '
                             'the stored data!')
        return True

    @staticmethod
    def default_chart_options():
        """Gets the default chart
        options.

        @return: dict representing
        the default chart options.
        """
        return {'type': 'line'}

    def series_data(self, keys, data, title='data', has_trend_line=False):
        """Gets the series data used to display the
        chart series.

        @param keys: str representing an absolute
        cell reference to the categories data.

        @param data: str representing an absolute
        cell reference to the values data.

        @keyword title: str representing the title
        to be associated with the series added. Default
        is 'values'

        @return: dict that represents the data to be
        added to the chart.
        """
        self._check_keys_and_data(keys, data)
        categories = self._get_data_ref(keys)
        values = self._get_data_ref(data)

        chart_data = {'categories': categories,
                      'name': title,
                      'values': values}

        if has_trend_line:
            trend_line = self.trend_line_data(data)
            chart_data.update(trend_line)

        return chart_data

    def _get_data_ref(self, data):
        """Gets the data reference to
        the cells.

        @param data: AbstractDataArea
         object that represents the
         data stored.

        @return: str representing the
        data reference.
        """
        return data.get_data_cells_reference()

    def trend_line_data(self, data, title='trend line'):
        """Gets the trend line data used to display
        the trend line in the chart.

        @param data: str representing an absolute
        cell reference to the data.

        @keyword title: str representing the title
        to be associated with the trend line data.
        Default is 'trend line'.

        @return: dict that represents the data to
        be added to the chart.
        """
        self._check_data(data)
        values = self._get_data_ref(data)
        data = {'values': values,
                'trendline': {'type': 'polynomial',
                              'name': title,
                              'order': self.TREND_LINE_ORDER,
                              'line': {'width': self.TREND_LINE_WIDTH,
                                       'dash_type': 'long_dash',
                                       'color': 'red'},
                              }
                }
        return data

    def size_data(self):
        """Gets the size data used to format
        the size of the chart.

        @return: dict representing the size
        format data to be used on the chart.
        """
        data = {'height': self.CHART_HEIGHT,
                'width': self.CHART_WIDTH}
        return data

    def x_axis_data(self):
        """Gets the x-axis data used to format
        the x-axis display of the chart.

        @return: dict representing the x-axis
        format data to be used on the chart.
        """
        data = {'num_font': {'size': self.X_AXIS_FONT_SIZE,
                             'rotation': self.X_AXIS_FONT_ROTATION},
                'name': 'Times'}

        return data

    def y_axis_data(self):
        """Gets the y-axis data used to format
        the y-axis display of the chart.

        @return: dict representing the y-axis
        format data to be used on the chart.
        """
        data = {}

        return data

    def title_data(self):
        """Gets the title data to be displayed
        on the chart.

        @return: dict representing the title
        data to be used on the chart.
        """
        return {'name': self.chart_name}