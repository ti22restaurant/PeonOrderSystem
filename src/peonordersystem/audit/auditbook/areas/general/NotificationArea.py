"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from peonordersystem.MenuItem import is_discount_item
from .abc.GeneralArea import GeneralArea


class NotificationArea(GeneralArea):
    """NotificationArea represents the area where
    that may be added to a datasheet. This area
    is for displaying MenuItems that are are
    considered a notification type.

    @var date: datetime.date object that represents
    the date associated with this area.

    @var data: list of MenuItem objects that represents
    the notification items that are displayed in this
    NotificationArea's data area.

    @var num_of_discounts: int representing the number
    of DiscountItems that are displayed in the data
    area.

    @var num_of_comps: int representing the number
    of comped items that are displayed in the data
    area.
    """

    def __init__(self, date_data, notification_data):
        """Initializes the notifications area.

        @param date_data: datetime.date object
        representing the date associated with
        this area.

        @param notification_data: list of MenuItems
        that represents the notification data to be
        displayed in this area.
        """
        self.date = date_data
        self.data = notification_data

        self.num_of_discounts = 0
        self.num_of_comps = 0

        super(NotificationArea, self).__init__()

    def update_title_data(self):
        """Override Method.

        Updates the title data.

        @return: None
        """
        title = 'Notification Items on {}'.format(self.date)
        super(NotificationArea, self).update_title_data(title, self.date)

    def update_total_data(self):
        """Override Method.

        Updates the total data.

        @return: None
        """
        totals_data = self._get_totals_data()
        subtotals_data = self._get_subtotals_data()
        super(NotificationArea, self).update_total_data(totals_data, subtotals_data)

    def _get_format_total_data(self):
        """Override Method

        Gets the format used to display
        the total data.

        @return: xlsxwriter.Format used to
        display the total data.
        """
        return self.format_data['title_format_right']

    def _get_format_subtotal_data(self):
        """Override Method

        Gets the format used to display
        the subtotal data.

        @return: xlsxwriter.Format used to
        dispolay the subtotal data.
        """
        return self.format_data['subtitle_format_right']

    def _get_totals_data(self):
        """Gets the total associated
        with this area.

        @return: tuple where each index
        is (str, int) representing the
        total name and the total data to
        be displayed.
        """
        return ('Total items', len(self.data)),

    def _get_subtotals_data(self):
        """Gets the subtotal associated
        with this area.

        @return: tuple where each index
        is (str, int) represent the subtotal
        name and subtotal data to be displayed.
        """
        return (('Discount Items Total', self.num_of_discounts),
                ('Comped Items Total', self.num_of_comps))

    def connect(self, worksheet):
        """Override Method

        Connects the area to the given
        worksheet allowing the area to write
        the data to the worksheet.

        @param worksheet: xlsxwriter.worksheet.Worksheet
        object that represents the sheet that the area
        will be written to.

        @return: 2 tuple of (int, int) representing the
        row and column that it is safe to add another
        area.
        """
        values = super(NotificationArea, self).connect(worksheet)
        self.update_title_data()
        self._add_initial_data()
        return values

    def _add_initial_data(self):
        """Adds the initial stored data
        to the NotificationArea.

        @return: None
        """
        for item in self.data:
            self._add_item_data(item)
        self.update_total_data()

    def _write_item_data(self, menu_item):
        """Writes the item data to the data
        area.

        @param menu_item: MenuItem object
        that represents the notification
        item to be written to the data area.

        @return: None
        """
        self._write_item_data_name(menu_item.get_name())
        self._write_item_data_price(menu_item.get_price())

    def _write_item_data_name(self, item_name):
        """Writes the item name to the data
        area.

        @param item_name: str representing
        the item name to be written to the
        data area.

        @return: None
        """
        format = self._get_item_data_name_format()
        self.write_data(item_name, format=format)

    def _get_item_data_name_format(self):
        """Gets the format used to display
        the item data name.

        @return: xlsxwriter.Format that is
        used to display the item name to the
        data area.
        """
        return self.format_data['item_data_format_left']

    def _write_item_data_price(self, item_price):
        """Writes the item price data to the
        data area.

        @param item_price: float representing the
        item price.

        @return: None
        """
        format = self._get_item_data_price_format()
        self.write_data(item_price, col=self.area_end_col, format=format)

    def _get_item_data_price_format(self):
        """Gets the item price format that
        will be used to display to the data
        area.

        @return: xlsxwriter.Format that is
        used to format the data to display
        to the area.
        """
        return self.format_data['total_data_format']

    def add(self, notification_data):
        """Override Method

        Adds the given notification data
        to the data area and updates the totals.

        @param notification_data: list of MenuItem
        objects that represents the data to be added
        to the NotificationArea's data area.

        @return: None
        """
        for notification_item in notification_data:
            self._add_item_data(notification_item)
            self.data.append(notification_item)

    def _add_item_data(self, item):
        """Adds the given item data to the
        areas data area.

        @param item: MenuItem object that
        represents the data to be added.

        @return: None
        """
        self._write_item_data(item)
        self._update_item_data(item)
        self.row += 1

    def _update_item_data(self, item):
        """Updates the stored item data.

        @param item: MenuItem object that
        is used to update the stored data.

        @return: None
        """
        try:
            if is_discount_item(item):
                self.num_of_discounts += 1
        except ValueError:
            self.num_of_comps += 1

    def finalize(self):
        """Finalizes the totals
        section.

        @return: None
        """
        self.update_total_data()