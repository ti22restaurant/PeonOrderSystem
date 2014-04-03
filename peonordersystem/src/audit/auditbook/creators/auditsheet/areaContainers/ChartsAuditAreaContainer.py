"""This module defines the container that stores
the standard charts used in the audit sheet.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.AreaContainer import AreaContainer
from .components.StandardChartComponent import StandardChartComponent


class ChartsAuditAreaContainer(AreaContainer):
    """Describes the container used for storing
    the _components that make up the general charts
    for the audit sheet.
    """

    def __init__(self, workbook, sheet_name='Date Charts'):
        """Initializes the container.

        @param workbook: Workbook that the charts
        should be added to on a new sheet.

        @keyword sheet_name: str representing the name
        of the sheet that will store the charts. Default
        is 'Date Charts'
        """
        self._workbook = workbook
        self._worksheet = workbook.add_worksheet(sheet_name)

        self._components = []
        self._create_charts_components()

    def _create_charts_components(self):
        """Creates the charts _components.

        @return: None
        """
        self._create_charts_components_orders()
        self._create_charts_components_totals()
        self._create_charts_components_items()

    def _create_charts_components_orders(self):
        """Creates the orders chart component.

        @return: None
        """
        component = StandardChartComponent('ORDERS', self._worksheet, self._workbook)
        self._components.append(component)

    def _create_charts_components_totals(self):
        """Creates the totals charts component.

        @return: None
        """
        component = StandardChartComponent('TOTALS', self._worksheet, self._workbook)
        self._components.append(component)

    def _create_charts_components_items(self):
        """Creates the items chart _components.

        @return: None
        """
        component = StandardChartComponent('ITEMS', self._worksheet, self._workbook)
        self._components.append(component)

    def update(self, data):
        """Updates the _components
        stored in this container.

        @param data: data that the
        _components will be updated
        with.

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