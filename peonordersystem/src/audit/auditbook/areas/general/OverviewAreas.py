"""This module defines classes that
make heavy usage of the abstract base
class OverviewArea.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.OverviewArea import OverviewArea


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

    def _get_date_data(self):
        """Gets the date data associated
        with this area.

        @return: datetime.date object
        representing the datetime.
        """
        return self.date

    def add(self, packaged_order):
        """

        @param packaged_order:
        @return:
        """
        self._check_date(packaged_order.date)
        super(OrdersOverviewArea, self).add(packaged_order)

    def _check_date(self, order_date):
        """Checks that the given date is
        within this overview areas date range.

        @raise ValueError: If the given date is
        not equal to the stored date.

        @param order_date: datetime.date that
        represents the date to be checked.

        @return: bool value that represents
        if the test was passed.
        """
        if not order_date or not order_date == self.date:
            raise ValueError('Expected all values to be in the on ' +
                             ' the same date. Some values within ' +
                             ' the given packaged order data were' +
                             ' not.')

        return True