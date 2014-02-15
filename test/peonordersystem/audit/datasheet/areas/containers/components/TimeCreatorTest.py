"""This module represents the unittests for
the TimeCreator object.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import unittest
from random import randint
from datetime import date, datetime, time

from peonordersystem.audit.auditbook.areas.datasheet.containers.components import \
    TimeCreator


class TimeCreatorTest(unittest.TestCase):
    """Tests the TimeCreator component"""

    def setUp(self):
        """Sets up a given test case data.

        @return: None
        """
        self.time_creator = None

    def tearDown(self):
        """Tears down a given test case data.

        @return: None
        """
        del self.time_creator

    def where_time_creator_spans_dates(self, start_time, end_time):
        """Creates the time creator that spans the given times.

        @param start_time: datetime.time representing the
        start time.

        @param end_time: datetime.time representing the
        end time.

        @return: None
        """
        self.time_creator = TimeCreator(start_time, end_time)

    def then_date_range_covers_dates(self, start_time, end_time):
        """Checks that the created TimeCreator spans the given
        time range.

        @param start_time: datetime.time that represents the
        start time.

        @param end_time: datetime.time that represents the
        end time.

        @return: None
        """
        increment = self.time_creator.TIME_INCREMENT
        curr_time = datetime.combine(date.today(), start_time)

        for each_time in self.time_creator.data:
            self.assertLessEqual(start_time, each_time)
            self.assertGreaterEqual(end_time, each_time)
            self.assertEqual(each_time, curr_time.time())
            curr_time += increment

    def test_none_times(self):
        """Tests the case where None values are
        given as parameters to the TimeCreator

        @return: None
        """
        self._none_times_first_arg()
        self._none_times_second_arg()
        self._none_times_both_args()

    def _none_times_first_arg(self):
        """Tests the case where None value is
        given as the first argument to the TimeCreator

        @return: None
        """
        arg1 = None
        arg2 = datetime.now().time()
        self.assertRaises(Exception, TimeCreator, arg1, arg2)

    def _none_times_second_arg(self):
        """Tests the case where None value is given
        as the second argument to the TimeCreator

        @return: None
        """
        arg1 = datetime.now().time()
        arg2 = None
        self.assertRaises(Exception, TimeCreator, arg1, arg2)

    def _none_times_both_args(self):
        """Tests the case where both arguments
        are None.

        @return: None
        """
        self.assertRaises(Exception, TimeCreator, None, None)

    def test_same_times(self):
        """Tests the case where the start time
        and end time are the same.

        @return: None
        """
        
        start_time = time(randint(0, 23), randint(0, 59), randint(0, 59))
        end_time = start_time

        self.where_time_creator_spans_dates(start_time, end_time)
        self.then_date_range_covers_dates(start_time, end_time)

    def test_times_outside_of_range(self):
        """Tests the case where the start_time > end_time

        @return: None
        """

        start_time = time(randint(12, 23), randint(0, 59), randint(0, 59))
        end_time = time(randint(0, 11), randint(0, 59), randint(0, 59))

        self.assertRaises(Exception, TimeCreator, start_time, end_time)

    def test_min_max_time_range(self):
        """Tests the case where the start time
        is the lowest possible time and end time
        is highest possible time.

        @return: None
        """
        start_time = time.min
        end_time = time.max

        self.where_time_creator_spans_dates(start_time, end_time)
        self.then_date_range_covers_dates(start_time, end_time)

    def test_values_in_domain(self):
        """Tests the case where random time
        values are generated such that
        start_time < end_time.

        @return: None
        """
        start_time = time(randint(0, 11), randint(0, 59), randint(0, 59))
        end_time = time(randint(12, 23), randint(0, 59), randint(0, 59))

        self.where_time_creator_spans_dates(start_time, end_time)
        self.then_date_range_covers_dates(start_time, end_time)