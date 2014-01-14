"""
Settings module holds constants that are used
throughout the PeonOrderSystem project. These
constants represent Settings that could potentially
be adjusted.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""
import re
import string
from datetime import datetime, timedelta, time

SYSTEM_TITLE = 'Fish Cake Factory'

#====================================================================================
# This block represents constants used for Reserver objects and displaying those
# Reserver objects.
#====================================================================================

# in milliseconds, 10 seconds by default
RESERVATION_UPDATE_TIME_FRAME = 1000 * 10
# default is 10 minutes
RESERVATION_NOTIFICATION_TIME_MAX = \
    timedelta(minutes=RESERVATION_UPDATE_TIME_FRAME / 1000)
# in seconds, 0 seconds
RESERVATION_NOTIFICATION_TIME_MIN = timedelta(seconds=0.0)

# notification time frame as str
RESERVATION_NOTIFICATION_TIME_FRAME_STR = \
    str(round(RESERVATION_UPDATE_TIME_FRAME / 1000)) + ' minutes'

#====================================================================================
# This block represents constants used for MenuItem objects and the displaying of
# those MenuItem objects.
#====================================================================================

STANDARD_TEXT = 500
STANDARD_TEXT_BOLD = STANDARD_TEXT + 300
STANDARD_TEXT_LIGHT = STANDARD_TEXT - 300

MENU_ITEM_NON_CONFIRMED_COLOR_HEXADECIMAL = '#000000'
MENU_ITEM_CONFIRMED_COLOR_HEXADECIMAL = '#999999'

#====================================================================================
# This block represents constants that are used in the CheckOperations module,
# these constants effect the process of summing checks.
#====================================================================================
SALES_TAX = .10

#==============================================================================
# This block represents constants that are utilized by the audit dialogs when
# generating audit files.
#==============================================================================
AUDIT_FILE_TYPE = '.xlsx'
CLOSING_AUDIT_DEFAULT_NAME = 'closing_audit'

OPEN_TIME = time.min
CLOSE_TIME = time.max

TIME_GROUPING = timedelta(minutes=15)

#==============================================================================
# This block represents constants that are utilized by the orders area for
# generating displayed information to the user.
#==============================================================================

STANDARD_TABLE_NAME = 'TABLE'
# Expected less than 12 for ease of use.
NUM_OF_TABLES_TO_DISPLAY = 10

#====================================================================================
# This block represents constants that are utilized in the ConfirmationSystem module
# to serialize and display data.
#====================================================================================
TOGO_SEPARATOR = chr(127)
FILE_TYPE_SEPARATOR = '.'

TYPE_SUFFIX_STANDARD_ORDER = FILE_TYPE_SEPARATOR + 'order'
TYPE_SUFFIX_CHECKOUT = FILE_TYPE_SEPARATOR + 'checkout'

FILENAME_PATTERN = re.compile('^(?P<order_name>.*)\[(?P<order_datetime>.*)\](?P<file_type>.*)')
FILENAME_TEMPLATE = '{order_name}[{order_datetime}]{file_type}'

#BLACKLIST REQUIRES THE FOLLOWING CHARACTERS BY DEFAULT
# '\', '[', ']', '.'
FILENAME_BLACKLIST_CHARS = {r'[': chr(1),
                            r']': chr(2),
                            '\\': chr(3),
                            '/': chr(4),
                            ' ': chr(5),
                            '\n': chr(6),
                            FILE_TYPE_SEPARATOR: chr(7)}

TRANSLATION_FROM_CHARS_TO_BLACKLIST_CHARS = string.maketrans(
    ''.join(FILENAME_BLACKLIST_CHARS.keys()),
    ''.join(FILENAME_BLACKLIST_CHARS.values()))

TRANSLATION_FROM_BLACKLIST_CHARS_TO_CHARS = string.maketrans(
    ''.join(FILENAME_BLACKLIST_CHARS.values()),
    ''.join(FILENAME_BLACKLIST_CHARS.keys()))

#====================================================================================
# This block represents constants that are used in Dialog windows and for naming
# conventions.
#====================================================================================
UNDONE_CHECKOUT_SEPARATOR = '***UNDONE CHECKOUT***'

#====================================================================================
# This block contains the schema that are utilized to build the necessary databases.
#====================================================================================

DATE_DATA_COLS = {'Date': 'NUMERIC',
                  'DateNumOfOrders_standard': 'INT',
                  'DateNumOfOrders_togo': 'INT',
                  'DateSubtotal': 'REAL',
                  'DateTax': 'REAL',
                  'DateTotal': 'REAL'}

ORDER_DATA_COLS = {'OrderNumber': 'INT',
                   'OrderDate': 'NUMERIC',
                   'OrderName': 'TEXT',
                   'OrderSubtotal': 'REAL',
                   'OrderTax': 'REAL',
                   'OrderTotal': 'REAL',
                   'OrderHasNotifications': 'INT',
                   'OrderNotifications_json': 'TEXT',
                   'OrderItemFrequency_json': 'TEXT',
                   'OrderType_standard': 'INT',
                   'OrderType_togo': 'INT',
                   'OrderData_json': 'TEXT'}

ITEM_DATA_COLS = {'OrderNumber': 'INT',
                  'ItemName': 'TEXT',
                  'ItemDate': 'NUMERIC',
                  'ItemIsNotification': 'INT',
                  'ItemData_json': 'TEXT'}

RESERVATIONS_DATA_COLS = {'ReservationName': 'TEXT',
                          'ReservationTime': 'NUMERIC',
                          'ReservationNumber': 'TEXT',
                          'ReservationData_json': 'TEXT'}

#====================================================================================
# This block represents constants that are utilized in accordance with time
#====================================================================================
CTIME_STR = "%a %b %d %H:%M:%S %Y"

SQLITE_DATE_TIME_FORMAT_STR = '%Y-%m-%d %H:%M:%S'
SQLITE_DATE_FORMAT_STR = '%Y-%m-%d'

# Based on utilizing stftime, which piggy backs on the time module. Therefore
# times are invalid before or beyond the unix epoch.
MAX_DATETIME = datetime(2038, 1, 1)
MIN_DATETIME = datetime.fromtimestamp(0)

