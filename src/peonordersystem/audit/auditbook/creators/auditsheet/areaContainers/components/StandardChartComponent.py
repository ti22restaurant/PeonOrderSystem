"""This module defines the audit chart
used for displaying data.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.ChartComponent import ChartComponent

from src.peonordersystem.audit.auditbook.areas.datasheet.DataAreas import DataArea
from src.peonordersystem.audit.auditbook.areas.datasheet.containers.GroupByKeyContainer \
    import GroupByKeyContainer
from src.peonordersystem.audit.auditbook.areas.datasheet.parsers.DataParserFactory \
    import DataParserFactory


class StandardChartComponent(ChartComponent):
    """Describes a class that operates the
    functionality of a chart and places it
    in the given worksheet.
    """

    def __init__(self, value_parser, worksheet, workbook):
        """Initializes the StandardChartComponent.

        @param value_parser: str representing the value
        that should be parsed and stored in this chart.

        @param worksheet: Worksheet representing the
        worksheet that the chart will be written to.

        @param workbook: Workbook that contains a
        datasheet for the data to be stored.
        """
        self._attributes = {'key_parser': 'DATES',
                            'value_parser': value_parser}

        super(StandardChartComponent, self).__init__(worksheet, workbook)

    def _get_keys_area(self):
        """Gets the keys associated
        with the charts.

        @return: Area that represents
        the keys.
        """
        return self._datasheet.date_keys

    def _create_data_areas(self):
        """Creates the data areas
        used for storing the values
        to be associated with the chart.

        @return: None
        """
        parser = DataParserFactory(self._attributes)
        container = GroupByKeyContainer(parser, self._keys.data)
        area = DataArea(container)
        self._datasheet.add_area(area)
        self._areas.append(area)

    def _get_chart(self):
        """Gets the chart that should
        have the data added to it.

        @return: Chart
        """
        title = self._attributes['value_parser'].title()
        return self._workbook.add_chart(title)