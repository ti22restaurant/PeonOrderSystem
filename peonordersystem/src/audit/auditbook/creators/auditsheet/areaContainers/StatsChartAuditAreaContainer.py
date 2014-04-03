"""This module defines the container
used for creating and accessing audit
wide stats charts.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.AreaContainer import AreaContainer
from .components.StatsChartComponent import StatsChartComponent


class StatsChartsAuditAreaContainer(AreaContainer):
    """Describes the class that is used to hold
    stats charts data and operate their functionality.
    """

    def __init__(self, workbook, sheet_name='Stats Charts'):
        """Initializes the container.

        @param workbook: Workbook that a new stats chart
        sheet should be added to.

        @keyword sheet_name: str representing the name that
        the sheet the container operates on should be named.
        """
        self._workbook = workbook
        self._worksheet = workbook.add_worksheet(sheet_name)

        self._components = []

        self._create_stats_charts_components()

    def _create_stats_charts_components(self):
        """Creates the stats charts _components.

        @return: None
        """
        self._create_stats_charts_components_orders()
        self._create_stats_charts_components_totals()

    def _create_stats_charts_components_orders(self):
        """Creates the orders stats charts.

        @return: None
        """
        component = StatsChartComponent('ORDERS', self._worksheet, self._workbook)
        self._components.append(component)

    def _create_stats_charts_components_totals(self):
        """Creates the totals stats charts.

        @return: None
        """
        component = StatsChartComponent('TOTALS', self._worksheet, self._workbook)
        self._components.append(component)

    def update(self, data):
        """Updates the container data.

        @param data: data that the _components
        should be updated with.

        @return: None
        """
        for component in self._components:
            component.update(data)

    def finalize(self):
        """Finalizes the container.

        @return: None
        """
        for component in self._components:
            component.finalize()
