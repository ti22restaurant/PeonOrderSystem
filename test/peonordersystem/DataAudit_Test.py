"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from src.peonordersystem.CustomExceptions import InvalidDateRangeError
from src.peonordersystem.ConfirmationSystem import CHECKOUT_FILE_NAME, \
    ORDER_FILE_NAME
from src.peonordersystem import DataAudit
from src.peonordersystem import path

from test.peonordersystem.standardoperations_test import generate_random_date, \
    MAXIMUM_POTENTIAL_DATE_SHIFT_IN_DAYS, ORDERS_DATES_RANGE_MAX, \
    ORDERS_DATES_RANGE_MIN

import jsonpickle
import datetime
import os

import time


import unittest

TABS = '    '


class DataAuditTest(unittest.TestCase):
    """

    """
    print TABS + 'DataAudit testing'

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_file_creation(self):
        """Test that the request directory
        and today directory were created
        and exist.

        @return: None
        """
        # Testing case here must consider both if the request directory
        # and the today directory have been created and therefore
        # exist.
        print TABS * 2 + 'Testing that the necessary directories have been created'
        self.assertTrue(os.path.exists(DataAudit.REQUEST_DIRECTORY))
        self.assertTrue(os.path.exists(DataAudit.TODAY_DIRECTORY))
        print TABS * 2 + 'Finished testing directory creation'

    def test_get_data(self):
        """Tests the method that obtains the
        data from the data storage area.

        @return: None
        """
        pass

if __name__ == "__main__":
    unittest.main()