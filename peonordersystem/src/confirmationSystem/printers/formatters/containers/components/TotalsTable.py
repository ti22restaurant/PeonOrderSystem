"""This module defines the TotalsTable
class that is used to generate the
display for showing totals associated
with a receipt.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from reportlab.platypus import Paragraph, Table, TableStyle

from .abc.Component import Component


class TotalsTable(Component):
    """TotalsTable is used for generating
    a table for displaying the totals with
    an associated order and displaying on
    a receipt.
    """
    TOTAL_SIZE = 12
    TOTAL_LINES = 1

    TOTAL_FORMAT = """
        <para align=left size=%s>
            <b>{data}</b>
        </para>
    """ % str(TOTAL_SIZE)

    SUBTOTAL_SIZE = 8
    SUBTOTAL_LINES = 2

    SUBTOTAL_FORMAT = """
        <para align=left size=%s>
            <i>{data}</i>
        </para>
    """ % str(SUBTOTAL_SIZE)

    TABLE_STYLE = TableStyle(
        [
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0)
        ]
    )

    NUM_OF_LINES = 3

    def __init__(self, total_data):
        """Initializes the TotalsTable.

        @param total_data: dict of values
        containing the following key value
        pairs:

            'subtotal'  :   float representing the subtotal
            'tax'       :   float representing the tax.
            'total'     :   float representing the total.
        """
        super(TotalsTable, self).__init__()
        self._generate_tables(total_data)

    @property
    def height(self):
        """Gets the height associated
        with this component.

        @return: float representing the
        height of this component.
        """
        total_lines = self.TOTAL_SIZE * self.TOTAL_LINES
        subtotal_lines = self.SUBTOTAL_LINES * self.SUBTOTAL_SIZE
        return (total_lines + subtotal_lines) * self.ROW_SPACE_MULTIPLIER

    @property
    def width(self):
        """Gets the width associated
        with this component.

        @return: float representing
        the width of this component.
        """
        return self.DEFAULT_WIDTH

    def _generate_tables(self, total_data):
        """Generates the total tables.

        @param total_data: dict which holds
        values associated with the totals.

        @return: None
        """
        data_rows = self._generate_rows(total_data)

        table = Table(data_rows, style=self.TABLE_STYLE)
        self._flowables.append(table)

    def _generate_rows(self, total_data):
        """Generates the data rows for
        display in the table.

        @param total_data: dict which holds
        values associated with the totals.

        @return: list of lists representing
        the data rows that were generated to
        be displayed in the table.
        """
        rows = []

        row = self._generate_row('subtotal: ', total_data['subtotal'],
                                 self.SUBTOTAL_FORMAT)
        rows.append(row)

        row = self._generate_row('tax: ', total_data['tax'], self.SUBTOTAL_FORMAT)
        rows.append(row)

        row = self._generate_row('total: ', total_data['total'], self.TOTAL_FORMAT)
        rows.append(row)

        return rows

    def _generate_row(self, title, total, frmt):
        """Generates the data row for a given
        total.

        @param title: str representing the
        title to display in the row.

        @param total_data: float representing
        the total to display in the row.

        @param frmt: str representing the format
        to for the data to take.

        @return: list of values representing the
        row generated.
        """
        data = []

        text = frmt.format(data=title)
        p_text = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        data.append(p_text)

        text = frmt.format(data=total)
        p_text = Paragraph(text, self.DEFAULT_PARAGRAPH_STYLE)
        data.append(p_text)

        return ['', '', ''] + data