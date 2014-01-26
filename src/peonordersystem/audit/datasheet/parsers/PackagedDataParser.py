"""This module represents
@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
from .components.KeyParsers import (TimeKeyParser, DateKeyParser)
from .components.ValueParsers import (OrdersValueParser, ItemsValueParser,
                                      TotalsValueParser)
from .DataParser import DataParser


class PackagedDataParser(DataParser):
    """PackagedDataParser is used for parsing
    packaged data. It creates a specific type of
    parser for generating parsing packaged data
    based on the given initialization parameters.
    """
    KEY_PARSERS = {
        'TIME': TimeKeyParser,
        'DATE': DateKeyParser
    }

    VALUE_PARSERS = {
        'ORDERS': OrdersValueParser,
        'ITEMS': ItemsValueParser,
        'TOTALS': TotalsValueParser
    }

    def __init__(self, name_of_key_parser, name_of_value_parser):
        """Initializes a PackagedDataParser object.

        @param name_of_value_parser: str representing the type of
        value parser to create.

            1. ORDERS: Parser that pulls the number of orders from
            given PackagedData.

            2. ITEMS: Parser that pulls the number of items from given
            PackagedData.

            3. TOTALS: Parser that pulls total data from given PackagedData.

        @param name_of_key_parser: str representing the type of key parser
        to create.

            1. TIME: Parser that pulls the time from the PackagedData as the key.

            2. DATE: Parser that pulls the date from the PackagedData as the key.
        """
        key_parser = self._get_key_parser(name_of_key_parser)
        value_parser = self._get_value_parser(name_of_value_parser)
        super(PackagedDataParser, self).__init__(key_parser, value_parser)

    def _get_key_parser(self, name):
        """Gets the key parser associated
        with the given name.

        @param name: str representing the key
        parser to be created.

        @raise NameError: if the given name is
        not associated with an applicable KeyParser.

        @return: KeyParser object associated
        with the given name.
        """
        try:
            return self._get_key_parser_object(name)

        except KeyError:
            raise NameError(name + ' is not a valid key parser name')

    def _get_key_parser_object(self, name):
        """Gets the KeyParser object associated
        with the given name.

        @param name: str representing the name
        that the KeyParser is associated with.

        @return: KeyParser object.
        """
        key_parser = self.KEY_PARSERS[name.upper()]
        key_parser_obj = key_parser()
        return key_parser_obj

    def _get_value_parser(self, name):
        """Gets the value parser associated
        with the given name.

        @param name: str representing the value
        parser to be created.

        @raise NameError: if the given name is
        not associated with an applicable
        ValueParser.

        @return: ValueParser object that is
        associated with the given name.
        """
        try:
            return self._get_value_parser_object(name)

        except KeyError:
            raise NameError(name + ' is not a valid value parser name')

    def _get_value_parser_object(self, name):
        """Gets the value parser object associated
        with the given name.

        @param name: str representing the name that
        the ValueParser is associated with.

        @return: ValueParser object.
        """
        value_parser = self.VALUE_PARSERS[name.upper()]
        value_parser_obj = value_parser()
        return value_parser_obj
