"""This Module represents the container used
to group values by keys.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""

from .abc.Container import Container
from .components.Grouper import KeyGrouper
from src.peonordersystem.audit.datasheet.areas.parsers.abc.DataParser import \
    DataParser


class GroupByKeyContainer(Container):
    """Class that is used to update and
    store data.
    """

    def __init__(self, data_parser, data_keys):
        """Initializes the class with the
        given parser and keys information.

        @param data_parser: DataParser object
        that holds the necessary parsers for
        processing incoming data.

        @param data_keys: list of objects
        representing the keys.
        """
        self._grouper = KeyGrouper(data_keys)
        self._check_parser(data_parser)
        self._data_parser = data_parser
        self._data_keys = tuple(data_keys)
        self._data = self._create_initial_data_values()

    @staticmethod
    def _check_parser(parser):
        """Checks if the given package value is of
        the expected subclass.

        @param parser: object that is to be
        tested if it is an instance or subclass of
        DataParser

        @return: bool representing if the test was
        passed.
        """
        if not parser or not isinstance(parser, DataParser):
            curr_type = type(parser)
            raise ValueError('Expected instance of DataParser to be given for '
                             'ValueDataArea. Received {} instead.'.format(curr_type))

        return True

    def _create_initial_data_values(self):
        """Creates the data values.

        @return: list of equal length
        to the data keys but populated
        with zeros.
        """
        return [0 for each in self._data_keys]

    @property
    def data(self):
        """Gets the stored data.

        @return: tuple of values
        representing the stored
        data sorted by key and
        parsed for values.
        """
        return tuple(self._data)

    def add(self, data):
        """Adds the given data to
        be grouped and placed into
        the stored data by key.

        @param data: DataBundle
        object that is to be processed.

        @return: int representing the
        index the data was placed at,
        this index matches the associated
        key value.
        """
        return self._insert_data_value(data)

    def _insert_data_value(self, data):
        """Inserts the data value into the
        appropriate spot.

        @param data: data representing the
        data to be inserted into the values.

        @return: None
        """
        index = self._find_key_index(data)
        self._data[index] += self._get_data_value(data)
        return index

    def _find_key_index(self, data):
        """Finds the associated index that this
        given data should be mapped under the
        keys as.

        @param data: data to find associated
        position.

        @return: int representing the index that
        the data should be associated with.
        """
        cmp_value = self._get_data_comparison_value(data)
        index = self._grouper.get_key_index(cmp_value)
        return index

    def _get_data_value(self, data):
        """Gets the value associated with
        the data.

        @param data: DataBundle that is to
        have its value obtained.

        @return: value associated with the
        DataBundle.
        """
        return self._data_parser.get_data_value(data)

    def _get_data_comparison_value(self, data):
        """Gets the value associated with the
        data comparison.

        @param data: DataBundle to have the
        value obtained from it.

        @return: value representing the data
        comparison.
        """
        return self._data_parser.get_data_comparison_value(data)

