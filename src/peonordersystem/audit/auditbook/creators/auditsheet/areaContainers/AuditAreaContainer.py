"""This module defines the general
AuditAreaContainer that is used
to gather components together
and control the functionality of
areas.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.AreaContainer import AreaContainer
from .components.OverviewComponent import OverviewComponent
from .components.FrequencyComponent import FrequencyComponent


class AuditAreaContainer(AreaContainer):
    """Describes a class that controls
    areas at a higher level to disseminate
    information through update and finalize.
    """

    def __init__(self, workbook, **flags):
        """Initializes the AuditAreaContainer.

        @param workbook: workbook that represents
        the workbook that a worksheet with the
        respective component areas should be
        added to.
        """
        self.worksheet = workbook.add_worksheet('Audit Overview')
        self._flags = flags
        self._components = []
        self._create_components()

    def _create_components(self):
        """Creates the necessary _components
        for the container.

        @return: None
        """
        self._create_overview_component()
        self._create_frequency_component()

    def _create_overview_component(self):
        """Creates the overview component

        @return: None
        """
        component = OverviewComponent(self.worksheet)
        self._components.append(component)

    def _create_frequency_component(self):
        """Creates the frequency component

        @return: None
        """
        if self._flags['frequency']:
            component = FrequencyComponent(self.worksheet)
            self._components.append(component)

    def update(self, data):
        """Updates the containers _components.

        @param data: data to update the
        _components with.

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