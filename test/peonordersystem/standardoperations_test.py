"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from src.peonordersystem.path import SYSTEM_ORDERS_PATH

import jsonpickle
import datetime
import random
import os

MAXIMUM_POTENTIAL_DATE_SHIFT_IN_DAYS = 7 * 356
MAX_TIMEDELTA = datetime.timedelta(MAXIMUM_POTENTIAL_DATE_SHIFT_IN_DAYS)

MIN_DATE = datetime.date.min + MAX_TIMEDELTA

MAX_DATE = datetime.date.max - MAX_TIMEDELTA

ORDERS_DATES_RANGE_MAX = datetime.date(2013, 12, 14)
ORDERS_DATES_RANGE_MIN = datetime.date(2013, 10, 1)


def generate_random_date(start_date=MIN_DATE, end_date=MAX_DATE):
    """Generates a pseudo-random date from within
    the given ranges:

    @keyword year: 2 tuple of int representing the (MIN, MAX),
    of the range to be selected. By default is constants that
    represent the min as 7 and max as 9993. (to allow some
    potential variation if time is being removed/added)

    @keyword month: 2 tuple of int representing the (MIN, MAX),
    of the range to be selected for the month. By default is
    constants min: 1, max: 12.

    @keyword day: 2 tuple of int representing the (MIN, MAX),
    of the range to be selected for the day. By default is
    constants min: 1, max: 28 (28 to allow for february).

    @raise ValueError: If the given dates are not within
    the specified ranges defined by the module wide constants

    @return: datetime.date object that represents the
    randomly generated date.
    """
    if start_date > end_date or start_date < MIN_DATE or end_date > MAX_DATE:
        raise ValueError('Failure in testing case. gave inadequate date parameters')

    change_in_date = (end_date - start_date) / random.randint(1, 50)
    return start_date + change_in_date


def get_file_data(filepath):
    """Retrieves the file data stored
    in the given file.

    @param filepath: str representing the
    path to the file that should be opened
    and decoded with jsonpickle.

    @return: list of MenuItem objects that
    represents the decoded files data.
    """
    if not os.path.exists(filepath):
        raise ValueError('Expected given filepath [{}] to exist'.format(filepath))

    file_data_str = open(filepath, 'r').read()
    return jsonpickle.decode(file_data_str)


