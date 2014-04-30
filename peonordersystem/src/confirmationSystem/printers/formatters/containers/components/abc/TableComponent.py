"""This module provides the abstract base
class for the TableComponent.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractproperty, abstractmethod

from .Component import Component

from peonordersystem.src.confirmationSystem.printers.formatters.PrinterSettings \
    import DEFAULT_FRONT_PRINTER_WIDTH


class TableComponent(Component):
    """This class describes the
    required functionality for an
    object to be a useable TableComponent.
    """

    __metaclass__ = ABCMeta

    DEFAULT_TABLE_STYLE = (
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0)
    )

    FIRST_COL_WIDTH = 15
    DEFAULT_TABLE_COL_WIDTH = ([FIRST_COL_WIDTH] +
                               [DEFAULT_FRONT_PRINTER_WIDTH - FIRST_COL_WIDTH])

    NUMBER_SIZE = 10
    NUMBER_FORMAT = """
        <para align=center size=%s>
            <super>{number}.</super>
        </para>
    """ % str(NUMBER_SIZE)

    MAIN_SIZE = 10
    MAIN_FORMAT = """
        <para align=left size=%s>
            <b>{data}</b>
        </para>
    """ % str(MAIN_SIZE)

    SUB_SIZE = 9
    SUB_FORMAT = """
        <para align=left leftIndent=10 size=%s>
            <i>{data}</i>
        </para>
    """ % str(SUB_SIZE)

    def __init__(self, data):
        """Initializes the TableComponent.

        @param data: data to be passed to
        the generate_tables method.
        """
        super(TableComponent, self).__init__()
        self.generate_tables(data)

    @property
    def width(self):
        """Gets the width associated
        with the table.

        @return: float representing the
        width of the table.
        """
        return self.DEFAULT_WIDTH

    @abstractproperty
    def height(self):
        """Gets the height associated
        with the table.

        @return: float representing the
        height of the table.
        """
        pass

    @abstractmethod
    def generate_tables(self, data):
        """Generates the tables for
        display.

        @param data: data that is to
        be used in generating the tables.

        @return: None
        """
        pass

    def add_table(self, table):
        """Adds the given table
        to the stored flowables
        for access by exterior
        objects.

        @param table: reportlab.platypus.Table
        class that is to be added to the
        stored flowables.

        @return: None
        """
        self._flowables.append(table)
