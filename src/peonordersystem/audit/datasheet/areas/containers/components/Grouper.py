"""Grouper Module defines classes that
act as Grouper components.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from .abc.Grouper import Grouper
from .abc.Component import Component


class KeyGrouper(Grouper, Component):
    """KeyGrouper groups given objects
    into their associated keys given
    at initialization"""

    def __init__(self, keys):
        """Initializes a new KeyGrouper
        that is interacted with to obtain
        the appropriate index for a key.
        """
        self._key_type = None

        self._ensure_keys_requirements(keys)
        self._keys = keys

    @property
    def data(self):
        """Gets the keys data.

        @return: tuple representing
        the stored keys data.
        """
        return tuple(self._keys)

    def _ensure_keys_requirements(self, keys):
        """Ensures that the key requirements
        are met.

        @raise ValueError: If the keys are empty.

        @return: None
        """
        try:
            self._check_key_requirements(keys)
        except IndexError:
            raise ValueError('Cannot create grouping with empty keys set')

    def _check_key_requirements(self, keys):
        """Checks that the key requirements have
        been met. These requirements are:

            1. Each entry is a uniform type.
            2. Each value is in sorted order.
            3. The keys are non-empty.

        @param keys: list of objects representing
        the keys to generate.

        @return: None
        """
        prev_key = keys[0]
        self._key_type = type(prev_key)

        for key in keys[1:]:
            self._check_uniform_type(key)
            self._check_sorted_pair(prev_key, key)

    def _check_uniform_type(self, key):
        """Checks that each key value is
        of uniform type.

        @raise TypeError: if the key is
        not of the expected key type.

        @param key: object representing the
        key.

        @return: bool value if the test was
        passed.
        """
        if not type(key) == self._key_type:
            raise TypeError('Given keys data are not of the same uniform type!')
        return True

    def _check_sorted_pair(self, prev_key, next_key):
        """Checks that each key value is in
        sorted order.

        @raise ValueError: if the next key is
        greater than the previous key.

        @param prev_key: object representing
        the previous key. Expected to be less
        than or equal to the next key.

        @param next_key: object representing the
        next key. Expected to be greater than
        or equal to the previous key.

        @return: bool value if the test was
        passed.
        """
        if prev_key > next_key:
            raise ValueError('Given keys are not in sorted order!')
        return True

    def get_key_index(self, key):
        """Gets the index associated
        with the key. This index returned
        represents the value that the key
        may be categorized under.

        @param key: object representing
        the value to be categorized.

        @return: int representing the index
        that the key may be categorized at
        in the data.
        """
        self._check_uniform_type(key)
        return self._find_index(self._keys, key)

    @staticmethod
    def _find_index(sublist, value):
        """Finds the index by parsing the potential
        data keys that this data could be associated
        with.

        @param sublist: collection representing the
        keys data to parse to find an associated
        value.

        @param value: value representing the comparison
        value that should be compared to the keys.

        @return: int representing the index that
        represents the category or key that the
        associated value should be indexed under.
        """
        if len(sublist) > 1:
            mid_index = len(sublist) / 2
            mid_value = sublist[mid_index]

            if value < mid_value:
                return KeyGrouper._find_index(sublist[:mid_index], value)
            else:
                return mid_index + KeyGrouper._find_index(sublist[mid_index:], value)

        return 0
