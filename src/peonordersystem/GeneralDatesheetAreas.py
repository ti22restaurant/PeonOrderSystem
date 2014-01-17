"""Defines the areas that are part of a standard
GeneralDatesheet.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from collections import Counter

from src.peonordersystem.MenuItem import is_menu_item, is_discount_item
from src.peonordersystem.CheckOperations import (get_total, get_total_tax,
                                                 get_order_subtotal)
from src.peonordersystem.SpreadsheetAreas import SpreadsheetArea


class OrderArea(SpreadsheetArea):
    """OrderArea represents a general
    order that is described through a PackagedOrderData
    object and stores information regarding a single order.

    This order area is used to parse and display data from
    the PackagedOrderData.

    @var: packaged_data: PackagedOrderData information that
    this area should display.
    """

    def __init__(self, packaged_data, format_dict):
        """Initializes the OrderArea
        object with the packaged data.

        @param packaged_data: PackagedOrderData object
        that represents the order areas data.

        @param format_dict: dict that maps str to
        xlsxwriter.Formats that represent the formats
        for cells.
        """
        self.packaged_data = packaged_data
        super(OrderArea, self).__init__(format_dict)

    def connect(self, worksheet):
        """Override Method.

        Connects the area to the worksheet.

        @param worksheet: xlsxwriter.worksheet.Worksheet
        object that represents the worksheet where
        the area will be added.

        @return: 2 tuple of (int, int) representing the
        row and column that the area terminates at. This
        is the coordinates for the upper right hand corner
        where another area could be added.
        """
        values = super(OrderArea, self).connect(worksheet)
        self.update_title_data()
        self.update_total_data()
        self._update_items_data()
        return values

    def _update_items_data(self):
        """Updates the items data by adding
        all the data stored in the packaged
        data to the data area.

        @return: None
        """
        for item in self.packaged_data.data:
            self._write_item(item)

    def update_title_data(self):
        """Override Method.

        Updates the title data

        @return: None
        """
        name = self.packaged_data.name
        date = self.packaged_data.datetime

        super(OrderArea, self).update_title_data(name, date)

    def update_total_data(self):
        """Override Method.

        Updates the total data.

        @return: None
        """
        totals = self._get_total_data()
        subtotals = self._get_subtotal_data()

        super(OrderArea, self).update_total_data(totals,subtotals)

    def _get_total_data(self):
        """Gets the total data stored in this
        areas packaged data.

        @return: tuple where each entry represents the
        (str, float) where the values are the total name
        and total data respectively.
        """
        return ('total', self.packaged_data.totals['total']),

    def _get_subtotal_data(self):
        """Gets the subtotal data stored in this
        areas packaged data.

        @return: tuple where each entry represents the
        (str, float) where the values are the subtotal name
        and the subtotal data respectively.
        """
        return (
            ('tax', self.packaged_data.totals['tax']),
            ('subtotal', self.packaged_data.totals['subtotal'])
        )

    def add(self, menu_item):
        """Adds the given item to the
        data area and updates the totals.

        @raise ValueError: If non MenuItem
        object is given.

        @param menu_item: MenuItem object
        that represents the item to be
        displayed.

        @return: None
        """
        is_menu_item(menu_item)
        self._add_menu_item(menu_item)
        self.update_total_data()

    def _add_menu_item(self, menu_item):
        """Adds the menu_item data to the
        data area.

        @param menu_item: MenuItem object
        that is to be added to the data area.

        @return: None
        """
        self._update_packaged_data(menu_item)
        self._write_item(menu_item)

    def _update_packaged_data(self, menu_item):
        """Updates the packaged data item area
        and data totals areas respectively.

        @param menu_item: MenuItem object that
        is to be used to update the packaged
        data.

        @return: None
        """
        self._update_packaged_data_item(menu_item)
        self._update_packaged_data_totals(menu_item)

    def _update_packaged_data_item(self, menu_item):
        """Updates the packaged data item list with
        the given MenuItem.

        @param menu_item: MenuItem object that is
        to be added to the packaged data's item list.

        @return: MenuItem object that was added.
        """
        self.packaged_data.data.append(menu_item)
        return menu_item

    def _update_packaged_data_totals(self, menu_item):
        """Updates the packaged data totals area with
        the given MenuItems data.

        @param menu_item: MenuItem object that is
        used to update the totals.

        @return: 3 tuple of (float, float, float)
        representing the total, tax, and subtotal
        associated with the MenuItem respectively.
        """
        subtotal = get_order_subtotal((menu_item,))
        tax = get_total_tax(subtotal)
        total = get_total((menu_item,))

        self.packaged_data.totals['total'] += total
        self.packaged_data.totals['tax'] += tax
        self.packaged_data.totals['subtotal'] += subtotal

        return total, tax, subtotal

    def _write_item(self, menu_item):
        """Writes the MenuItems data to the data
        area.

        @param menu_item: MenuItem object that is
        to be added to the area.

        @return: 2 tuple of (int, int) representing the
        row and column that it is safe to append more data
        to after the item has been written.
        """
        row, col = self._write_item_name(menu_item.get_name())
        row, col = self._write_item_price(menu_item.get_price())
        self.row = row

        row, col = self._write_item_stars(menu_item.stars)
        self.row = row

        row, col = self._write_item_options(menu_item.options)
        self.row = row

        row, col = self._write_item_note(menu_item.notes)
        self.row = row

        return self.row, col

    def _write_item_name(self, item_name):
        """Writes the items name to the data
        area.

        @param item_name: str representing the
        items name.

        @return: 2 tuple of (int, int) representing
        the row and column that it is safe to
        append more data to after this procedure.
        """
        format = self._get_item_name_format()
        self.write_data(item_name, format=format)
        return self.row + 1, self.col

    def _get_item_name_format(self):
        """Gets the format associated with the
        item name.

        @return: xlsxwriter.Format that represents
        the format for the name data.
        """
        return self.format_dict['item_data_format_left']

    def _write_item_price(self, item_price):
        """Writes the items price data to the
        data area.

        @param item_price: float representing
        the items price.

        @return:2 tuple of (int, int) representing
        the row and column that it is safe to
        append more data to after this procedure.
        """
        format = self._get_item_price_format()
        self.write_data(item_price, col=self.area_end_col, format=format)
        return self.row + 1, self.col

    def _get_item_price_format(self):
        """Gets the format for the item price.

        @return: xlsxwriter.Format that represents
        the format for the price to be written.
        """
        return self.format_dict['total_data_format']

    def _write_item_stars(self, item_stars):
        """Writes the item stars data to the
        data area.

        @param item_stars: int representing the
        number of stars associated with the item.

        @return:2 tuple of (int, int) representing
        the row and column that it is safe to
        append more data to after this procedure.
        """
        self._write_item_stars_name()
        self._write_item_stars_value(item_stars)
        return self.row + 1, self.col

    def _write_item_stars_name(self):
        """Writes the item stars name data.

        @return: None
        """
        format = self._get_item_stars_name_format()
        self.write_data('stars', format=format)

    def _get_item_stars_name_format(self):
        """Gets the format associated with the
        item stars name.

        @return: xlsxwriter.Format that represents
        the format for displaying the item stars name.
        """
        return self.format_dict['subitem_data_format_left']

    def _write_item_stars_value(self, value):
        """Writes the item stars value to the
        data area.

        @param value: int representing the stars
        value.

        @return: None
        """
        format = self._get_item_stars_value_format()
        self.write_data(value, col=self.col + 1, format=format)

    def _get_item_stars_value_format(self):
        """Gets the format for displaying the
        item stars value.

        @return: xlsxwriter.Format that represents
        the format to display the item stars value.
        """
        return self.format_dict['subitem_data_format_center']

    def _write_item_options(self, item_options):
        """Writes the item options to the data area.

        @param item_options: list of OptionItem
        objects that represents the options to be
        written to the data area.

        @return:2 tuple of (int, int) representing
        the row and column that it is safe to
        append more data to after this procedure.
        """
        col = self.col + 1
        row_counter = self.row

        self._write_item_options_title()

        for item in item_options:
            name = item.get_name()
            price = item.get_price()

            format = self._get_item_option_name_format()
            self.write_data(name, row=row_counter, col=col,
                            format=format)

            format = self._get_item_option_price_format()
            self.write_data(price, row=row_counter, col=self.area_end_col,
                            format=format)

            row_counter += 1

        return row_counter, self.col

    def _write_item_options_title(self):
        """Writes the item options title to
        the data area.

        @return: None
        """
        format = self._get_item_options_title_format()
        self.write_data('options', format=format)

    def _get_item_options_title_format(self):
        """Gets the format associated with the
        item options title.

        @return: xlsxwriter.Format that is used
        to display the item options title.
        """
        return self.format_dict['subitem_data_format_left']

    def _get_item_option_name_format(self):
        """Gets the format that is used to
        display the item options name

        @return: xlsxwriter.Format that represents
        the format to display the item options name.
        """
        return self.format_dict['subitem_data_format_center']

    def _get_item_option_price_format(self):
        """Gets the format that is used to
        display the item option price.

        @return: xlsxwriter.Format that is used
        to display the item option price.
        """
        return self.format_dict['subitem_data_total_format']

    def _write_item_note(self, item_note):
        """Writes the item note data to the
        data area.

        @param item_note: str representing the
        note associated with the item

        @return:2 tuple of (int, int) representing
        the row and column that it is safe to
        append more data to after this procedure.
        """
        self._write_item_note_title()
        self._write_item_note_data(item_note)

        return self.row + 1, self.col

    def _write_item_note_title(self):
        """Writes the item note title to the
        data area.

        @return: None
        """
        format = self._get_item_note_title_format()
        self.write_data('note', format=format)

    def _get_item_note_title_format(self):
        """Gets the format used to display
        the item note title.

        @return: xlsxwriter.Format that is
        used to display the item note title.
        """
        return self.format_dict['subitem_data_format_left']

    def _write_item_note_data(self, data):
        """Writes the item note data to the
        data area.

        @param data: str representing the item
        note data to be written.

        @return: None
        """
        format = self._get_item_note_data_format()
        self.write_data(data, col=self.col + 1, format=format)

    def _get_item_note_data_format(self):
        """Gets the format used to display
        the item note data.

        @return: xlsxwriter.Format that is used
        to display the item note data.
        """
        return self.format_dict['subitem_data_format_center']


class FrequencyArea(SpreadsheetArea):
    """FrequencyArea represents a general
    area that can be added to the Datesheet. This area is
    used to displaying item frequency data.

    @var date: datetime.datetime object representing
    the date that this item frequency area should be
    associated with.

    @var item_data: Counter that represents the number of
    times any given item was ordered. Each key is a str
    representing the item, which is mapped to values that
    represent the number of item orders.

    @var total_num_of_elements: float representing the
    total number of items ordered. This is used in generating
    the frequency data.

    @var freq_data: Counter that represents the frequency
    of an item being ordered. Each key is a str representing
    an item, which is mapped to values that represent the
    frequency of the item.

    @var freq_total: float representing the total value of
    all frequency values summed.

    @var freq_error: float representing how close of an
    approximation the frequency can be considered.
    """
    NUM_OF_SUBTOTAL_ROWS = 1

    def __init__(self, curr_date, item_data, format_dict):
        """Initializes the area with the given data.

        @param curr_date: datetime.datetime object
        representing the associated datetime for the
        area.

        @param item_data: Counter that maps str that
        represent items to int that represent the number
        of occurrences.

        @param format_dict: dict that maps str that
        represent the format names to xlsxwriter.Format
        objects.
        """
        self.date = curr_date
        self.item_data = Counter()
        self.total_num_of_elements = 0.0
        self._update_item_data(item_data)

        self.freq_data = Counter()
        self.freq_total = 0.0
        self.freq_error = 0.0
        self._update_freq_data()

        super(FrequencyArea, self).__init__(format_dict)

    @property
    def data_area_start(self):
        """Override Method

        Gets the int representing
        the row that the data area starts
        on.

        @return: int representing the
        data area start row.
        """
        change_in_rows = self.NUM_OF_SUBTOTAL_ROWS - \
                         super(FrequencyArea, self).NUM_OF_SUBTOTAL_ROWS

        return self._DATA_AREA_START + change_in_rows

    def _update_item_data(self, item_data):
        """Updates the stored item data.

        @param item_data: Counter object that
        represents the data to be updated.

        @return: None
        """
        self.item_data += item_data
        self.total_num_of_elements += self._get_total_num_of_elements(item_data)

    def _update_freq_data(self):
        """Updates the stored frequency data.

        @return: None
        """
        self.freq_data = self._make_freq_data()
        self.freq_total = self._get_freq_total(self.freq_data)
        self.freq_error = self._get_freq_error(self.freq_total)

    def _make_freq_data(self):
        """Makes the frequency data from
        other stored data.

        @return: Counter representing the
        frequency data.
        """
        data = Counter()

        for item_name, item_count in self.item_data.most_common():
            data[item_name] = round(item_count / self.total_num_of_elements, 2)

        return data

    @staticmethod
    def _get_freq_total(freq_data):
        """Gets the total sum values
        stored in the given frequency
        data values.

        @param freq_data: Counter that has
        frequencies for the values.

        @return: float representing the sum
        of all those frequencies.
        """
        return float(sum(freq_data.values()))

    @staticmethod
    def _get_freq_error(freq_total):
        """Gets the error associated with
        the frequency total.

        @param freq_total: float representing
        the frequency total.

        @return: float representing the error
        of the frequency total.
        """
        # simple error
        return 1.00 - freq_total

    @staticmethod
    def _get_total_num_of_elements(freq_data):
        """Gets the total number of elements
        in the given data.

        @param freq_data: Counter representing
        the data to have its elements counted.

        @return: float number representing the
        total number of elements in the given
        data.
        """
        return float(len(list(freq_data.elements())))

    def connect(self, worksheet):
        """Override Method

        Connects the area to the
        given worksheet.

        @param worksheet: xlsxwriter.worksheet.Worksheet
        object that represents the worksheet
        that the area will be added to.

        @return: 2 tuple of (int, int) representing
        the row and column that is the upper right
        hand boundary of the area. This is where it
        would be safe to add a new area.
        """
        values = super(FrequencyArea, self).connect(worksheet)

        self.update_header_data()
        self._write_item_frequency_data()

        return values

    def update_header_data(self):
        """Updates the header data for the
        area.

        @return: None
        """
        self.update_title_data()
        self.update_total_data()

    def update_title_data(self):
        """Override Method.

        Updates the title data for the
        area.

        @return: None
        """
        name = 'Item Frequency for {}'.format(self.date)

        super(FrequencyArea, self).update_title_data(name, self.date)

    def update_total_data(self):
        """Override method.

        Updates the total data for the
        area.

        @return: None
        """
        total_data = self._get_total_data()
        subtotal_data = self._get_subtotal_data()

        super(FrequencyArea, self).update_total_data(total_data,
                                                                     subtotal_data)

    def _get_total_data(self):
        """Get the total data for the
        area.

        @return: tuple where each entry
        is a (str, int) representing the
        total name and the total data to
        be displayed.
        """
        return ('Total Frequency', self.freq_total),

    def _get_format_total_data(self):
        """Override Method.

        Gets the format to be used for
        the total data.

        @return: xlsxwriter.Format that
        is to be used to display the
        total data.
        """
        return self.format_dict['title_format_right']

    def _get_subtotal_data(self):
        """Get the subtotal data to
        be added to the area.

        @return: tuple where each entry
        is a (str, int) representing the
        subtotal name and subtotal data
        to be displayed in the area.
        """
        return ('Frequency Error', self.freq_error),

    def _get_format_subtotal_data(self):
        """Override Method

        Gets the subtotal data format that
        will be used to display the subtotal
        data.

        @return: xlsxwriter.Format that is
        used to display the subtotal data.
        """
        return self.format_dict['subtitle_format_right']

    def add(self, item_data):
        """Override Method.

        Adds the item data to the
        frequency area.

        @param item_data: Counter representing
        the item data to be updated. This item
        data should be in standard str to int
        representing number of orders form.

        @return: None
        """
        self._update_item_data(item_data)
        self._update_freq_data()

        self.update_header_data()
        self._write_item_frequency_data

    def _write_item_frequency_data(self):
        """Writes the item frequency data to
        the data area.

        @note: This method rewrites all stored
        frequency data and should be used sparingly.
        This is because once frequency data is updated
        all potential frequencies may change.

        @return: None
        """
        self.row = self.data_area_start

        for item_name, freq_value in self.freq_data.most_common():
            self._write_item_name(item_name)
            self._write_item_data(freq_value)
            self.row += 1

    def _write_item_name(self, item_name):
        """Writes the item name to the data area.

        @param item_name: str representing the
        name of the item to have its frequency
        displayed.

        @return: None
        """
        format = self._get_item_name_format()
        self.write_data(item_name, format=format)

    def _get_item_name_format(self):
        """Gets the format for displaying
        the item name.

        @return: xlsxwriter.Format that
        represents the format to be displayed.
        """
        return self.format_dict['item_data_format_left']

    def _write_item_data(self, value):
        """Writes the item value to the
        data area.

        @param value: int representing
        the item data to be displayed.

        @return: None
        """
        format = self._get_item_data_format()
        self.write_data(value, col=self.area_end_col, format=format)

    def _get_item_data_format(self):
        """Gets the format for displaying
        the item data.

        @return: xlsxwriter.Format object
        representing the format used to
        display the item data.
        """
        return self.format_dict['item_data_format_right']


class NotificationArea(SpreadsheetArea):
    """

    """

    def __init__(self, date_data, notification_data, format_dict):
        """

        @param date_data:
        @param notification_data:
        @param format_dict:
        @return:
        """
        self.date = date_data
        self.data = notification_data

        self.num_of_discounts = 0
        self.num_of_comps = 0

        super(NotificationArea, self).__init__(format_dict)

    def update_title_data(self):
        """Override Method.

        @return:
        """
        title = 'Notification Items on {}'.format(self.date)
        super(NotificationArea, self).update_title_data(title, self.date)

    def update_total_data(self):
        """Override Method.

        @return:
        """
        totals_data = self._get_totals_data()
        subtotals_data = self._get_subtotals_data()
        super(NotificationArea, self).update_total_data(totals_data, subtotals_data)

    def _get_totals_data(self):
        """

        @return:
        """
        return ('Total items', len(self.data)),

    def _get_subtotals_data(self):
        """

        @return:
        """
        return (('Discount Items Total', self.num_of_discounts),
                ('Comped Items Total', self.num_of_comps))

    def connect(self, worksheet):
        """

        @param worksheet:
        @return:
        """
        values = super(NotificationArea, self).connect(worksheet)
        self.update_title_data()

        for menu_item in self.data:
            print menu_item
            print menu_item.get_price()
            self._add_item_data(menu_item)

        self.update_total_data()

        return values

    def _write_item_data(self, menu_item):
        """

        @param menu_item:
        @return:
        """
        self._write_item_data_name(menu_item.get_name())
        self._write_item_data_price(menu_item.get_price())

    def _write_item_data_name(self, item_name):
        """

        @param item_name:
        @return:
        """
        format = self._get_item_data_name_format()
        self.write_data(item_name, format=format)

    def _get_item_data_name_format(self):
        """

        @return:
        """
        return self.format_dict['item_data_format_left']

    def _write_item_data_price(self, item_price):
        """

        @param item_price:
        @return:
        """
        format = self._get_item_data_price_format()
        self.write_data(item_price, col=self.area_end_col, format=format)

    def _get_item_data_price_format(self):
        """

        @return:
        """
        return self.format_dict['total_data_format']

    def add(self, notification_item):
        """

        @param notification_item:
        @return:
        """
        self._add_item_data(notification_item)
        self.update_total_data()

    def _add_item_data(self, item):
        """

        @param item:
        @return:
        """
        self._write_item_data(item)
        self.row += 1

    def _add_item_data_type(self, item):
        try:
            if is_discount_item(item):
                self.num_of_discounts += 1
        except ValueError:
            self.num_of_comps += 1

        finally:
            self.data.append(item)


class OverviewArea(SpreadsheetArea):
    """OverviewArea represents an area that is
    used to display all a general overview of
    all of the orders that were made on the
    a given date.

    @var date: datetime.date representing the
    current date associated with the Overview
    area.

    @var date_totals: float representing the
    sum total of all orders totals displayed
    in the data area of the OverviewArea.

    @var date_subtotals: float representing
    the sum total of all orders subtotals
    displayed in the data area of the
    OverviewArea.

    @var date_tax: float representing the
    sum total of all orders tax displayed
    in the data area of the OverviewArea

    @var togo_orders: int representing the
    number of togo orders that are displayed
    in the data area of the OverviewArea.

    @var standard_orders: int representing
    the number of standard orders that are
    displayed in the data area of the
    OverviewArea.
    """

    NUM_OF_SUBTOTAL_ROWS = 4

    def __init__(self, date_data, format_dict):
        """Initializes the OverviewArea with the
        given date and format data.
        """
        self.date = date_data
        self.date_totals = 0.0
        self.date_subtotals = 0.0
        self.date_tax = 0.0

        self.togo_orders = 0
        self.standard_orders = 0
        super(OverviewArea, self).__init__(format_dict)

    @property
    def data_area_start(self):
        """Override Property.

        Gets the int representing the
        row where the data area begins.

        @return: int representing the row
        where the data area begins.
        """
        change_in_row = self.NUM_OF_SUBTOTAL_ROWS - \
                        super(OverviewArea, self).NUM_OF_SUBTOTAL_ROWS

        return self._DATA_AREA_START + change_in_row

    def connect(self, worksheet):
        """Override Method

        Connects the area to the given
        worksheet. Once linked these
        areas are considered coupled.

        @param worksheet: xlsxwriter.worksheet.Worksheet
        that represents the worksheet
        that this area will be written
        to.

        @return: 2 tuple of (int, int) representing
        the row and column that it is safe to add
        another area too.
        """
        values = super(OverviewArea, self).connect(worksheet)
        self.update_title_data()
        return values

    def update_title_data(self):
        """Override Method

        Updates the title data area.

        @return: None
        """
        title = 'Order Data for ' + str(self.date)
        super(OverviewArea, self).update_title_data(title, self.date)

    def update_total_data(self):
        """Override Method.

        Updates the total data area.

        @return: None
        """
        total_data = self._get_total_data()
        subtotal_data = self._get_subtotal_data()
        super(OverviewArea, self).update_total_data(total_data, subtotal_data)
        self.update_type_data()

    def update_type_data(self):
        """Updates the type data area.

        @return: None
        """
        type_data = self._get_type_data()
        self._write_type_data(type_data)

    def _write_type_data(self, type_data):
        """Writes the data to the type
        data area.

        @return: None
        """
        curr_row = super(OverviewArea, self).data_area_start
        for type_name, type_value in type_data:

            format = self._get_type_data_name_format()
            self.write_data(type_name, row=curr_row, format=format)

            format = self._get_type_data_value_format()
            self.write_data(type_value, row=curr_row, col=self.area_end_col,
                            format=format)

            curr_row += 1

    def _get_type_data_name_format(self):
        """Gets the format for displaying
        the type name in the total area.

        @return: xlsxwriter.Format that
        represents the display for the
        type name in the total area.
        """
        return self.format_dict['subtitle_format_left']

    def _get_type_data_value_format(self):
        """Gets the format used to display
        the type value in the total area.

        @return: xlsxwriter.Format that is
        used to display the type value in
        the total area.
        """
        return self.format_dict['subtitle_format_right']

    def _get_total_data(self):
        """Gets the total data to display.

        @return: tuple where each entry is
        (str, float) representing the total
        name and total data to be displayed,
        respectively.
        """
        return ('Total', self.date_totals),

    def _get_subtotal_data(self):
        """Gets the subtotal data to
        be displayed.

        @return: tuple where each entry
        is (str, float) representing the
        subtotal name and subtotal data
        to be displayed.
        """
        return (
            ('tax', self.date_tax),
            ('subtotal', self.date_subtotals),
        )

    def _get_type_data(self):
        """Gets the type data to be
        displayed.

        @return: tuple where each entry
        is (str, int) representing the
        type name and the type data to
        be displayed.
        """
        return (
            ('standard orders', self.standard_orders),
            ('togo orders', self.togo_orders)
        )

    def add(self, packaged_order):
        """Override Method

        Adds the packaged_order data
        to the data area.

        @param packaged_order: PackagedOrderData
        object that represents the order data to
        be added to the area.

        @return: None
        """
        self._update_overview_data(packaged_order)
        self.update_total_data()
        self._write_order_data(packaged_order)

    def _update_overview_data(self, packaged_order):
        """Updates the overview data which is used
        to store both totals and type data.

        @param packaged_order: PackagedOrderData
        object that represents the the data to
        update with.

        @return: None
        """
        self._update_overview_data_totals(packaged_order.totals)
        self._update_overview_data_type(packaged_order)

    def _update_overview_data_totals(self, totals_data):
        """Updates the overview data's stored totals.

        @param totals_data: dict of str to values
        where each key that represents the total type
        is mapped to a value that represents the total.

        Expected values are:

            'total'     :   float representing order total data
            'tax'       :   float representing order tax data
            'subtotal   :   float representing the order subtotal data.

        @return: 3 tuple of (float, float, float) representing the
        total, tax and subtotal data respectively.
        """
        self.date_totals += totals_data['total']
        self.date_tax += totals_data['tax']
        self.date_subtotals += totals_data['subtotal']

        return self.date_totals, self.date_tax, self.date_subtotals

    def _update_overview_data_type(self, packaged_order):
        """Updates the stored overview data's type data.

        @param packaged_order: PackagedOrderData that
        represents the data to be used to update the
        stored data.

        @return: None
        """
        self.standard_orders += packaged_order.is_standard
        self.togo_orders += packaged_order.is_togo

    def _write_order_data(self, packaged_order):
        """Writes the order data to the data area.

        @return: 2 tuple of (int, int) representing
        the row and column that it is safe to add
        data.
        """
        self._write_order_data_name(packaged_order.name)
        self._write_order_data_total(packaged_order.totals['total'])

        self.row += 1

        return self.row, self.col

    def _write_order_data_name(self, order_name):
        """Writes the order name to the data area.

        @param order_name: str representing the
        order name to be written.

        @return: None
        """
        format = self._get_order_data_name_format()
        self.write_data(order_name, format=format)

    def _get_order_data_name_format(self):
        """Gets the format for displaying
        the order name in the data area.

        @return: xlsxwriter.Format that is
        used to display the order name in the
        data area.
        """
        return self.format_dict['item_data_format_left']

    def _write_order_data_total(self, total):
        """Writes the order total in the data
        area.

        @return: None
        """
        format = self._get_order_data_total_format()
        self.write_data(total, col=self.area_end_col, format=format)

    def _get_order_data_total_format(self):
        """Gets the format for displaying the
        order total in the data area.

        @return: xlsxwriter.Format that is
        used to display the order total.
        """
        return self.format_dict['total_data_format']