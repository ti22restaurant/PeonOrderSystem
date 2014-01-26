"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from collections import Counter

from .workbook import Workbook
from .generalsheet.areas.StandardAreas import (OverviewArea, FrequencyArea,
                                               NotificationArea, OrderArea)

from .datasheet.areas.StandardAreas import (OrdersTimeDataArea, ItemsTimeDataArea,
                                            TotalsTimeDataArea)


class AuditWorkbook(Workbook):
    """AuditWorkbook class defines the standard
    audit style workbook. This includes three
    types of sheets:

        1. Audit Overview Sheet :   which represents the overview
                                    of the data covered in the audit.

        2. Date Overview Sheet  :   which represents the overview
                                    of the data covered on a specific
                                    date.

        3. Date Sheet          :    which represents the order data
                                    for a specific date.

    Each sheet is divided into multiple areas which are generated
    and added in their respective methods.
    """

    def add_date_sheet(self, date_data, packaged_data):
        """Adds a new date sheet to the workbook with the
        given date and populates the sheet with the given
        data.

        @param date_data: datetime.date that represents the
        date associated with this data.

        @param packaged_data: PackagedOrderData that represents
        the dat associated with this sheet.

        @return: None
        """
        name = str(date_data)
        worksheet = self.add_worksheet(name)
        self._add_date_sheet_areas(date_data, worksheet, packaged_data)

    def _add_date_sheet_areas(self, date_data, worksheet, packaged_data):
        """Creates and adds the date sheet areas to the given worksheet.

        @param date_data: datetime.date that represents the date associated
        with the packaged data.

        @param worksheet: Worksheet object that represents the worksheet
        that the areas that contain the data will be added to.

        @param packaged_data: PackagedOrderData that represents
        the data to be added to the areas.

        @return:
        """
        overview_area = self._create_date_sheet_overview_area(date_data, worksheet)
        freq_area = self._create_date_sheet_frequency_area(date_data, worksheet)
        notif_area = self._create_date_sheet_notification_area(date_data, worksheet)

        item_freq = Counter()
        notif_data = []

        for packaged_order in self._generate_date_sheet_order_area(packaged_data,
                                                                   worksheet):
            item_freq.update(packaged_order.item_frequency)
            notif_data += packaged_order.notification_data
            overview_area.add(packaged_order)

        freq_area.add(item_freq)
        notif_area.add(notif_data)

    def _create_date_sheet_overview_area(self, date_data, worksheet):
        """Creates the OverviewArea in the given worksheet.

        @param date_data: datetime.date that represents the date that
        the OverviewArea will be associated with.

        @param worksheet: Worksheet object that the OverviewArea will
        be added to.

        @return: OverviewArea object that has been added to the
        given worksheet.
        """
        overview_area = OverviewArea(date_data)
        worksheet.add_area(overview_area)
        return overview_area

    def _create_date_sheet_frequency_area(self, date_data, worksheet):
        """Creates the FrequencyArea in the given worksheet.

        @param date_data: datetime.date that represents the date
        associated with the data.

        @param worksheet: Worksheet object that the area is to be
        added to.

        @return: FrequencyArea that has been added to the given
        worksheet.
        """
        freq_area = FrequencyArea(date_data, Counter())
        worksheet.add_area(freq_area)
        return freq_area

    def _create_date_sheet_notification_area(self, date_data, worksheet):
        """Creates the NotificationArea in the given worksheet.

        @param date_data: datetime.date that represents the date
        associated with the data.

        @param worksheet: Worksheet object that the area is to be
        added to.

        @return:NotificationArea that has been added to the given
        worksheet.
        """
        notif_area = NotificationArea(date_data, [])
        worksheet.add_area(notif_area)
        return notif_area

    def _generate_date_sheet_order_area(self, packaged_data, worksheet):
        """Generates the order areas for the date sheet.

        @param packaged_data: PackagedOrderData that represents data to
        be added to the order areas.

        @param worksheet: Worksheet that the areas should be added to.

        @return: Generator object that yields packaged order data.
        @yield: PackagedOrderData that has had an order area created
        for it.
        """
        for packaged_order in packaged_data:
            order_area = OrderArea(packaged_order)
            worksheet.add_area(order_area)
            yield packaged_order

    def add_overview_date_sheet(self, packaged_data):
        """Adds a new date overview sheet to the workbook,
        and populates the sheet with the given data.

        @return:
        """
        time_key_area = self.datasheet.time_keys
        time_keys = time_key_area.data

        orders = OrdersTimeDataArea(time_keys)
        items = ItemsTimeDataArea(time_keys)
        totals = TotalsTimeDataArea(time_keys)

        for order in packaged_data:

            orders.insert(order)
            self.add_chart(orders)
            items.insert(order)
            self.add_chart(items)
            totals.insert(order)
            self.add_chart(totals)

    def add_overview_audit_sheet(self):
        """Adds a new audit overview sheet to the workbook,
        and populates the sheet with the given data.

        @return:
        """
        pass