"""This module defines custom exceptions that may be thrown in the
PeonOrderSystem project. This module holds multiple classes that
define the exceptions that can be thrown.

@group Non-Fatal Errors: This group contains every non-fatal error
for the PeonOrderSystem project. Each Non-Fatal Error is designed
to be caught by the PeonOrderSystem and reported to the user in
real time.

@author: Carl McGraw
@contact: cjmcgraw@uw.edu
@version: 1.0
"""
import json
from path import NON_FATAL_ERROR_MESSAGES_DATA as ERROR_FILE

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