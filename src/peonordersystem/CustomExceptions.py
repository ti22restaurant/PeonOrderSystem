"""This module defines custom exceptions that may be thrown in the
PeonOrderSystem project. This module holds multiple classes that
define the exceptions that can be thrown.

@group Non-Fatal Errors: This group contains every non-fatal error
for the PeonOrderSystem project. Each Non-Fatal Error is designed
to be caught by the PeonOrderSystem and reported to the user in
real time.

@group Fatal Errors: This group contains custom defined fatal errors
for the PeonOrderSystem project. Each Fatal Error is designed not to
be caught.

@author: Carl McGraw
@contact: cjmcgraw( at )uw.edu
@version: 1.0
"""
import json
from src.peonordersystem.path import NON_FATAL_ERROR_MESSAGES_DATA as \
    ERROR_FILE

curr_file = open(ERROR_FILE, 'r')

error_data = json.load(curr_file)

ERROR_PREFIX = error_data['ERROR_PREFIX']

INVALID_ORDER_MESSAGE = ERROR_PREFIX + error_data['INVALID_ORDER_MESSAGE']

INVALID_ITEM_MESSAGE = ERROR_PREFIX + error_data['INVALID_ITEM_MESSAGE']

INVALID_RESERVATION_MESSAGE = ERROR_PREFIX + error_data['INVALID_RESERVATION_MESSAGE']

NO_SELECTION_MESSAGE = ERROR_PREFIX + error_data['NO_SELECTION_MESSAGE']


class InvalidItemError(Exception):
    """InvalidItemError is an exception that
    occurs when MenuItem operations have been
    performed on a non menu item. The most
    frequent case of this is when the object
    is of type None.

    @group Non-Fatal Errors: This class is a
    member of the Non-Fatal Errors group.
    """

    def __init__(self, message):
        """Initializes a new InvalidItemError
        exception. Displays the given message.

        @param message: str to be displayed when
        the error occurs.
        """
        super(InvalidItemError, self).__init__(message)


class InvalidOrderError(Exception):
    """InvalidOrderError is an exception that
    occurs when Order operations have been
    performed on an invalid Order. Orders may
    be invalid because they do not contain any
    valid MenuItems or are of the improper
    type.

    @group Non-Fatal Errors: This class is a
    member of the Non-Fatal Errors group.
    """

    def __init__(self, message):
        """Initializes a new InvalidOrderError
        object. Displays the given message when
        raised.

        @param message: str to be displayed when
        this error occurs
        """
        super(InvalidOrderError, self).__init__(message)


class InvalidReservationError(Exception):
    """InvalidReservationError is an exception
    that occurs when an non Reserver object has
    been treated as a Reserver object.

    @group Non-Fatal Errors: This class is a
    member of the Non-Fatal Errors group.
    """

    def __init__(self, message):
        """Initializes the InvalidReservationError
        object. Displays the given message when
        the error is raised.

        @param message: str to be displayed when
        the object is invoked and the error raised.
        """
        super(InvalidReservationError, self).__init__(message)


class NoSuchSelectionError(Exception):
    """NoSuchSelectionError is an exception
    that occurs when a selection has been
    requested, but a none type was returned
    meaning that no selection was made.

    @group Non-Fatal Errors: This class is
    a member of the Non-Fatal Errors group.
    """
    def __init__(self, message):
        """Initializes a new NoSuchSelectionError
        object. Displays the given message when
        this error is raised.

        @param message: str to be displayed when
        this error is raised.
        """
        super(NoSuchSelectionError, self).__init__(message)


class InvalidDateRangeError(Exception):
    """InvalidDateRangeError raises an exception
    when the given date range is outside of a
    safe range. This range by definition is expected
    to simply be when start_date > end_date.

    @group Fatal Errors: This class is a member
    of the Fatal Errors group. As such it wont be
    caught when it is called.

    """
    def __init__(self, start_date, end_date):
        """Initializes a new InvalidDateRangeError
        object. Displays a message stating the
        relationship between the start date and
        end date that is expected when this
        error is called. Specifically that the start
        date > end date.

        @raise TypeError: if start_date <= end_date

        @param start_date: datetime.date object representing
        the starting date of the range. Must be greater than
        end_date parameter.

        @param end_date: datetime.date object representing
        the ending date of the range. Must be less than the
        start_date parameter.
        """
        if start_date > end_date:
            message = 'Expected valid dates where the start date ' + \
                      ' <= end date. Got\n' \
                      'start_date ---> {}\n'.format(start_date) + \
                      'end_date ---> {}'.format(end_date)
            super(InvalidDateRangeError, self).__init__(message)
        else:
            message = 'Invalid use of InvalidDateRangeError. Dates are' \
                      ' within the range of start_date <= end_date. Values:\n' + \
                      'start_date ---> {}\n'.format(start_date) + \
                      'end_date ---> {}\n'.format(end_date) + \
                      'start_date > end_date ----> {}'.format(start_date > end_date)
            raise TypeError(message)
