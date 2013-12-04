"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
import datetime
import random


def generate_random_date():
    """Generates a pseudo-random date from within
    the given ranges:

        year: 0-2013
        month: 1-12
        day: 1-28 (to ensure always valid day chosen)

    @return: datetime.date object that represents the
    randomly generated date.
    """
    year = random.randint(datetime.MINYEAR, datetime.MAXYEAR)
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    return datetime.date(year, month, day)