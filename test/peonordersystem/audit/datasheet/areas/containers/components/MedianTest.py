"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import unittest
from random import randint
from bisect import insort

from src.peonordersystem.audit.datasheet.areas.containers.components.Median \
    import CategoryMedian


class CategoryMedianTest(unittest.TestCase):
    """

    """
    NUMBER_OF_CATEGORIES = 100

    def setUp(self):
        """

        @return:
        """
        self._median_data = CategoryMedian()

    def tearDown(self):
        """

        @return:
        """
        del self._median_data

    def test_median_single_category(self):
        """

        @return:
        """
        value = randint(1, 1000)
        category = 'default single category'
        self._update_data(category, value)
        self._update_data(category, value)
        self.then_median_is(value * 2)

    def _update_data(self, category, value):
        """

        @param category:
        @param value:
        @return:
        """
        self._median_data.update(category, value)

    def then_median_is(self, value):
        """

        @param value:
        @return:
        """
        median = self._median_data.data
        self.assertEqual(median, value)

    def test_median_multiple_categories_even(self):
        """

        @return:
        """
        data = []

        for x in range(self.NUMBER_OF_CATEGORIES):
            value = randint(1, 1000)
            self._update_data(chr(x), value)
            insort(data, value)

        v1 = data[len(data) / 2]
        v2 = data[len(data) / 2 - 1]

        exp_value = (v1 + v2) / 2.0
        self.then_median_is(exp_value)

    def test_median_multiple_categories_odd(self):
        """

        @return:
        """
        data = []

        for x in range(self.NUMBER_OF_CATEGORIES + 1):
            value = randint(1, 1000)
            self._update_data(chr(x), value)
            insort(data, value)

        self.then_median_is(data[len(data) / 2])
