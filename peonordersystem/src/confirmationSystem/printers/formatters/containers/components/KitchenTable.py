"""This module defines the KitcheTable
that is used to display menu items to
the kitchen.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.TableComponent import TableComponent

from reportlab.platypus import Table, Paragraph


class KitchenTable(TableComponent):
    """Generates a table that is used
    for displaying items to the kitchen.
    """
    OPTION_FORMAT = '{option}<br/>'
    NAME_SIZE = 12

    def __init__(self, items_data):
        """Initializes the KitchenTable
        with the given data.

        @param items_data: list of MenuItem
        objects that represents the data to
        be generated for display to the kitchen.
        """
        self._item_number = 0
        self._item_rows = 0

        self._option_rows = 0

        self.sub_table_col_width = [45] + [self.DEFAULT_TABLE_COL_WIDTH[1] - 45]

        super(KitchenTable, self).__init__(items_data)

    @property
    def height(self):
        """Gets the height value that
        represents the height necessary
        for the table.

        @return: int representing the
        height.
        """
        return self._item_rows * self.NAME_SIZE + self._option_rows * self.SUB_SIZE

    def generate_tables(self, data):
        """Generates the tables that
        are used to display.

        @param data: list of MenuItem
        objects that represents the
        data that will be used to
        generate the tables.

        @return: reportlab.platypus.Table
        that stores the given data for
        display.
        """
        rows = []

        for item in data:
            row = self._create_item_row(item)
            rows.append(row)
            row = self._create_option_row(item)
            rows.append(row)

        table = Table(rows, colWidths=self.DEFAULT_TABLE_COL_WIDTH,
                      style=self.DEFAULT_TABLE_STYLE)

        self.add_table(table)

    def _create_item_row(self, item):
        """Creates the row for the
        given item.

        @param item: MenuItem that
        is to have a row int he table
        generated for it.

        @return: list of objects
        representing the items row
        in the table.
        """
        row = []

        self._item_number += 1
        self._item_rows += 1

        text = self.NUMBER_FORMAT.format(number=self._item_number)
        p_num = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_num)

        text = self.MAIN_FORMAT.format(data=item.get_name())
        p_name = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_name)

        return row

    def _create_option_row(self, item):
        """Creates the row for the options
        of the given item.

        @param item: MenuItem object that
        is to have its option data retrieved

        @return: list of objects
        representing the options
        row in the table.
        """
        row = ['']

        self._item_rows += 1

        table = self._create_option_table(item)
        row.append(table)

        return row

    def _create_option_table(self, item):
        """Creates the options table
        that is a nested table that
        displays a given items option data.

        @param item: MenuItem object that is
        to have the options sub-table
        generated.

        @return: reportlab.platypus.Table that
        represents the table used for displaying
        the options data.
        """
        data = []

        if item.has_stars():
            stars_row = self._create_stars_row(item.stars)
            data.append(stars_row)

        if item.has_options():
            options_row = self._create_options_row(item.options)
            data.append(options_row)

        if item.has_note():
            notes_row = self._create_notes_row(item.notes)
            data.append(notes_row)

        return Table(data or [''],
                     colWidths=self.sub_table_col_width,
                     style=self.DEFAULT_TABLE_STYLE)

    def _create_stars_row(self, num):
        """Creates the row that displays
        the stars data.

        @param num: int representing the
        number of stars to be displayed.

        @return: list of objects that
        represents the row for the stars.
        """
        row = []

        text = self.SUB_FORMAT.format(data='stars: ')
        p_name = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_name)

        text = self.SUB_FORMAT.format(data=num)
        p_num = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_num)

        self._option_rows += 1

        return row

    def _create_options_row(self, options):
        """Creates the row that displays the
        options data.

        @param options: list of OptionItem
        objects representing the options
        to be displayed in this row.

        @return: list of objects representing
        the row of options.
        """
        row = []

        text = self.SUB_FORMAT.format(data='options: ')
        p_name = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_name)

        data = ''
        for option in options:
            self._option_rows += 1
            data += self.OPTION_FORMAT.format(option=option)

        text = self.SUB_FORMAT.format(data=data)
        p_opt = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_opt)

        # For fencepost problem of break
        self._option_rows += 1

        return row

    def _create_notes_row(self, note):
        """Creates the notes row that
        displays he notes data.

        @param note: str representing
        the note to be displayed.

        @return: list of objects
        representing the notes row.
        """
        row = []

        text = self.SUB_FORMAT.format(data='note: ')
        p_name = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_name)

        text = self.SUB_FORMAT.format(data=note)
        p_note = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_note)

        self._option_rows += (len(note) / 12) + 1

        return row