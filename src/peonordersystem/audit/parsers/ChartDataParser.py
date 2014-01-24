"""This module defines classes that
are used to generate data in the proper
format for displaying in charts.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""


class ChartDataParser(object):
    """Defines a class that stores
    functionality for obtaining chart
    data.
    """

    NUM_OF_ROWS = 29
    CHART_HEIGHT = 576

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

    def series_data(self, categories, values, title='values'):
        """Gets the series data used to display the
        chart series.

        @param categories: str representing an absolute
        cell reference to the categories data.

        @param values: str representing an absolute
        cell reference to the values data.

        @keyword title: str representing the title
        to be associated with the series added. Default
        is 'values'

        @return: dict that represents the data to be
        added to the chart.
        """
        data = {'categories': categories,
                'line': {'name': title},
                'values': values}
        return data

    def trend_line_data(self, values, title='trend line'):
        """Gets the trend line data used to display
        the trend line in the chart.

        @param values: str representing an absolute
        cell reference to the data.

        @keyword title: str representing the title
        to be associated with the trend line data.
        Default is 'trend line'.

        @return: dict that represents the data to
        be added to the chart.
        """
        data = {'values': values,
                'trendline': {'type': 'polynomial',
                              'name': title,
                              'order': self.TREND_LINE_ORDER,
                              'width': self.TREND_LINE_WIDTH,
                              'dash_type': 'long_dash'}}
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