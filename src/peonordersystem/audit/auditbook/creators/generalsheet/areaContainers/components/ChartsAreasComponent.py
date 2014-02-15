"""This module defines the component
that controls the charts areas.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.Component import GeneralComponent

from src.peonordersystem.audit.auditbook.areas.datasheet.DataAreas import DataArea
from src.peonordersystem.audit.auditbook.areas.datasheet.containers.GroupByKeyContainer\
    import GroupByKeyContainer
from src.peonordersystem.audit.auditbook.areas.datasheet.parsers.DataParserFactory\
    import DataParserFactory


class ChartsAreasComponent(GeneralComponent):
    """Provides the functionality for operating
    the charts areas.
    """

    def __init__(self, date, worksheet, workbook):
        """Initializes the component.

        @param date: datetime.date that represents the
        date associated with any incoming data.

        @param worksheet: Worksheet that the charts should
        be added to.

        @param workbook: Workbook that holds the datasheet
        that is used to define the keys and values for the
        charts data.
        """
        self.workbook = workbook
        super(ChartsAreasComponent, self).__init__(date, worksheet)
        self._datasheet = workbook.datasheet
        self._time_keys = self._datasheet.time_keys

        self._orders_chart_data = self._create_orders_data_area()
        self._totals_chart_data = self._create_totals_data_area()
        self._items_chart_data = self._create_items_data_area()

    def _create_orders_data_area(self):
        """Creates the chart data area for
        the orders chart.

        @return: Area
        """
        parser = DataParserFactory({'key_parser': 'TIMES',
                                     'value_parser': 'ORDERS'})
        container = GroupByKeyContainer(parser, self._time_keys.data)
        area = DataArea(container)
        self._datasheet.add_area(area)
        return area

    def _create_totals_data_area(self):
        """Creates the chart data area for
        the totals chart.

        @return: Area
        """
        parser = DataParserFactory({'key_parser': 'TIMES',
                                    'value_parser': 'TOTALS'})
        container = GroupByKeyContainer(parser, self._time_keys.data)
        area = DataArea(container)
        self._datasheet.add_area(area)
        return area

    def _create_items_data_area(self):
        """Creates the chart data area for
        the items chart.

        @return: Area
        """
        parser = DataParserFactory({'key_parser': 'TIMES',
                                    'value_parser': 'ITEMS'})
        container = GroupByKeyContainer(parser, self._time_keys.data)
        area = DataArea(container)
        self._datasheet.add_area(area)
        return area

    def update(self, data):
        """Updates the _components
        data charts.

        @param data: data to be used
        to update the component.

        @return: None
        """
        self._orders_chart_data.insert(data)
        self._totals_chart_data.insert(data)
        self._items_chart_data.insert(data)

    def finalize(self):
        """Finalizes the _components
        data.

        @return: None
        """
        self._create_orders_chart()
        self._create_items_chart()
        self._create_totals_chart()

    def _create_orders_chart(self):
        """Creates the orders chart.

        @return: Chart
        """
        chart = self.workbook.add_chart('Orders Data')
        chart.add_keys_and_data(self._time_keys, self._orders_chart_data, 'Orders')
        self._worksheet.add_area(chart)
        return chart

    def _create_items_chart(self):
        """Creates the items chart

        @return: Chart
        """
        chart = self.workbook.add_chart('Items Data')
        chart.add_keys_and_data(self._time_keys, self._items_chart_data, 'Items')
        self._worksheet.add_area(chart)
        return chart

    def _create_totals_chart(self):
        """Creates the totals chart

        @return: Chart
        """
        chart = self.workbook.add_chart('Totals Data')
        chart.add_keys_and_data(self._time_keys, self._totals_chart_data, 'totals')
        self._worksheet.add_area(chart)
        return chart
