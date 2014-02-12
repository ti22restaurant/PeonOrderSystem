"""This module defines the creator
that is used to create the general
areas for displaying a specific orders
data.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from src.peonordersystem.audit.auditbook.creators.abc.Creator import Creator
from .areaContainers.GeneralAreaContainer import GeneralAreaContainer


class GeneralsheetCreator(Creator):
    """Provides the functionality for
    displaying order data.

    Categorizes the orders and segments
    them into separate worksheets to
    display the data.
    """

    def __init__(self, workbook, **flags):
        """Initializes the creator

        @param workbook: Workbook that the
        worksheets to display the data should
        be added to.

        @keyword flags: keyword arguments that
        are used to customize what areas are
        created and displayed in the worksheets.
        Accepted keywords are:

            'datesheets'    :   bool value that represents
                                if the data should be parsed
                                for orders.

            'order_charts'  :   bool value that represents
                                if the charts for the orders
                                should be created.

            'orders'        :   bool value that represents if
                                the a unique orders area should
                                be created for every order describing
                                all information in detail.

            'frequency'     :   bool value that represents if the
                                area that display item frequency
                                should be created and displayed.

            'notification'  :   bool value that represents if the
                                area that displays notification data
                                should be created and displayed.
        """
        self.workbook = workbook
        self._flags = flags

        self._components = {}

    def update(self, data):
        """Updates the created
        areas data.

        @param data: data that
        is to be used to update
        the created areas.

        @return: None
        """
        date = data.date
        if date in self._components:
            self._update_component(data)
        else:
            self._create_component(data)

    def _update_component(self, data):
        """Updates the component data.

        @param data: data that is to
        be used to update the components.

        @return: None
        """
        component = self._components[data.date]
        component.update(data)

    def _create_component(self, data):
        """Creates a new component
        with the given data.

        @param data: data that is to
        be used to update the component.

        @return: None
        """
        if self._flags['datesheets']:
            date = data.date
            datesheet_component = GeneralAreaContainer(date, self.workbook,
                                                       **self._flags)
            datesheet_component.update(data)
            self._components[date] = datesheet_component

    def finalize(self):
        """Finalizes the creators areas.

        @return: None
        """
        for component in self._components.values():
            component.finalize()


