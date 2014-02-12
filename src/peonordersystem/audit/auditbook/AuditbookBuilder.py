"""This module defines the buider used
for generating an audit book.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from .abc.Builder import Builder
from .creators.generalsheet.GeneralsheetCreator import GeneralsheetCreator
from .creators.auditsheet.AuditsheetCreator import AuditsheetCreator


class AuditbookBuilder(Builder):
    """This class controls and operates
    an AuditBook that spans the given
    dates, and is updated with the given
    data.
    """

    def __init__(self, workbook_name, start_date, end_date, **flags):
        """Initializes the builder.

        @param workbook_name: str representing the name that should
        be associated with this workbook.

        @param start_date: datetime.date that representing the
        starting date of the audit.

        @param end_date: datetime.date that represents the end
        date of the audit.

        @param flags: keyword arguments that allow for
        customization of the operation of the audit. This
        allows users to control which areas will be generated
        or displayed. Accepted keywords are:

                'auditsheet'    :       bool value representing
                                        if the overall audit sheet
                                        that displays the totals
                                        over the entire audit
                                        should be generated.

                'audit_charts'  :       bool value representing if
                                        the audit charts that represent
                                        the total data in chart form
                                        over the entire audit should
                                        be generated.

                'stats_charts'  :       bool value representing if
                                        the stats charts that represent
                                        the total data in chart form
                                        over the entire audit but parsed
                                        into mean and median should be
                                        generated.

                'datesheets'    :       bool value representing
                                        if the unique datesheets
                                        for each date that display
                                        the descriptive information
                                        for each order should be
                                        generated.

                'orders'        :       bool value representing
                                        if the unique area for each
                                        order in the datesheet should
                                        be generated displaying descriptive
                                        information about any order.

                'frequency'     :       bool value representing if
                                        the frequency areas that display
                                        how often an item was ordered
                                        over the period should be generated.

                'notification'  :       bool value representing if
                                        the notification areas that display
                                        the notification items should
                                        be generated.

                'order_charts'  :       bool value representing if the
                                        charts that display the orders
                                        data for any given date should
                                        be generated.
        """
        super(AuditbookBuilder, self).__init__(workbook_name)

        self._start_date = start_date
        self._end_date = end_date

        self._auditsheet_container = None

        self._flags = self.__parse_flags(**flags)
        self._build_creators()

    def __parse_flags(self, **flags):
        """Parses the flags and sets up the
        defaults if no value was given.

        @keyword flags: keyword argument
        that represents the flags that
        are to be stored.

        @return: dict representing the
        parsed flags with all non-entries
        as default.
        """
        flags = {'stats_charts': True,
                 'order_charts': True,
                 'audit_charts': True,
                 'auditsheet': True,
                 'datesheets': True,
                 'orders': True,
                 'frequency': True,
                 'notification': True}

        flags.update(flags)
        return flags

    def _build_creators(self):
        """builds the creators which
        are used to generate the necessary
        areas.

        @return: None
        """
        self._set_up_creators()

    def _set_up_creators(self):
        """Sets up the creators

        @return: None
        """
        self._set_up_auditsheet_creator()
        self._set_up_datesheet_creator()

    def _set_up_datesheet_creator(self):
        """Sets up the datesheet creator.

        @return: None
        """
        creator = GeneralsheetCreator(self.workbook, **self._flags)
        self.add(creator)

    def _set_up_auditsheet_creator(self):
        """Sets up the auditsheet creator.

        @return: None
        """
        creator = AuditsheetCreator(self.workbook, self._start_date,
                                    self._end_date, **self._flags)
        self.add(creator)

    def finalize(self):
        """Finalizes the AuditBook.

        @return: None
        """
        super(AuditbookBuilder, self).finalize()
        self.workbook.close()

