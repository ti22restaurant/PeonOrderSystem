"""This module defines the factory
used for generating DataParsers.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.DataParser import DataParser
from .components.KeyParsers import TimeKeyParser, DateKeyParser
from .components.ValueParsers import (TotalsValueParser,
                                      OrdersValueParser,
                                      ItemsValueParser)


class DataParserFactory(DataParser):
    """Factory that is used for creating
    the DataParsers.
    """

    KEY_PARSERS = {
        'TIMES': TimeKeyParser,
        'DATES': DateKeyParser
    }

    VALUE_PARSERS = {
        'TOTALS': TotalsValueParser,
        'ORDERS': OrdersValueParser,
        'ITEMS': ItemsValueParser
    }

    def __init__(self, data):
        """Initializes two dataparsers objects
        from the given keywords.

        @param data: dict representing the data
        to be generated:

            'key_parser'    :   'TIMES' or 'DATES',
            'value_parser'  :   'TOTALS', 'ORDERS', 'ITEMS'
        """
        key_parser = self._get_key_parser(data['key_parser'])
        value_parser = self._get_value_parser(data['value_parser'])
        super(DataParserFactory, self).__init__(key_parser, value_parser)

    def _get_key_parser(self, name):
        """Gets the associated key
        parser.

        @param name: str representing
        the key parser to generate.

        @return: KeyParser object
        that representing the created
        key parser.
        """
        self._check_key_name_exists(name)
        return self.KEY_PARSERS[name]()

    def _check_key_name_exists(self, name):
        """Checks if the given key name
        exists.

        @raise NameError: if the given name
        doesn't

        @param name: str representing the
        name associated with the key parsers.

        @return: bool representing if the
        test was passed.
        """
        if not name in self.KEY_PARSERS:
            raise NameError('Invalid key parser name given! No parser named'
                            ' {}'.format(name))
        return True

    def _get_value_parser(self, name):
        """Gets the associated ValueParser
        from the given name.

        @param name: str representing the
        name associated with the ValueParser
        to be generated.

        @return: ValueParser object that was
        generated from the given str.
        """
        self._check_value_name_exists(name)
        return self.VALUE_PARSERS[name]()

    def _check_value_name_exists(self, name):
        """Checks if the given str representing
        a ValueParser may be used.

        @raise NameError: if the given str
        representing the ValueParser was
        invalid.

        @param name: str representing the
        ValueParser to be generated.

        @return: bool value representing if
        the test was passed.
        """
        if not name in self.VALUE_PARSERS:
            raise NameError('Invalid value parsers name given! No parser named '
                            ' {}'.format(name))
        return True
