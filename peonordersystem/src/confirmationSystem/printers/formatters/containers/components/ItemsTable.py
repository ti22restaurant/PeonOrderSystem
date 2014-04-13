"""This module defines the ItemsTable
class which is used to generate the
display for items on the receipt.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from reportlab.platypus import Paragraph, Table

from peonordersystem.src.confirmationSystem.printers.formatters.PrinterSettings \
    import DEFAULT_FRONT_PRINTER_WIDTH

from .abc.Component import Component


class ItemsTable(Component):
    """Generates the display for
    MenuItems.
    """

    TABLE_SPAN_COLS = 1, 3

    DEFAULT_TABLE_STYLE = (
        ('SPAN', (TABLE_SPAN_COLS[0], 0), (TABLE_SPAN_COLS[1], 0)),
        ('LEFTPADDING', (0, 0), (-1, -1), -1),
        ('RIGHTPADDING', (0, 0), (-1, -1), -1)
    )

    DEFAULT_TABLE_COL_WIDTH = ([15] + 4 * [(DEFAULT_FRONT_PRINTER_WIDTH - 15) / 4])

    NUMBER_SIZE = 10

    NUMBER_FORMAT = """
        <para align=center size=%s>
            <super>{number}.</super>
        </para>
     """ % str(NUMBER_SIZE)

    ITEM_SIZE = 10

    ITEM_DATA_FORMAT = """
        <para align=left size=%s>
            <b>{data}</b>
        </para>
     """ % str(ITEM_SIZE)

    OPTION_SIZE = 9

    OPTION_DATA_FORMAT = """
        <para align=left leftIndent=10 size=%s>
            <i>{data}</i>
        </para>
    """ % str(OPTION_SIZE)

    def __init__(self, items_data):
        """Initializes the items table.

        @param items_data: list of MenuItem
        objects that represents the order to
        be displayed.
        """
        super(ItemsTable, self).__init__()

        # Stateful fields
        self._item_number = 0
        self._current_style = []

        self._item_rows = len(items_data)
        self._option_rows = 0

        self._generate_tables(items_data)

    @property
    def width(self):
        """Gets the width taken
        up by the components area.

        @return: float representing
        the width.
        """
        return self.DEFAULT_WIDTH

    @property
    def height(self):
        """Gets the height taken
        up by the components area.

        @return: float representing
        the height.
        """
        item_lines = self.ITEM_SIZE * self._item_rows
        option_lines = self.OPTION_SIZE * self._option_rows

        return (item_lines + option_lines) * self.ROW_SPACE_MULTIPLIER

    def _generate_tables(self, items):
        """Generates the tables for display.

        @param items: list of MenuItem objects
        that represents the data to generate
        from.

        @return: None
        """
        for item in items:
            table = self._generate_table(item)
            self._flowables.append(table)

    def _generate_table(self, item):
        """Generates a table for the
        given item.

        @param item: MenuItem object
        that a table is to be generated for

        @return: reportlab.platypus.Table
        object that represents the table
        associated with the given MenuItem
        """
        self._current_style = list(self.DEFAULT_TABLE_STYLE)

        item_rows = self._create_rows(item)
        return Table(item_rows, self.DEFAULT_TABLE_COL_WIDTH,
                     style=self._current_style)

    def _create_rows(self, item):
        """Creates the data rows for
        the given item.

        @param item: MenuItem object
        that is to have the data rows
        generated for it.

        @return: list of lists that
        hold objects representing the
        data rows for a table generated
        for the given MenuItem.
        """
        rows = []

        item_row = self._create_item_row(item)
        rows.append(item_row)

        for option in item.options:
            option_row = self._create_option_row(option)
            rows.append(option_row)

        return rows

    def _create_item_row(self, item):
        """Creates the item row for
        the given item.

        @param item: MenuItem object
        that is to have the main item
        row generated for it.

        @return: list of values
        representing the objects to
        display the MenuItems data.
        """
        row = []
        self._item_number += 1

        text = self.NUMBER_FORMAT.format(number=self._item_number)
        p_num = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_num)

        name = item.get_name()
        text = self.ITEM_DATA_FORMAT.format(data=name)
        p_name = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_name)

        # filler columns
        row.append('')
        row.append('')

        price = item.get_price()
        text = self.ITEM_DATA_FORMAT.format(data=price)
        p_price = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_price)

        return row

    def _create_option_row(self, option):
        """Creates the option row for the
        given options

        @param option: OptionItem that is
        to have display data generated for
        it.

        @return:list of values representing
        the row assocaited with the given
        OptionItem.
        """
        # initial filler column for item number
        row = ['']
        self._option_rows += 1
        self._update_style()

        name = option.get_name()
        text = self.OPTION_DATA_FORMAT.format(data=name)
        p_name = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_name)

        # filler columns
        row.append('')
        row.append('')

        price = option.get_price()
        text = self.OPTION_DATA_FORMAT.format(data=price)
        p_price = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        row.append(p_price)

        return row

    def _update_style(self):
        """Updates the table style to
        incorporate an additional item.

        @return: None
        """
        curr_row = len(self._current_style) - len(self.DEFAULT_TABLE_STYLE) + 1

        style_row = (
            'SPAN',
            (self.TABLE_SPAN_COLS[0], curr_row),
            (self.TABLE_SPAN_COLS[1], curr_row))

        self._current_style.append(style_row)