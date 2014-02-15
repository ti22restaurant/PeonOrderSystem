"""ChartArea module represents classes
that are used for wrapping and connecting
ChartAreas to Worksheet classes.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from peonordersystem.audit.auditbook.areas.abc.Area import Area


class ChartArea(Area):
    """ChartArea represents a wrapper
    for the chart that is used to interact
    with the system and allow charts to be
    added to worksheets.
    """

    def __init__(self, chart):
        """Initializes the new chart with the
        given chart.

        @param chart: XLChart that represents
        the chart to have the functionality
        performed on it.
        """
        self._chart = chart

    def add_keys_and_data(self, keys, data, title='values', has_trend_line=False):
        """Adds the keys and data to the chart.

        @param keys: DataArea that represents
        the area storing the keys data.

        @param data: DataArea that represents
        the area storing the values data.

        @keyword title: str representing the
        title associated with the data.

        @keyword has_trend_line: bool value
        representing of the data should
        display a trend line as well.

        @return: None
        """
        self._chart.set_keys(keys)
        self._chart.add_series(data, title=title, has_trend_line=has_trend_line)

    def connect(self, worksheet):
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
        row = worksheet.row
        col = worksheet.col
        worksheet.insert_chart(row, col, self._chart)

        return self._chart.height + row, col
