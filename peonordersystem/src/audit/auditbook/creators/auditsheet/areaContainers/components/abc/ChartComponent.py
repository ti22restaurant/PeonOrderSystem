"""This module defines the abstract base class
for all AuditComponents that are charts.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .Component import AuditComponent
from abc import ABCMeta, abstractmethod


class ChartComponent(AuditComponent):
    """Describes the base functionality
    and required methods for the a component
    to be useable as a ChartComponent.
    """

    __metaclass__ = ABCMeta

    def __init__(self, worksheet, workbook):
        """Initializes the ChartComponent.

        @param worksheet: Worksheet that this
        ChartComponent is to be added to.

        @param workbook: Workbook that contains
        the datasheet where the data areas can
        be placed
        """
        super(ChartComponent, self).__init__(worksheet)
        self._workbook = workbook

        self._datasheet = workbook.datasheet
        self._keys = self._get_keys_area()

        self._titles = []

        self._areas = []
        self._create_data_areas()

        self.runs = 0

    @abstractmethod
    def _get_keys_area(self):
        """Gets the keys area
        to be associated with
        the chart.

        @return: Area
        """
        pass

    @abstractmethod
    def _create_data_areas(self):
        """Creates the data areas
        to be used by the chart.

        These values should be added
        to the areas field.

        @return: None
        """
        pass

    def update(self, data):
        """Updates the chart
        with the given data.

        @param data: data to
        be used to update the
        chart.

        @return: None
        """
        for area in self._areas:
            area.insert(data)

    def finalize(self):
        """Finalizes the chart
        area.

        @return: None
        """
        chart = self._get_chart()

        for area in self._areas:
            chart.add_keys_and_data(self._keys, area)

        self._worksheet.add_area(chart)

    @abstractmethod
    def _get_chart(self):
        """Gets the chart
        that will be stored
        in the worksheet.

        @return: Chart
        """
        pass