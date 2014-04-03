"""This module defines the wrapper used
to wrap the chart to provide functionality
to the audit system

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.AuditChart import AuditChart
from .parsers.ChartDataParser import ChartDataParser


class XLChart(AuditChart):
    """Provides the functionality
    for operating an XLChart through
    the AuditChart interface.
    """

    def __init__(self, chart, name):
        """Initializes the chart.

        @param chart: xlsxwriter.Chart object
        that is the chart being wrapped by
        this class.

        @param name: str representing the
        name associated with the chart.
        """
        self._chart = chart
        self._chart_data_parser = ChartDataParser(name)

        self._keys = None
        self._values = []

        self._set_chart_properties()

    @property
    def height(self):
        """Gets the height in
        number of rows.

        @return: int
        """
        return self._chart_data_parser.NUM_OF_ROWS

    @property
    def width(self):
        """Gets the width in
        number of columns

        @return: int
        """
        return self._chart_data_parser.CHART_WIDTH

    def _set_chart_properties(self):
        """Sets the charts default
        properties from its data parser.

        @return: None
        """
        self._set_chart_properties_size()
        self._set_chart_properties_title()
        self._set_chart_properties_axis()

    def _set_chart_properties_size(self):
        """Sets the charts default size
        property.

        @return: None
        """
        data = self._chart_data_parser.size_data()
        self._chart.set_size(data)

    def _set_chart_properties_title(self):
        """Sets the charts default title
        property.

        @return: None
        """
        data = self._chart_data_parser.title_data()
        self._chart.set_title(data)

    def _set_chart_properties_axis(self):
        """Sets the charts axis properties.

        @return: None
        """
        self._set_chart_axis_x()
        self._set_chart_axis_y()

    def _set_chart_axis_x(self):
        """Sets the charts x axis properties.

        @return: None
        """
        data = self._chart_data_parser.x_axis_data()
        self._chart.set_x_axis(data)

    def _set_chart_axis_y(self):
        """Sets the charts y axis properties.

        @return: None
        """
        data = self._chart_data_parser.y_axis_data()
        self._chart.set_y_axis(data)

    def set_keys(self, keys):
        """Sets the keys associated
        with the chart. Only one set
        of keys may be active on the
        chart.

        @param keys: collection representing
        that will represent the x axis of this
        chart.

        @return: None
        """
        self._keys = keys

    def add_series(self, data, title='values', has_trend_line=False):
        """Adds the data as a series to the
        chart.

        @param data: collection of data that
        is to be added as a series on the chart.

        @return: None
        """
        self._values.append(data)
        series_data = self._chart_data_parser.series_data(self._keys, data, title,
                                                          has_trend_line)
        self._chart.add_series(series_data)
