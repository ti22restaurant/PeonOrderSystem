"""ChartArea module represents classes
that are used for wrapping and connecting
ChartAreas to Worksheet classes.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from peonordersystem.audit.Area import Area
from peonordersystem.audit.generalsheet.parsers.ChartParser import ChartParser


class ChartArea(Area):
    """ChartArea represents a wrapper
    for the chart that is used to interact
    with the system and allow charts to be
    added to worksheets.
    """

    def __init__(self, chart, chart_data_parser):
        """Initializes the new chart with the
        given chart.

        @param chart: xlsxwriter.Chart that
        represents the chart to be created
        and have data written to it.

        @param chart_data_parser: ChartParser
        object that is used to format chart
        data.
        """
        self._chart = chart
        self._data_parser = chart_data_parser
        self._data = None
        self._keys = None

    def add_keys_and_data(self, keys, data):
        """Adds the keys and data to the chart.

        @param keys: DataArea that represents
        the area storing the keys data.

        @param data: DataArea that represents
        the area storing the values data.

        @return: None
        """
        self._update_stored_keys_and_data(keys, data)
        self._add_chart_keys_and_data()

    def _update_stored_keys_and_data(self, keys, data):
        """Updates the stored keys and data to
        be displayed in this chart area.

        @param keys: DataArea object that
        represents the data to be stored in the keys.

        @param data: DataArea object that
        represents the data to be stored in the
        as the values.

        @return: None
        """
        self._keys = keys.get_data_cells_reference()
        self._data = data.get_data_cells_reference()

    def _add_chart_keys_and_data(self):
        """Adds the current keys and
        data to the chart.

        @return: None
        """
        data = self._get_series_data()
        self._chart.add_series(data)

    def _get_series_data(self):
        """Gets the series data
        that is to be displayed
        as the main data for this
        chart.

        @return: dict representing
        the data to be added as a
        series on this chart.
        """
        data = self._data_parser.series_data(self._keys, self._data)
        return data

    def _add_trend_line(self):
        """Adds trend line data
        to this chart.

        @return: None
        """
        data = self._get_trend_line_data()
        self._chart.add_series(data)

    def _get_trend_line_data(self):
        """Gets the trend line data
        that will be used in displaying
        the charts trend line.

        @return: dict representing the
        trendline data that will be added
        as a series to the chart.
        """
        data = self._data_parser.trend_line_data(self._data)
        return data

    def connect(self, worksheet, *args, **kwargs):
        """Connects this area to a worksheet.

        @param worksheet: Worksheet class that represents
        the worksheet that the chart will be inserted into.

        @param args: wildcard catchall used to catch
        the standard data passed through the connect
        method such as format_data.

        @param kwargs: wildcard catchall used to
        catch any keyword arguments passed.

        @return: 2 tuple of (int, int) representing
        the row and column that it is safe to append
        data to beneath this generated area.
        """
        row, col = self._unpack_keyword_arguments(**kwargs)
        self._set_chart_properties()
        worksheet.insert_chart(row, col, self._chart)
        return self._data_parser.NUM_OF_ROWS + row, col

    def _unpack_keyword_arguments(self, **kwargs):
        """Unpacks keyword arguments data involving
        row and column data.

        @param kwargs: wildcard catchall used to
        catch any keyword arguments and subsequently
        parse them.

        @return: 2 tuple of (int, int) representing
        the row and column that was given as keyword
        arguments. Default is 0,0.
        """
        row = 0
        col = 0

        if 'row' in kwargs:
            row = kwargs['row']
        if 'col' in kwargs:
            col = kwargs['col']

        return row, col

    def _set_chart_properties(self):
        """Sets the chart properties.

        @return: None
        """
        self._set_chart_properties_size()
        self._set_chart_properties_title()
        self._set_chart_properties_axis()

    def _set_chart_properties_size(self):
        """Sets the chart properties size
        value.

        @return: None
        """
        size = self._get_chart_size_data()
        self._chart.set_size(size)

    def _get_chart_size_data(self):
        """Gets the chart size data.

        @return: dict representing
        the chart size data.
        """
        return self._data_parser.size_data()

    def _set_chart_properties_axis(self):
        """Sets the chart properties axis.

        @return: None
        """
        self._set_chart_axis_x()
        self._set_chart_axis_y()

    def _set_chart_axis_x(self):
        """Sets the x axis data for
        the chart.

        @return: None
        """
        data = self._get_chart_axis_x_data()
        self._chart.set_x_axis(data)

    def _get_chart_axis_x_data(self):
        """Gets the chart x axis data.

        @return: dict that represents
        the x axis chart data.
        """
        return self._data_parser.x_axis_data()

    def _set_chart_axis_y(self):
        """Sets the y-axis chart data.

        @return: None
        """
        data = self._get_chart_y_axis_data()
        self._chart.set_y_axis(data)

    def _get_chart_y_axis_data(self):
        """Gets the chart y-axis data
        to be displayed.

        @return: dict representing the
        y-axis data.
        """
        return self._data_parser.y_axis_data()

    def _set_chart_properties_title(self):
        """Sets the title property for the
        chart.

        @return: None
        """
        data = self._get_chart_title_data()
        self._chart.set_title(data)

    def _get_chart_title_data(self):
        """Gets the title data to be
        displayed in the chart.

        @return: dict representing the
        title data to be displayed.
        """
        return self._data_parser.title_data()


class DataChartArea(ChartArea):
    """DataChartArea represents a chart
    area used to display data values.
    """

    def __init__(self, chart, chart_name=''):
        """Initializes a new DataChartArea object.

        @param chart: xlsxwriter.Chart object that
        represents the chart to have the data added
        to it.

        @keyword chart_name: str representing the
        value to be displayed as the charts name.
        By default is empty string.
        """
        data_parser = ChartParser(chart_name)
        super(DataChartArea, self).__init__(chart, data_parser)
