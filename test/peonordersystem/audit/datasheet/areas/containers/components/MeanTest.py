"""This module provides the unittests
for the Mean objects.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import unittest
from random import randint

from src.peonordersystem.audit.datasheet.areas.containers.components.Mean import \
    CategoryMean


class CategoryMeanTest(unittest.TestCase):
    """This class provides the unittests for
    the CategoryMean object."""
    NUMBER_OF_TESTS = 25
    NUMBER_OF_CATEGORIES = 10

    NUMBER_OF_PLACES = 4

    def setUp(self):
        """Sets up the initial data.

        @return: None
        """
        self._category_mean = CategoryMean()

    def tearDown(self):
        """Tears down the initial data.

        @return: None
        """
        del self._category_mean

    def test_initial_values(self):
        """Tests that the initial values
        are set correctly.

        @return: None
        """
        mean_value = self._category_mean.data
        self.assertEqual(mean_value, 0.0)

    def test_none_update_args(self):
        """Tests that operates correctly
        when given None arguments.

        @return: None
        """
        self._none_update_args_test_first_arg()
        self._none_update_args_test_second_arg()
        self._none_update_args_test_both_args()

    def _none_update_args_test_first_arg(self):
        """Tests the update when given None as
        first argument.

        @return: None
        """
        meth = self._category_mean.update
        arg1 = None
        arg2 = 10.0

        self.assertRaises(Exception, meth, arg1, arg2)

    def _none_update_args_test_second_arg(self):
        """Tests the update method when given
        None as second argument.

        @return: None
        """
        meth = self._category_mean.update
        arg1 = 10.0
        arg2 = None

        self.assertRaises(Exception, meth, arg1, arg2)

    def _none_update_args_test_both_args(self):
        """Tests the update method when given
        None as both arguments.

        @return: None
        """
        meth = self._category_mean.update
        arg1 = None
        arg2 = None

        self.assertRaises(Exception, meth, arg1, arg2)

    def test_update_with_single_category(self):
        """Tests the update method when a single
        category is updated.

        @return: None
        """
        exp_mean = 0.0

        for x in xrange(self.NUMBER_OF_TESTS):
            exp_mean += self._update_with_single_category()
            self.assertEqual(exp_mean, self._category_mean.data)

    def _update_with_single_category(self, category='category_name'):
        """Tests the update method with a single
        category.

        @keyword category: value representing the
        category to be associated with the update.

        @return: float representing the expected
        mean after the category has been updated.
        """
        sum = 0.0

        for x in xrange(self.NUMBER_OF_TESTS):
            value = randint(1, 10000)
            self._category_mean.update(category, value)
            sum += value

        return sum

    def test_update_with_multiple_categories(self):
        """Tests the update method with multiple
        categories.

        @return: None
        """
        exp_mean = 0.0

        for x in xrange(self.NUMBER_OF_TESTS):
            exp_mean += self._update_with_multiple_categories()
            self.assertAlmostEqual(exp_mean, self._category_mean.data, self.NUMBER_OF_PLACES)

    def _update_with_multiple_categories(self):
        """Updates the CategoryMean with multiple
        categories.

        @return: None
        """
        sum = 0.0

        for x in range(self.NUMBER_OF_CATEGORIES):
            sum += self._update_with_single_category(category=x)

        return round(sum / self.NUMBER_OF_CATEGORIES,
                     self._category_mean._round_digits)

    def test_update_multiple_iterations(self):
        """Tests the update over multiple iterations
        of both single and multiple categories update.

        @return: None
        """
        m1 = 0.0
        n1 = 1

        m2 = 0.0
        n2 = self.NUMBER_OF_CATEGORIES

        for x in xrange(self.NUMBER_OF_TESTS):
            
            m1 += self._update_with_single_category()
            exp_mean = self._update_expected_mean_data(m1, n1, m2, n2)
            self.assertEqual(exp_mean, self._category_mean.data)

            m2 += self._update_with_multiple_categories()
            exp_mean = self._update_expected_mean_data(m1, n1, m2, n2)
            self.assertEqual(exp_mean, self._category_mean.data)

    def _update_expected_mean_data(self, m1, n1, m2, n2):
        """Updates the expected mean data with the given
        data.

        @param m1: float representing the first mean.

        @param n1: int representing the number of items
        in the first mean.

        @param m2: float representing the second mean.

        @param n2: int representing the number of items
        in the second mean.

        @return: float representing the expected mean if
        both means are combined to form a new mean.
        """
        sum1 = m1 * n1
        sum2 = m2 * n2

        total_sum = sum1 + sum2

        #if statement to resolve fence post problem on first iteration. This is
        # simply used to be helpful in calculating the expected mean and is was
        # used so that the modules inner functionality wouldn't have to be exposed
        # to this test.
        if sum2:
            total_n = n1 + n2
        else:
            total_n = n1

        new_mean = total_sum / total_n

        return round(new_mean, self._category_mean._round_digits)
