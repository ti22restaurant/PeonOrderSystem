"""
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""

from abc import ABCMeta, abstractmethod

class ChartArea(object):
    """

    """
    __metaclass__ = ABCMeta

    _chart = None

    def __init__(self, chart):
        """

        @return:
        """
        self._chart = chart
        pass

    def add_categories(self, categories):
        self._chart.add_series({'categories': categories})

    def add_values(self, values):
        self._chart.

    @abstractmethod
    def connect(self, worksheet):
        """

        @param worksheet:
        @return:
        """
        self.worksheet

    def write_data(self, *args):
        self._chart.


class ItemDataChart(object):
    """

    """

    def connect(self, chart):
        """

        @param chart:
        @return:
        """

