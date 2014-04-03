"""This module defines the component
that is used to generate the main areas
for an order audit.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from collections import Counter

from .abc.Component import GeneralComponent

from peonordersystem.src.audit.auditbook.areas.general.OverviewAreas \
    import OrdersOverviewArea
from peonordersystem.src.audit.auditbook.areas.general.FrequencyArea \
    import FrequencyArea
from peonordersystem.src.audit.auditbook.areas.general.OrderArea import OrderArea
from peonordersystem.src.audit.auditbook.areas.general.NotificationArea \
    import NotificationArea


class MainAreasComponent(GeneralComponent):
    """Component that is used to provide the
    functionality for displaying a single
    dates order data.
    """

    def __init__(self, date, worksheet, **flags):
        """Initializes the component.

        @param date: datetime.date that represents
        the date this area covers.

        @param worksheet: Worksheet to which the
        areas should be added.

        @keyword flags: keyword argument that allows
        for customization of the functionality of the
        area. Accepted values are:

            'orders':        :   bool value that represents if
                                 each consecutive orders information
                                 should be created and displayed.


            'frequency'     :   bool value that represents if
                                the frequency area should be
                                generated.

            'notification'  :   bool value that represents if the
                                notification data should be created.
        """
        super(MainAreasComponent, self).__init__(date, worksheet)
        self._areas = []
        self._freq_data = Counter()

        self._flags = flags

        self._overview_area = self._create_overview_area()
        self._frequency_area = self._create_frequency_area()
        self._notification_area = self._create_notification_area()

    def _create_overview_area(self):
        """Creates the overview area.

        @return: Area
        """
        area = OrdersOverviewArea(self._date)
        self._worksheet.add_area(area)
        self._areas.append(area)
        return area

    def _update_overview_area(self, data):
        """Updates the overview area.

        @param data: data that will be
        used to update the area.

        @return: None
        """
        self._overview_area.add(data)

    def _create_frequency_area(self):
        """Creates the frequency area.

        @return: Area
        """
        if self._flags['frequency']:
            area = FrequencyArea(self._date, Counter())
            self._worksheet.add_area(area)
            self._areas.append(area)
            return area

    def _update_frequency_area(self, data):
        """Updates the frequency area.

        @param data: data that will be
        used to update the area.

        @return: None
        """
        if self._flags['frequency']:
            self._frequency_area.add(data)

    def _create_notification_area(self):
        """Creates the notification area.

        @return: Area
        """
        if self._flags['notification']:
            area = NotificationArea(self._date, [])
            self._worksheet.add_area(area)
            self._areas.append(area)
            return area

    def _update_notification_area(self, data):
        """Updates the notification area.

        @param data: data that is to be
        used to update the notification area.

        @return: None
        """
        data = data.notification_data
        if self._flags['notification']:
            self._notification_area.add(data)

    def update(self, data):
        """Updates the _components data.

        @param data: data used to update
        the component.

        @return: None
        """
        self._update_freq_data(data)
        self._create_orders_area(data)
        self._update_overview_area(data)
        self._update_notification_area(data)

    def _update_freq_data(self, data):
        """Updates the _components freq_data.

        @param data: data to be used to
        update the freq_data.

        @return: None
        """
        freq_data = data.item_frequency
        self._freq_data.update(freq_data)

    def _create_orders_area(self, data):
        """Creates the orders area.

        @param data: data that the orders
        area will display.

        @return: Area
        """
        if self._flags['orders']:
            area = OrderArea(data)
            self._worksheet.add_area(area)
            self._areas.append(area)
            return area

    def finalize(self):
        """Finalizes the component.

        @return: None
        """
        self._update_frequency_area(self._freq_data)

        for area in self._areas:
            area.finalize()
