"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
import unittest

from peonordersystem.audit.auditbook.areas.datasheet.parsers.DataBundleParser import \
    PackagedDataParser

from src.peonordersystem.audit.datasheet.areas.MeanValueDataArea import \
    MeanValueDataArea
from src.peonordersystem.audit.datasheet.areas.KeyDataAreas import TimeKeysDataArea


class MeanValueDataAreaTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """

        @param cls:
        @return:
        """
        cls.time_keys = TimeKeysDataArea()
        cls.data_parser = PackagedDataParser('TIME', 'ORDERS')
        cls.mean_data = MeanValueDataArea(cls.data_parser, cls.time_keys)

    def setUp(self):
        """

        @return:
        """
        self.mean_values = []

    def _get_current_data(self):
        return self.mean_data.data

    def tearDown(self):
        """

        @return:
        """
        pass

    def insert_values(self):
        """

        @return:
        """

    def test_empty_data(self):
        """

        @return:
        """
        empty_data = self._get_empty_data()
        self.assertEqual(self.mean_data.data, empty_data)

    def _get_empty_data(self):
        """

        @return:
        """
        return [0 for x in self.time_keys.data]

