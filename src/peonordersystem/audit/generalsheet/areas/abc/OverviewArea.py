"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from abc import ABCMeta, abstractmethod
from src.peonordersystem.audit.generalsheet.areas.abc.GeneralArea import GeneralArea


class OverviewArea(GeneralArea):
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

    __metaclass__ = ABCMeta

    def __init__(self):
        """Initializes the OverviewArea with the
        given date and format data.
        """
        self.date_totals = 0.0
        self.date_subtotals = 0.0
        self.date_tax = 0.0

        self.togo_orders = 0
        self.standard_orders = 0
        super(OverviewArea, self).__init__()

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

    def connect(self, worksheet, format_data, **kwargs):
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
        values = super(OverviewArea, self).connect(worksheet, format_data, **kwargs)
        self.update_title_data()
        return values

    def update_title_data(self):
        """Override Method

        Updates the title data area.

        @return: None
        """
        title = self._get_title_data()
        super(OverviewArea, self).update_title_data(title, self.date)

    @abstractmethod
    def _get_title_data(self):
        """

        @return:
        """
        pass

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
        return self.format_data['subtitle_format_left']

    def _get_type_data_value_format(self):
        """Gets the format used to display
        the type value in the total area.

        @return: xlsxwriter.Format that is
        used to display the type value in
        the total area.
        """
        return self.format_data['subtitle_format_right']

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
        self._check_date(packaged_order.date)
        self._update_overview_data(packaged_order)
        self.update_total_data()
        self._write_order_data(packaged_order)

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
            raise ValueError('Expected all values to be in the on ' + \
                             ' the same date. Some values within ' + \
                             ' the given packaged order data were' + \
                             ' not.')

        return True

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
        return self.format_data['item_data_format_left']

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
        return self.format_data['total_data_format']