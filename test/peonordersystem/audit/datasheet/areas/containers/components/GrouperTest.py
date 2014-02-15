"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import unittest
from random import randint

from peonordersystem.audit.auditbook.areas.datasheet.containers.components.Grouper \
    import KeyGrouper


class KeyGrouperTest(unittest.TestCase):
    """

    """

    START_RANGE = 0
    END_RANGE = 1000

    def setUp(self):
        """

        @return:
        """
        self._key_grouper = None
        self._keys = None

    def tearDown(self):
        """

        @return:
        """
        del self._key_grouper
        del self._keys

    def _get_index(self, value):
        """

        @return:
        """
        return self._key_grouper.get_key_index(value)

    def create_default_key_grouper(self, step=1):
        """

        @return:
        """
        self._keys = range(self.START_RANGE, self.END_RANGE, step)
        self._result = [0 for x in self._keys]
        self._key_grouper = KeyGrouper(self._keys)

    def test_empty_keys(self):
        """

        @return:
        """
        self.assertRaises(Exception, KeyGrouper, [])

    def test_None_keys(self):
        """

        @return:
        """
        self.assertRaises(Exception, KeyGrouper, None)

    def test_varying_types_keys(self):
        """

        @return:
        """
        self.assertRaises(Exception, KeyGrouper, [1, 2, 'a'])

    def test_unsorted_keys(self):
        """

        @return:
        """
        values = range(10)
        keys = values[1:] + values[:1]

        self.assertRaises(Exception, KeyGrouper, keys)

    def test_get_key_index_step_of_one(self):
        """

        @return:
        """
        self.create_default_key_grouper(step=1)
        self._check_values()

    def test_get_key_index_step_of_three(self):
        """

        @return:
        """
        self.create_default_key_grouper(step=3)
        self._check_values()

    def test_get_key_index_random_step(self):
        """

        @return:
        """
        step = randint(self.START_RANGE, self.END_RANGE)
        self.create_default_key_grouper(step=step)
        self._check_values()

    def _check_values(self):
        """

        @return:
        """
        self._check_value_below_range()
        self._check_value_in_range()
        self._check_value_above_range()

    def _check_value_below_range(self):
        """

        @return:
        """
        self._check_value_below_range_equal()
        self._check_value_below_range_random()

    def _check_value_below_range_equal(self):
        """

        @return:
        """
        value = self._keys[0]
        index = self._get_index(value)
        self.assertEqual(value, self._keys[index])

    def _check_value_below_range_random(self):
        """

        @return:
        """
        value = randint(self._keys[0] * 1000, self._keys[0])
        index = self._get_index(value)
        self.assertLessEqual(value, self._keys[index])

    def _check_value_in_range(self):
        """

        @return:
        """
        value = randint(self._keys[0], self._keys[-2])
        index = self._get_index(value)
        self.assertGreaterEqual(value, self._keys[index])
        self.assertLessEqual(value, self._keys[index + 1])

    def _check_value_above_range(self):
        """

        @return:
        """
        self._check_value_above_range_equal()
        self._check_value_above_range_random()

    def _check_value_above_range_equal(self):
        """

        @return:
        """
        value = self._keys[-1]
        index = self._get_index(value)
        self.assertEqual(value, self._keys[index])

    def _check_value_above_range_random(self):
        """

        @return:
        """
        value = randint(self._keys[-1], self._keys[-1])
        index = self._get_index(value)
        self.assertGreaterEqual(value, self._keys[index])

