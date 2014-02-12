"""This module defines the general container
used to operate standard orders areas.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from .abc.AreaContainer import AreaContainer
from .components.ChartsAreasComponent import ChartsAreasComponent
from .components.MainAreasComponent import MainAreasComponent


class GeneralAreaContainer(AreaContainer):
    """Operates and controls functionality
    of displaying the data in the orders over
    a single date.
    """

    def __init__(self, date, workbook, **flags):
        """Initializes the container.

        @param date: datetime.date that represents
        the date associated with the data to be
        added,

        @param workbook: Workbook that the necessary
        worksheets will be added to to display the
        data and also contains a datasheet used for
        storing charts keys and values

        @keyword flags: keyword arguments that allow
        for customization of the areas created by this
        container. Accepted keywords:

            'orders':        :   bool value that represents if
                                 each consecutive orders information
                                 should be created and displayed.


            'frequency'     :   bool value that represents if
                                the frequency area should be
                                generated.

            'notification'  :   bool value that represents if the
                                notification data should be created.

            'order_charts'  :   bool value representing if the
                                data should be parsed and displayed
                                in charts.
        """
        self._flags = flags

        self.date = date
        self.workbook = workbook
        self._components = []

        self._create_components()

    def _create_components(self):
        """Creates the _components to
        provide the functionality.

        @return: None
        """
        self._create_main_component()
        self._create_charts_component()

    def _create_main_component(self):
        """Creates the main component for
        displaying the order data.

        @return: None
        """
        ws = self.workbook.add_worksheet(str(self.date))
        component = MainAreasComponent(self.date, ws, **self._flags)
        self._components.append(component)

    def _create_charts_component(self):
        """Creates the charts component.

        @return: None
        """
        if self._flags['order_charts']:
            title = 'data on ' + str(self.date)

            ws = self.workbook.add_worksheet(title)
            component = ChartsAreasComponent(self.date, ws, self.workbook)
            self._components.append(component)

    def update(self, data):
        """Updates the containers data.

        @param data: data to update the
        container with.

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


