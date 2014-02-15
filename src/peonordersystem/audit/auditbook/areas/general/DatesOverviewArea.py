"""This module defines the behavior
for the DatesOverviewArea.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from collections import OrderedDict

from .abc.OverviewArea import OverviewArea

from src.peonordersystem.audit.adapters.data.MutableData import MutableData


class DatesOverviewArea(OverviewArea):
    """DatesOverviewArea is the area that
    represents the overview area used for
    displaying the overview data for each
    date.
    """

    def __init__(self):
        """Initializes the DatesOverviewArea"""
        super(DatesOverviewArea, self).__init__()
        self._data = OrderedDict()

    def add(self, data):
        """Adds the given data to the order

        @param data: data to be added
        to the area.

        @return: None
        """
        if not data.date in self._data:
            self._create_data(data)
        else:
            self._update_data(data)

    def _update_data(self, data):
        """Updates the stored data.

        @param data: data to be added
        to the area.

        @return: None
        """
        date = data.date
        curr_data = self._data[date]
        curr_data.update(data)

    def _create_data(self, data):
        """Create the a new data
        component.

        @param data: data to be added
        to the area.

        @return: None
        """
        date = data.date
        self._data[date] = MutableData('Date: ' + str(date), data.datetime)
        self._update_data(data)

    def _get_title_data(self):
        """Gets the title data associated with
        this area.

        @return: str representing the title to be
        associated with this area.
        """
        return 'Audit Overview'

    def _get_date_data(self):
        """Gets the date data to
        display

        @return: None
        """
        pass

    def finalize(self):
        """Finalizes the data
        and writes it to the
        area.

        @return: None
        """
        for key, data in self._data.items():
            super(DatesOverviewArea, self).add(data)
        super(DatesOverviewArea, self).finalize()