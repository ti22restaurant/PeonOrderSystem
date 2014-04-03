"""This module defines the abstract
base class component used in the
generalsheet.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
@version: 1.0
"""
from abc import ABCMeta, abstractmethod


class GeneralComponent(object):
    """GeneralComponent defines
    the methods and base functionality
    for a being a useable component.
    """

    __metaclass__ = ABCMeta

    def __init__(self, date, worksheet):
        """Initializes the component.

        @param date: datetime.date that
        is associated with the date that
        the component will be storing data
        from.

        @param worksheet: Worksheet that
        the component will be added to.
        """
        self._date = date
        self._worksheet = worksheet

    def _check_date(self, data):
        """Checks if the given date is
        a datetime.date object.

        @raise ValueError: if the
        given data doesn't match the
        expected date.

        @param data: data that is
        to be checked for the date.

        @return: bool value representing
        if the test was passed.
        """
        if self.date != data.date:
            raise ValueError('Cannot add data stored at a different date to '
                             'a general component!')
        return True

    @abstractmethod
    def update(self, data):
        """Updates the component
        with the given data.

        @param data: data to be
        used to update the component.

        @return: None
        """
        pass

    @abstractmethod
    def finalize(self):
        """Finalizes the component.

        @return: None
        """
        pass