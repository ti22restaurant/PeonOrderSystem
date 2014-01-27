"""This module defines classes that
make heavy usage of the abstract base
class OverviewArea.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from peonordersystem.audit.generalsheet.areas.abc.OverviewArea import \
    OverviewArea


class OrdersOverviewArea(OverviewArea):
    """OrdersOverviewArea is the area that
    represents the area used for displaying
    the overview data for the orders area.
    """

    def __init__(self, date_data):
        """Initializes the OrdersOverviewArea.

        @param date_data: datetime.date representing
        the date associated with this overview area.
        """
        self.date = date_data
        super(OrdersOverviewArea, self).__init__()

    def _get_title_data(self):
        """Gets the title data associated with this
        area.

        @return: str representing the title to be
        associated with this area.
        """
        return 'Order Data for ' + str(self.date)


class DatesOverviewArea(OverviewArea):
    """DatesOverviewArea is the area that
    represents the overview area used for
    displaying the overview data for each
    date.
    """

    def _get_title_data(self):
        """Gets the title data associated with
        this area.

        @return: str representing the title to be
        associated with this area.
        """
        return 'Audit Overview'
