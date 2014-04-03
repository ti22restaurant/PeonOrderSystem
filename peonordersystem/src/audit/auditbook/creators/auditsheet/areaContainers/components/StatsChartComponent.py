"""This module defines the component
for displaying stats chart data including
the mean and median in a single component.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.ChartComponent import ChartComponent

from peonordersystem.src.audit.auditbook.areas.datasheet.DataAreas import DataArea
from peonordersystem.src.audit.auditbook.areas.datasheet.containers.StatsContainer \
    import TimeCategoryStatsContainer


class StatsChartComponent(ChartComponent):
    """Describes the class used for operating
    the functionality of a stats chart.
    """

    def __init__(self, value_parser, worksheet, workbook):
        """Initializes the component.

        @param value_parser: str repersenting the value
        to be parsed by the stats component.

        @param worksheet: Worksheet for the chart to be
        added to.

        @param workbook: Workbook that stores a datasheet
        to allow for storing of charts values.
        """
        self._attributes = {'key_parser': 'TIMES',
                            'value_parser': value_parser}

        super(StatsChartComponent, self).__init__(worksheet, workbook)

    def _get_keys_area(self):
        """Gets the keys area
        associated with the
        charts keys.

        @return: Area
        """
        return self._datasheet.time_keys

    def _create_data_areas(self):
        """Creates the data areas
        used to store the values
        associated with the chart.

        @return: None
        """
        self._create_data_area_mean()
        self._create_data_area_median()

    def _create_data_area_mean(self):
        """Creates the mean area used
        for storing the mean values.

        @return: None
        """
        attr = {'stats_component': 'MEAN'}
        attr.update(self._attributes)

        container = TimeCategoryStatsContainer(attr, self._keys.data)
        area = DataArea(container)
        self._datasheet.add_area(area)
        self._areas.append(area)

    def _create_data_area_median(self):
        """Creates the median area used
        for storing the median values.

        @return: None
        """
        attr = {'stats_component': 'MEDIAN'}
        attr.update(self._attributes)

        container = TimeCategoryStatsContainer(attr, self._keys.data)
        area = DataArea(container)
        self._datasheet.add_area(area)
        self._areas.append(area)

    def finalize(self):
        """Finalizes the component.

        @return: None
        """
        self._create_chart()

    def _create_chart(self):
        """Creates the chart to
        display in the worksheet.

        @return: None
        """
        chart = self._workbook.add_chart()

        chart.add_keys_and_data(self._keys, self._areas[0], title='mean',
                                has_trend_line=True)
        chart.add_keys_and_data(self._keys, self._areas[1], title='median')

        self._worksheet.add_area(chart)

    def _get_chart(self):
        """Gets the chart to display
        in the worksheet.

        @return: Chart
        """
        title = self._attributes['value_parser'].title() + ' stats'
        return self._workbook.add_chart({'type': 'line'}, title)
