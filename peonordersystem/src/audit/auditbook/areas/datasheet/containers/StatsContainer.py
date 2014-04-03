"""This module defines the container
used for storing and interacting with
stats components.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .components.Grouper import KeyGrouper
from .components.Mean import CategoryMean
from .components.Median import CategoryMedian

from .abc.Container import Container

from peonordersystem.src.audit.auditbook.areas.datasheet.parsers.DataParserFactory\
    import DataParserFactory
from peonordersystem.src.audit.auditbook.areas.datasheet.parsers.components.KeyParsers \
    import DateKeyParser


class TimeCategoryStatsContainer(Container):
    """Container used for interacting with
    stats _components that operate based
    on category.
    """

    STATS_COMPONENTS = {
        'MEAN': CategoryMean,
        'MEDIAN': CategoryMedian
    }

    PARSER_DATA = {
        'key_parser': 'TIMES'
    }

    def __init__(self, attributes, time_keys):
        """Initializes a new TimeCategoryStatsContainer object.

        @param attributes: Keyword attributes representing the
        expected value parser and stats _components type.

            'value_parser'  :   attribute to be given to parser.
            'stats_component'   :   'MEAN' or 'MEDIAN'

        @param time_keys: list of datetime.time keys representing
        the associated time categories.
        """
        attributes['key_parser'] = 'TIMES'
        self._parser_data = DataParserFactory(attributes)
        self._category_parser = DateKeyParser()
        self._key_grouper = KeyGrouper(time_keys)

        stats_name = attributes['stats_component']
        component = self._get_component(stats_name)

        self._data = []
        self._values = []

        for value in time_keys:
            stats_data = component()
            self._values.append(stats_data)
            self._data.append(stats_data.data)

        self.current_data = None

    def _get_component(self, name):
        """Gets the component based on
        the given name.

        @param name: str representing the
        component to generate.

        @return: stats component that has
        been generated.
        """
        return self.STATS_COMPONENTS[name]

    @property
    def data(self):
        """Gets the data associated
        with this stats container.

        @return: tuple of ints representing
        the values associated with the keys
        """
        return tuple(self._data)

    def _update_stored_data(self):
        """Updates the stored data
        to hold up to date stats
        data.

        @return: list of ints representing
        the generated stats data.
        """
        data = []

        for stats_data in self._values:
            data.append(stats_data.data)

        return data

    def _update_single_value(self, index):
        """Updates a single value of the
        stored data. This provides a more
        efficient way to update the data
        given that the only change was in
        a known, given index.

        @param index: int representing the
        index that was updated.

        @return: None
        """
        stats_data = self._values[index]
        self._data[index] = stats_data.data

    def add(self, data):
        """Adds the given data to the
        stats container to generate
        the stats from the given data.

        @param data: DataBundle object
        that represents the data to have
        the category stats extracted from
        it.

        @return: int representing the
        index of the keys that the data
        was added to.
        """
        self.current_data = data
        index = self._get_key_index()
        self._update_data_at(index)
        self.current_data = None
        return index

    def _get_key_index(self):
        """Gets the index of the
        key associated with the
        current data.

        @return: int representing
        the index that the current
        data value should be grouped
        at.
        """
        key = self._get_key()
        return self._key_grouper.get_key_index(key)

    def _update_data_at(self, index):
        """Updates the current data at
        the given index.

        @param index: int representing
        the index to be updated at.

        @return: None
        """
        value = self._get_value()
        category = self._get_category_data()

        stats_data = self._values[index]
        stats_data.update(category, value)

        self._update_single_value(index)

    def _get_key(self):
        """Gets the key associated
        with the current data.

        @return: int representing
        the category associated with
        the current data.
        """
        return self._parser_data.get_data_comparison_value(self.current_data)

    def _get_category_data(self):
        """Gets the parsed
        category data from the
        current data.

        @return: value representing
        the category associated with
        the current stored data.
        """
        return self._category_parser.get_key(self.current_data)

    def _get_value(self):
        """Gets the parsed value
        data from the current data.

        @return: value representing
        the value associated with the
        current stored data.
        """
        return self._parser_data.get_data_value(self.current_data)

