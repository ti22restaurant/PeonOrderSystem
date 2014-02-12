"""This module defines the Auditor class
that is used to generate the auditbook.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from .auditbook.AuditbookBuilder import AuditbookBuilder


class Auditor(object):
    """Auditor class takes a filename
    and data and builds the auditbook
    from the given data.
    """

    def __init__(self, filename, data, **flags):
        """Initializes and creates the auditbook
        with the given data.

        @param filename: str representing the
        filename that the auditbook should be
        saved as.

        @param data: CollectionDataBundle of
        data that the auditbook should be
        generated from. The given data is
        expected to be in sorted order.

        @keyword flags: Flags that are used in
        customizing what areas the auditbook
        will display. Accepted keywords are:

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
        start_date = data[0].datetime
        end_date = data[-1].datetime
        self._data = data
        self._builder = AuditbookBuilder(filename, start_date, end_date, **flags)
        self._create_auditbook()

    def _create_auditbook(self):
        """Creates the auditbook

        @return: None
        """
        self._build_auditbook()
        self._finalize()

    def _build_auditbook(self):
        """Builds the auditbook

        @return: None
        """
        for data in self._data:
            self._builder.update(data)

    def _finalize(self):
        """Finalizes the auditbook.

        @return: None
        """
        self._builder.finalize()

