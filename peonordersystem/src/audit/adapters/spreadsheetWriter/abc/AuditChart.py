"""This module defines the abstract base class
for the wrapper that provides the functionality
for the chart to be created and displayed.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod, abstractproperty


class AuditChart(object):
    """Abstract base class that
    defines the methods that must
    be instantiated for the object
    to be considered an AuditChart.
    """

    __metaclass__ = ABCMeta

    @abstractproperty
    def height(self):
        """Gets the height
        in rows.

        @return: int
        """
        pass

    @abstractproperty
    def width(self):
        """Gets the width
        in columns.

        @return: int
        """
        pass

    @abstractmethod
    def set_keys(self, keys):
        """Sets the keys.

        @param keys: collection
        that stores the keys.

        @return: None
        """
        pass

    @abstractmethod
    def add_series(self, data, title='values', has_trend_line=False):
        """Adds the series data to the chart with
        the given title.

        @param data: DataArea that is to be added to
        the chart.

        @keyword title: str representing the title
        of the series.

        @keyword has_trend_line: bool value
        representing if the series should have
        a trend line generated for the data.

        @return: None
        """
        pass

