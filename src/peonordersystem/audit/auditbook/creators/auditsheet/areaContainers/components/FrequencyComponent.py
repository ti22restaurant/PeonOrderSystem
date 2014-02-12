"""This module defines components
used for creating and operating
FrequencyAreas.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from collections import Counter
from datetime import date, time, datetime

from .abc.Component import AuditComponent

from src.peonordersystem.audit.auditbook.areas.general.FrequencyArea \
    import FrequencyArea


class FrequencyComponent(AuditComponent):
    """FrequencyComponent describes the
    component used to operate the
    FrequencyArea.
    """

    def __init__(self, worksheet):
        """Initializes a new FrequencyComponent.

        @param worksheet: worksheet that
        represents the worksheet that the
        area should be added to.
        """
        super(FrequencyComponent, self).__init__(worksheet)
        self._freq_area = self._create_area()
        self._freq_data = Counter()

    def _create_area(self):
        """Creates the area by
        connecting it to the
        worksheet.

        @return: FrequencyArea that
        was created.
        """
        area = self._set_up_area()
        self._worksheet.add_area(area)
        return area

    @staticmethod
    def _set_up_area():
        """Sets up the FrequencyArea.

        @return: FrequencyArea that
        was created.
        """
        curr_date = datetime.combine(date.today(), time.min)
        return FrequencyArea(curr_date, Counter())

    def update(self, data):
        """Updates the frequency
        data associated with the
        component.

        @param data: data that is
        to be updated.

        @return: None
        """
        freq_data = data.item_frequency
        self._freq_data.update(freq_data)

    def finalize(self):
        """Finalizes the component.

        @return: None
        """
        self._freq_area.add(self._freq_data)