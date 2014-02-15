"""This module provides the functionality
for users to perform audits through the
Auditor object.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import os
from datetime import datetime, date, time

from src.peonordersystem.path import SYSTEM_AUDIT_PATH

from src.peonordersystem.Settings import FILENAME_TEMPLATE
from src.peonordersystem.Settings import AUDIT_FILE_TYPE

from src.peonordersystem.confirmationSystem.ConfirmationSystem \
    import get_stored_order_data

from AuditBuilder import AuditBuilder


class Auditor(object):
    """Allows users to perform audits
    by using predefined daily audit or
    giving associated dates and times
    over which to perform the audit.
    """

    CLOSING_AUDIT_FLAGS = {'auditsheet': False,
                           'audit_charts': False,
                           'stats_charts': False,
                           'datesheets': True,
                           'orders': True,
                           'frequency': True,
                           'notification': True,
                           'order_charts': True}

    DEFAULT_AUDIT_NAME = 'audit'
    DEFAULT_CLOSING_AUDIT_NAME = 'closing_' + DEFAULT_AUDIT_NAME

    def closing_audit(self):
        """Performs the standard closing audit
        which covers a single day. Whatever time
        is provided from date.today() will be the
        audited day.

        @return: None
        """
        curr_date = datetime.now()
        path = self._create_closing_audit_path()
        data = self._get_data()
        AuditBuilder(path, curr_date, curr_date, data, **self.CLOSING_AUDIT_FLAGS)

    def _create_closing_audit_path(self):
        """Creates the path associated with
        the closing audit.

        @return: str representing the closing audits
        path.
        """
        dirs = self._create_audit_dirs()
        file_name = self._standardize_file_name(self.DEFAULT_CLOSING_AUDIT_NAME,
                                                date.today(), date.today())
        return dirs + '/' + file_name

    @staticmethod
    def _create_audit_dirs():
        """Creates the necessary dirs
        to store the closing audit.

        @return: str representing the
        directory generated for the
        closing audit to be placed in.
        """
        curr_date = date.today()
        dirs = SYSTEM_AUDIT_PATH
        dirs += '/{}/{}/{}'.format(curr_date.year, curr_date.month, curr_date.day)
        if not os.path.exists(dirs):
            os.makedirs(dirs)
        return dirs

    def audit_range(self, start_datetime, end_datetime, **kwargs):
        """Creates an audit over the given data range with the
        given keywords.

        @param start_datetime: datetime.datetime object that
        represents the starting datetime for the audit. Data
        will be pulled over this range. Inclusive.

        @param end_datetime: datetime.datetime objec tthat
        represents the ending datetime for the audit. Data will
        be pulled over this range. Inclusive.

        @keyword kwargs: keyword arguments that represent the
        customization of the audits path, and audit flags that
        are used to customize audit data. Accepted keywords are:

         @keyword flags: Flags that are used in
        customizing what areas the auditbook
        will display. Accepted keywords are:

                'file_path'     :       str representing the
                                        full file path for the
                                        audit to be saved as.

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

        @return: None
        """
        if 'file_path' in kwargs:
            file_path = kwargs['file_path']
        else:
            file_path = self._create_path(start_datetime.date(), end_datetime.date())

        data = self._get_data((start_datetime, end_datetime))
        AuditBuilder(file_path, start_datetime, end_datetime, data, **kwargs)

    def _create_path(self, start_date, end_date):
        """Creates the path for the audit to be
        saved at.

        @param start_date: datetime.date that represents
        the starting date for the audit.

        @param end_date: datetime.date that represents the
        ending date for the audit.

        @return: str representing the path for the audit
        to be saved at.
        """
        file_name = self._standardize_file_name(self.DEFAULT_AUDIT_NAME,
                                                start_date, end_date)
        return SYSTEM_AUDIT_PATH + '/' + file_name

    @staticmethod
    def _standardize_file_name(file_name, start_date, end_date):
        """Standardizes the file name for the audit.

        @param file_name: str representing the name that
        should be associated with this file name.

        @param start_date: datetime.date that represents
        the start date for the audit.

        @param end_date: datetime.date that represents
        the end date for the audit.

        @return: str representing the file name for the
        audit.
        """
        date_str = str(start_date) + ', ' + str(end_date)
        data = {'name': file_name,
                'timestamp': date_str,
                'file_type': AUDIT_FILE_TYPE}
        return FILENAME_TEMPLATE.format(**data)

    @staticmethod
    def _get_data(dates=None):
        """Gets the data that is to
        be displayed over the given dates.

        @keyword dates: tuple of datetime.datetime
        objects that represents the data range to
        retrieve the data from. Default is today
        for both start and end.

        @return: Generator object that yields
        OrderDataBundle objects that represent
        rows of data in sorted order by date.
        """
        if dates:
            start_date, end_date = dates
        else:
            start_date = datetime.combine(date.today(), time.min)
            end_date = datetime.combine(date.today(), time.max)
        generator = get_stored_order_data(start_date, end_date)
        return generator
