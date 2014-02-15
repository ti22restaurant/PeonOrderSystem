"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from collections import Counter
from .abc.GeneralArea import GeneralArea


class FrequencyArea(GeneralArea):
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

    def __init__(self, curr_date, item_data):
        """Initializes the area with the given data.

        @param curr_date: datetime.datetime object
        representing the associated datetime for the
        area.

        @param item_data: Counter that maps str that
        represent items to int that represent the number
        of occurrences.
        """
        self.date = curr_date
        self.item_data = Counter()
        self.total_num_of_elements = 0.0
        self._update_item_data(item_data)

        self.freq_data = Counter()
        self.freq_total = 0.0
        self.freq_error = 0.0
        self._update_freq_data()

        super(FrequencyArea, self).__init__()

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
            data[item_name] = round(item_count / self.total_num_of_elements, 4)

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
        return 1 - freq_total

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

        super(FrequencyArea, self).update_total_data(total_data, subtotal_data)

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
        return self.format_data['title_format_right']

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
        return self.format_data['subtitle_format_right']

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

        self._write_item_frequency_data()

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
        return self.format_data['item_data_format_left']

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
        return self.format_data['item_data_format_right']

    def finalize(self):
        """Finalizes the area.

        @return: None
        """
        self.update_header_data()