"""DataAudit module holds the necessary functions and
information for auditing previous orders and compiling
them into an xls document that is more human readable.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

from src.peonordersystem.ConfirmationSystem import parse_standardized_file_name
from src.peonordersystem import CheckOperations
from src.peonordersystem import path
from src.peonordersystem.CustomExceptions import InvalidDateRangeError
from src.peonordersystem.Settings import AUDIT_FILE_TYPE, \
    CLOSING_AUDIT_DEFAULT_NAME

from collections import Counter
from collections import deque
import jsonpickle
import datetime
import xlsxwriter
import time
import os

#================================================
# This block in the module generates and
# checks the necessary directories, as well as
# creates the module wide constants.
#================================================

ORDERS_DIRECTORY = path.SYSTEM_ORDERS_PATH
AUDIT_DIRECTORY = path.SYSTEM_AUDIT_PATH

TODAY_DIRECTORY = AUDIT_DIRECTORY

TODAYS_DATE = time.localtime()[:3]

for value in TODAYS_DATE:
    TODAY_DIRECTORY += "/{}".format(value)
    if not os.path.exists(TODAY_DIRECTORY):
        os.mkdir(TODAY_DIRECTORY)

REQUEST_DIRECTORY = AUDIT_DIRECTORY  + "/requests"

if not os.path.exists(REQUEST_DIRECTORY):
    os.mkdir(REQUEST_DIRECTORY)


BEGIN_COL = ord('A')
BEGIN_ROW = 0



def _check_dates(start_date, end_date):
    """Checks the given dates to see if
    they are within the acceptable range.

    @raise InvalidDateRangeError: if
    start_date > end_date.

    @param start_date: datetime.date
    object that represents the beginning
    date of the date range.

    @param end_date: datetime.date object
    that represents the ending date of
    the date range.

    @return: None
    """
    if start_date > end_date:
        raise InvalidDateRangeError(start_date, end_date)

def closing_audit():
    """Initiates a closing audit which generates
    the daily audit information and stores it in the
    specified audit area under the directory associated
    with the current date.

    @return: None
    """
    today = datetime.date(TODAYS_DATE[0], TODAYS_DATE[1], TODAYS_DATE[2])
    workbook = audit_data(today, today)

    closing_audit_filepath = TODAY_DIRECTORY + '/' + CLOSING_AUDIT_DEFAULT_NAME
    closing_audit_filepath = get_acceptable_filepath(closing_audit_filepath)
    workbook.save(closing_audit_filepath)


def request_audit(from_date, until_date, location=REQUEST_DIRECTORY,
                  name='Audit'):
    """Performs an audit over the selected date
    period.

    @param from_date: datetime.date object that represents
    the starting date that the audit should begin on, inclusive.

    @param until_date: datetime.date object that represents
    the ending date that the audit should conclude on, inclusive.

    @param name: str representing the name of the file that will
    be stored in the audit requests area.

    @return: None
    """
    str_date_range = '[' + str(from_date) + ',' + str(until_date) + ']'

    request_audit_filepath = location + '/' + name + str_date_range
    request_audit_filepath = get_acceptable_filepath(request_audit_filepath)

    workbook = audit_data(from_date, until_date, location + '/' + name)
    workbook.save(request_audit_filepath)


def get_acceptable_filepath(file_path):
    """checks if the given filepath is
    able to be used. Returns an updated file
    path that should be acceptable to be used
    without overwriting other files.

    @param file_path: str representing the
    entire file path that is to be checked.

    @return: str representing the updated file
    path.
    """
    counter = 1

    new_file_path = file_path.split('.')[0] + AUDIT_FILE_TYPE

    while os.path.exists(new_file_path):
        new_file_path = file_path.split('.')[0] + "(" + str(counter) + ")" + \
                        AUDIT_FILE_TYPE
        counter += 1

    return new_file_path


def _generate_day_data(worksheet, row, column, day_data):
    """

    @param worksheet:
    @param row:
    @param column:
    @param day_data:
    @return:
    """
    yield 'b'

def _generate_order_data(worksheet, row, column, order_data):
    """

    @param worksheet:
    @param row:
    @param column:
    @param order_data:
    @return:
    """
    pass


def _get_data(start_date, end_date):
    """Gets the data the data currently stored in
    the orders log area between the given start
    dates inclusive.

    @param start_date: datetime.date object that
    represents hte stored date that will be the
    beginning point.

    @param end_date: datetime.date object that
    represents the stored date that will be the
    ending point.

    @return: dict of str keys that represent the
    filename associated with the data, and are mapped
    to values which are lists of MenuItems that represent
    the order specified by the key.
    """
    _check_dates(start_date, end_date)

    data = {}

    curr_date = start_date
    while curr_date <= end_date:
        data_path = os.path.join(ORDERS_DIRECTORY, str(curr_date.year),
                                 str(curr_date.month), str(curr_date.day))
        if os.path.exists(data_path):
            data_files = {}

            for dirpath, dirnames, filenames in os.walk(data_path):

                if filenames:
                    filenames.sort()

                for filename in filenames:
                    file_path = dirpath + '/' + filename
                    data_file = open(file_path, 'r')
                    order_data = jsonpickle.decode(data_file.read())
                    data_files[filename, file_path] = order_data

            data[curr_date] = data_files

        curr_date += datetime.timedelta(days=1)

    return data

def audit_data(start_date, end_date, save_path):
    """Audits the data by retrieving the
    necessary information and parsing it
    into a human readable .xls file.

    @warning: Compiling these .xls files is
    costly and as such this function should
    only be called sparingly.

    @param from_date: datetime.date object
    that represents the starting date for
    the data to be gathered from, inclusive.

    @param until_date: datetime.date object
    that represents the ending date for the
    data to be gathered until, inclusive.

    @return: xlwt.Workbook representing the
    workbook that all of the information was
    added to.
    """
    workbook = xlsxwriter.Workbook(save_path)
    audit_sheet = workbook.add_worksheet('AUDIT SHEET')

    data = _get_data(start_date, end_date)

    date_data = []
    item_frequency = Counter()

    for date in data:

        for date_data in _generate_day_data(data[date]):

            date_data.append([date_data.name, date_data.total])
            item_frequency.update(date_data.item_frequency)


class DayData(object):
    """

    """
    def __init__(self, name, total, order_data, item_freq):
        """

        @param name:
        @param total:
        @param order_data:
        @param item_dict:
        @return:
        """
        self.name = name
        self.total = total
        self.order_data = order_data
        self.item_freq = item_freq

class OrderData(object):
    """

    """
    def __init__(self, name, total, order_data, item_freq):
        """

        @param name:
        @param total:
        @param order_data:
        @param item_dict:
        @return:
        """
        self.name = name
        self.total = total
        self.order_data = order_data
        self.item_freq = item_freq



if __name__ == '__main__':

    start_date = datetime.date(2011, 1, 1)
    end_date = datetime.date(2013, 12, 30)

    curr_time = time.time()
    data_f = _get_data(start_date, end_date)
    for each in data_f: print each
    print 'It took ---> ' + str(time.time() - curr_time) + ' to get data'

    curr_time = time.time()
    wkbk = audit_data(start_date, end_date)
    print 'It took ----> ' + str(time.time() - curr_time) + ' to perform the audit'