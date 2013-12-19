"""
Settings module holds constants that are used
throughout the PeonOrderSystem project. These
constants represent Settings that could potentially
be adjusted.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

SYSTEM_TITLE = 'Fish Cake Factory'

#====================================================================================
# This block represents constants used for Reserver objects and displaying those
# Reserver objects.
#====================================================================================

# in milliseconds, 10 minutes default
RESERVATION_UPDATE_TIME_FRAME = 1000 * 10
# in seconds, 12000 sec(20 minutes) default
RESERVATION_NOTIFICATION_TIME_MAX = RESERVATION_UPDATE_TIME_FRAME / 1000 * \
                                      2.0 - 1.0
# in seconds, 0 seconds
RESERVATION_NOTIFICATION_TIME_MIN = 0.0

# notification time frame as str
RESERVATION_NOTIFICATION_TIME_FRAME_STR = \
    str(round(RESERVATION_NOTIFICATION_TIME_MAX / 60)) + ' minutes'

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
TYPE_SUFFIX_STANDARD_ORDER = '.' + 'order'
TYPE_SUFFIX_CHECKOUT = '.' + 'checkout'

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

ITEM_DATA_COLS = {'ItemName': 'TEXT',
                  'ItemDate': 'NUMERIC',
                  'ItemIsNotification': 'INT',
                  'ItemData_json': 'TEXT'}

RESERVATIONS_DATA_COLS = {'ReservationName': 'TEXT',
                          'ReservationTime': 'NUMERIC',
                          'ReservationNumber': 'TEXT',
                          'ReservationData_json': 'TEXT'}
