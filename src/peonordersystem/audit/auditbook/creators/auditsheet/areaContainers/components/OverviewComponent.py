"""This module provides the component
for populating a container with the
OverviewArea.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.Component import AuditComponent

from src.peonordersystem.audit.auditbook.areas.general.DatesOverviewArea\
    import DatesOverviewArea


class OverviewComponent(AuditComponent):
    """This class describes a component
    that operates a DatesOverviewArea.
    """

    def __init__(self, worksheet):
        """Initializes the OverviewComponent.

        @param worksheet: worksheet that the
        area is to be added to.
        """
        super(OverviewComponent, self).__init__(worksheet)
        self._overview_area = self._create_area()

    def _create_area(self):
        """Creates the area and
        adds it to the worksheet.

        @return: DatesOverviewArea
        that has been created.
        """
        area = DatesOverviewArea()
        self._worksheet.add_area(area)
        return area

    def update(self, data):
        """Updates the area stored
        in this component.

        @param data: data to be added
        to this area.

        @return: None
        """
        self._overview_area.add(data)

    def finalize(self):
        """Finalizes the _components
        areas.

        @return: None
        """
        self._overview_area.finalize()