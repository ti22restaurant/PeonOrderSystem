"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from .abc.GeneralArea import GeneralArea
from src.peonordersystem.MenuItem import is_menu_item
from src.peonordersystem.CheckOperations import (get_order_subtotal,
                                                 get_total_tax,
                                                 get_total)


class OrderArea(GeneralArea):
    """OrderArea represents a general
    order that is described through a OrderDataBundle
    object and stores information regarding a single order.

    This order area is used to parse and display data from
    the OrderDataBundle.

    @var: packaged_data: OrderDataBundle information that
    this area should display.
    """

    def __init__(self, packaged_data):
        """Initializes the OrderArea
        object with the packaged data.

        @param packaged_data: OrderDataBundle object
        that represents the order areas data.
        """
        self.packaged_data = packaged_data
        super(OrderArea, self).__init__()

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
        return ('total', self.packaged_data.total),

    def _get_subtotal_data(self):
        """Gets the subtotal data stored in this
        areas packaged data.

        @return: tuple where each entry represents the
        (str, float) where the values are the subtotal name
        and the subtotal data respectively.
        """
        return (
            ('tax', self.packaged_data.tax),
            ('subtotal', self.packaged_data.subtotal)
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

        self.packaged_data.total += total
        self.packaged_data.tax += tax
        self.packaged_data.subtotal += subtotal

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
        return self.format_data['item_data_format_left']

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
        return self.format_data['total_data_format']

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
        return self.format_data['subitem_data_format_left']

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
        return self.format_data['subitem_data_format_center']

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
        return self.format_data['subitem_data_format_left']

    def _get_item_option_name_format(self):
        """Gets the format that is used to
        display the item options name

        @return: xlsxwriter.Format that represents
        the format to display the item options name.
        """
        return self.format_data['subitem_data_format_center']

    def _get_item_option_price_format(self):
        """Gets the format that is used to
        display the item option price.

        @return: xlsxwriter.Format that is used
        to display the item option price.
        """
        return self.format_data['subitem_data_total_format']

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
        return self.format_data['subitem_data_format_left']

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
        return self.format_data['subitem_data_format_center']

    def finalize(self):
        """Finalizes the area.

        @return: None
        """
        self.update_total_data()