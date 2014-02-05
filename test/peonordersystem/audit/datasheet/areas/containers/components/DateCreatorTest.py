"""This module tests the DateCreator
object for proper functionality.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import unittest
from random import randint
from datetime import datetime, date, timedelta

from src.peonordersystem.audit.datasheet.areas.containers.components.DateCreator \
    import DateCreator


class DateCreatorTest(unittest.TestCase):
    """Tests the DateCreator component."""

    def setUp(self):
        """Sets up the testing data.

        @return: None
        """
        self.date_creator = None

    def tearDown(self):
        """Tears down the testing data.

        @return: None
        """
        del self.date_creator

    def when_datecreator_spans(self, start_datetime, end_datetime):
        """Creates the DateCreator component that spans
        the given datetime.

        @param start_datetime: datetime.datetime that represents
        the starting datetime.

        @param end_datetime: datetime.datetime that represents
        the ending datetime.

        @return: None
        """
        self.date_creator = DateCreator(start_datetime, end_datetime)

    def then_dates_span(self, start_datetime, end_datetime):
        """Tests the DateCreator component if it spans the
        given datetime.

        @param start_datetime: datetime.datetime that represents
        the starting datetime.

        @param end_datetime: datetime.datetime that represents
        the ending datetime.

        @return: None
        """
        increment = self.date_creator.DATE_INCREMENT
        curr_datetime = start_datetime

        for each_date in self.date_creator.data:
            self.assertLessEqual(start_datetime.date(), each_date)
            self.assertGreaterEqual(end_datetime.date(), each_date)
            self.assertEqual(curr_datetime.date(), each_date)
            curr_datetime += increment

    def test_none_dates(self):
        """Test the DateCreator object when
        given None as an argument.

        @return: None
        """
        self._none_dates_first_arg()
        self._none_dates_second_arg()
        self._none_dates_both_args()

    def _none_dates_first_arg(self):
        """Test the DateCreator object
        when None is the first argument.

        @return: None
        """
        arg1 = None
        arg2 = date.today()

        self.assertRaises(Exception, DateCreator, arg1, arg2)

    def _none_dates_second_arg(self):
        """Tests the DateCreator when
        None is the second argument.

        @return: None
        """
        arg1 = date.today()
        arg2 = None

        self.assertRaises(Exception, DateCreator, arg1, arg2)

    def _none_dates_both_args(self):
        """Tests the DateCreator when
        both arguments are None.

        @return: None
        """
        arg1 = None
        arg2 = None

        self.assertRaises(Exception, DateCreator, arg1, arg2)

    def test_same_dates(self):
        """Tests the DateCreator when
        given the same date.

        @return: None
        """
        start_datetime = datetime.now()
        end_datetime = start_datetime

        self.when_datecreator_spans(start_datetime, end_datetime)
        self.then_dates_span(start_datetime, end_datetime)

    def test_dates_outside_of_range(self):
        """Tests the DateCreator when the
        given dates are such that
        start_date > end_date.

        @return: None
        """
        arg1 = datetime.now()
        arg2 = arg1 - timedelta(days=1)

        self.assertRaises(Exception, DateCreator, arg1, arg2)

    @unittest.skip('Test covers all possible days. As such it is highly '
                   'inefficient and should only be run when necessary.')
    def test_min_max_dates_range(self):
        """Tests the DateCreator when the dates
        span the minimum to maximum datetimes.

        @return: None
        """
        start_datetime = datetime.min
        #subtract one to allow test case to be tested.
        end_datetime = datetime.max - timedelta(days=1)

        self.when_datecreator_spans(start_datetime, end_datetime)
        self.then_dates_span(start_datetime, end_datetime)

    def test_values_in_domain(self):
        """Tests the DateCreator when it
        spans a random date interval.

        @return: None
        """
        start_datetime = datetime.now() - timedelta(days=randint(1, 10000))
        end_datetime = datetime.now() + timedelta(days=randint(1, 10000))

        self.when_datecreator_spans(start_datetime, end_datetime)
        self.then_dates_span(start_datetime, end_datetime)