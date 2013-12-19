"""This module provides functionality for the confirmation system.
Importing the module implicitly builds the necessary directories
to store in the data folder of the project. This import builds 
the following files ontop of data if they do not already exist

'...data/orders/{year}/{month}/{day}/'

All of this modules functions operate on this as the parent
directory. Each time this module is invoked and the year, month
or day changes it instantiates a new directory.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""
import re
import os
import time
import sqlite3
import jsonpickle
from collections import Counter
from src.peonordersystem import path
from src.peonordersystem import MenuItem
from src.peonordersystem import CheckOperations
from src.peonordersystem.Settings import TOGO_SEPARATOR, TYPE_SUFFIX_TOGO, \
    TYPE_SUFFIX_STANDARD_ORDER, TYPE_SUFFIX_CHECKOUT, UNDONE_CHECKOUT_SEPARATOR

jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)

#====================================================================================
# This block represents constants that are utilized throughout the module.
# Furthermore this block also ensures the basic structure of the directories
# necessary for the ConfirmationSystem module to work.
#====================================================================================

DIRECTORY = path.SYSTEM_ORDERS_PATH

ORDERS_DATABASE_PATH = path.SYSTEM_ORDERS_DATABASE
RESERVATIONS_DATABASE_PATH = path.SYSTEM_RESERVATIONS_DATABASE

CONFIRMED_DIRECTORY = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY
CHECKOUT_DIRECTORY = path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY


for dirs in (DIRECTORY, CHECKOUT_DIRECTORY, CONFIRMED_DIRECTORY,
             path.SYSTEM_DATABASE_PATH):
    if not os.path.exists(dirs):
        os.mkdir(dirs)

# Expected to be surrounded by '[', ']' brackets, with any
# valid format for time.strftime function.
STANDARD_TIME_FORMAT = '[%H-%M-%S, %m-%d-%y]'


#====================================================================================
# This block represents the block of code that initializes/sets up the database
# used to store information regarding all previous orders, menu items and other
# information. Each table in the database has a standard schema that is accessible
# through sqlite row objects keys() method.
#
# Orders Database
#
#   The following are the names of the tables set up in the database:
#
#       1. DateData: Represents all Order totals and data (without regard to the
#                specific MenuItems for any order). This is used for quick audits.
#
#       2. OrderData: Represents all potential information regarding any specific
#                 order. Stores the full menu item information for the order in the
#                 OrderData field as a json serialized object.
#
#       3. ItemData: Represents all MenuItems that have been ordered. This stores all
#                information regarding any given MenuItem. This is duplicate data
#                compiled from OrderData tables OrderData.
#
# Reservations Database
#
#       1. ReservationsData: Represents all reservations data that has been
#                            gathered by the UI and stores the data.
#
#====================================================================================
def _check_and_create_orders_database(database_directory=ORDERS_DATABASE_PATH):
    """Checks for the noted tables in the database, if they do not
    exist then they are created.

    @keyword database: database that these tables will be generated
    under. By default is standard ORDERS_DATABASE.

    @return: None
    """
    orders_database = sqlite3.connect(database_directory)
    db = orders_database.cursor()

    db.execute('CREATE TABLE IF NOT EXISTS DateData '
               '    (   Date NUMERIC, '
               '        DateNumOfOrders_standard INT, '
               '        DateNumOfOrders_togo INT, '
               '        DateSubtotal REAL, '
               '        DateTax REAL, '
               '        DateTotal REAL'
               '    );')

    db.execute('CREATE TABLE IF NOT EXISTS OrderData '
               '    (   OrderNumber INT, '
               '        OrderDate NUMERIC, '
               '        OrderName TEXT, '
               '        OrderSubtotal REAL, '
               '        OrderTax REAL, '
               '        OrderTotal REAL, '
               '        OrderHasNotifications INT,'
               '        OrderNotifications_json TEXT, '
               '        OrderItemFrequency_json TEXT,'
               '        OrderType_standard INT,'
               '        Ordertype_togo INT,'
               '        OrderData_json TEXT'
               '    );')

    db.execute('CREATE TABLE IF NOT EXISTS ItemData '
               '    (   ItemName TEXT, '
               '        ItemDate NUMERIC, '
               '        ItemIsNotification INT,'
               '        ItemData_json TEXT'
               '    );')

    orders_database.commit()
    return orders_database


def _check_and_create_reservations_database(directory=RESERVATIONS_DATABASE_PATH):
    """Checks for the noted tables present in the database, if they do not
    exist they are created.

    @keyword directory: str representing the path to which the
    generated database will be or is currently stored. Default
    is the RESERVATIONS_DATABASE_PATH

    @return: sqlite3.Connection pointing to the database.
    """
    reservations_database = sqlite3.connect(directory)
    db = reservations_database.cursor()

    db.execute('CREATE TABLE IF NOT EXISTS ReservationsData '
               '    (   ReservationName TEXT,'
               '        ReservationTime NUMERIC,'
               '        ReservationNumber TEXT,'
               '        ReservationData_json TEXT'
               '    );')

    reservations_database.commit()
    return reservations_database

ORDERS_DATABASE = _check_and_create_orders_database()
RESERVATIONS_DATABASE = _check_and_create_reservations_database()


#====================================================================================
# This block contains functions that are helper functions utilized in interpreting,
# loading and otherwise interacting with the data stored in databases or in the
# directory structure set up by this module. This includes generating and parsing
# standard file names, loading serializable data, and tracking a order number
# counter.
#====================================================================================
def standardize_file_name(order_name, is_checkout=False, set_time=None):
    """Standardizes the name of the file,
    under the standard format for the respective
    orders

    @param order_name: str representing the name
    of the order.

    @keyword is_checkout: bool representing if
    the standardized file name that is generated
    should be one for a checkout order or a
    confirmed order. Default is False.

    @return: str representing the standardized
    file format.
    """
    p = re.compile('[\[\.\s\]]')
    order_name = p.sub('_', order_name)

    if not set_time:
        set_time = time.time()

    order_name += time.strftime(STANDARD_TIME_FORMAT, time.localtime(set_time))

    if is_checkout:
        order_name += TYPE_SUFFIX_CHECKOUT
    elif TOGO_SEPARATOR in order_name:
        order_name += TYPE_SUFFIX_TOGO
    else:
        order_name += TYPE_SUFFIX_STANDARD_ORDER

    return order_name


def parse_standardized_file_name(file_name, togo_separator=' '):
    """Parses the str that represents the
    standard files information that is stored
    as the file name.

    @param file_name: str representing the file
    name that is to be parsed.

    @keyword togo_separator: str representing the character
    to be placed between the name and number representation
    representing the togo name. By default is whitespace. Thus
    'WXYZ 1234' is the standard format.

    @return: tuple of length 3. Representing the
    (time, order_name, type) respectively as three
    str types.

        order_time = float as number of seconds
        since epoch.

        order_name = standard order name

        file_type = checkout, order, togo, or log types
    """
    i = file_name.find('.')
    order_name = file_name[:i]
    file_type = file_name[i:]

    p = re.compile('[\[..\]]')

    i = p.search(order_name).start()
    file_time = order_name[i:]
    file_time = time.mktime(time.strptime(file_time, STANDARD_TIME_FORMAT))

    order_name = order_name[:i]
    order_name = order_name.replace(TOGO_SEPARATOR, togo_separator)
    order_name = order_name.replace('_', ' ')

    return file_time, order_name, file_type


def _load_data(file_path):
    """Loads the json serialized object
    data stored in the given file path.

    @param file_path: str representing
    the directory and filename in standard
    format that is to be opened and have
    its json data decoded.

    @return: object that represents the
    json data that was serialized.
    """
    with open(file_path) as file_data:
        data = file_data.read()
        return jsonpickle.decode(data)


def _find_order_name_paths(order_name, directory):
    """Finds the file paths that are in the specific
    directory and match the given order name without
    reference to their stored time values.

    @param order_name: str representing the order name
    of the stored value that is to be found.

    @return: list of str representing the file paths
    for each of the values that matched the given order
    name.
    """
    p = re.compile('[\[..\]]')
    dirpath, dirnames, filenames = os.walk(directory).next()

    matching_file_paths = []

    for filename in filenames:
        i = re.search(p, filename).start()
        curr_order_name = filename[:i].replace('_', ' ')

        if curr_order_name == order_name:
            matching_file_paths.append(directory + '/' + filename)

    return matching_file_paths


def _get_current_order_number(database=ORDERS_DATABASE):
    """Gets the current order number that is being
    counted. Pulls this data from the database. This
    function may be slow.

    @return: int representing the order number that
    is next.
    """
    db = database.cursor()
    counter = db.execute("SELECT COUNT (*) FROM OrderData")
    return counter.next()[0]

current_order_counter = _get_current_order_number()


#====================================================================================
# This block contains functions that are utilized in the initial set up of the UI
# to retrieve previously unattended data, or to allow for pulling of checkout data
# from the current date only. This occurs primarily if the system has been shut
# off prematurely with orders still present in the confirmed area, or a mistake
# has been made and a previously checked out item needs to be undone.
#====================================================================================
def unpack_order_data():
    """Unpacks the information stored in
    the confirmed order directory.

    @return: 2-tuple of dict types. Each
    dict maps a 2-tuple key to a list of MenuItem
    objects. Each key is a (str, float),
    that represents the name and time of order
    respectively. They are mapped to values that
    represent the order as a list of MenuItem
    objects.
    """
    table_orders = {}
    togo_orders = {}
    itr = os.walk(CONFIRMED_DIRECTORY)

    dirpath, dirnames, filenames = itr.next()

    for filename in filenames:
        order_time, order_name, file_type = parse_standardized_file_name(filename,
            togo_separator=TOGO_SEPARATOR)

        current_order = table_orders
        if file_type == TYPE_SUFFIX_TOGO:
            current_order = togo_orders

        current_order[order_name, order_time] = _load_data(dirpath + '/' + filename)

    return table_orders, togo_orders


def unpack_checkout_data():
    """Unpacks the information stored
    in the checkout area, of the date
    designated

    @return: dict of key (str, float)
    representing the order's associated name and
    the number of seconds since epoch it was checked out at.
    This is mapped to a list of MenuItem objects
    that represents the order.
    """
    checkout_data = {}

    itr = os.walk(CHECKOUT_DIRECTORY)
    dirpath, dirnames, filenames = itr.next()

    for filename in filenames:

        order_time, order_name, file_type = parse_standardized_file_name(filename,
                                                     togo_separator=TOGO_SEPARATOR)
        checkout_data[order_name, order_time] = _load_data(dirpath + '/' + filename)

    return checkout_data


def unpack_reservations_data(date=None):
    """Unpacks the reservation data on
    the specified date.

    @keyword date: float representing the
    number of seconds since unix epoch.

    @return: list of 3-tuple representing
    the name, str and struct_time that
    represents the reservations.
    """
    if not date:
        date = time.time()

    db = RESERVATIONS_DATABASE.cursor()

    data = db.execute('SELECT '
                      '     ReservationData_json '
                      'FROM '
                      '     ReservationsData '
                      'WHERE    '
                      '     date(ReservationTime) = date(?, "unixepoch", "localtime") '
                      'AND  '
                      '     ReservationTime > datetime(?, "unixepoch", "localtime");',
                      ([date for x in range(2)]))
    RESERVATIONS_DATABASE.commit()

    return [jsonpickle.decode(value[0]) for value in data]


#====================================================================================
# This block represents functions that are used for removing data files currently
# stored in the checkout or confirmed areas of the orders directory. As such any
# functions contained here are expected to provide only removal of some piece of
# data.
#====================================================================================
def _remove_order_file(standardized_file_name, directory=CONFIRMED_DIRECTORY):
    """Removes the file associated with the
    confirmed order from the necessary
    directory.

    @param standardized_file_name: str
    representing the name associated with
    the given order. This str is expected
    to have been previously transformed
    to the standardized form.

    @keyword directory: Directory that is
    to be removed from. By default is the
    CONFIRMED_DIRECTORY constant. Alternatively
    may be CHECKOUT_DIRECTORY constant to remove
    the CHECKOUT_DIRECTORY associated file.

    @return: list of MenuItem objects that
    represents the order that was removed.
    """
    file_name = directory + '/' + standardized_file_name
    order_data = _load_data(file_name)

    if os.path.isfile(file_name):
        os.remove(file_name)
    return order_data


def _save_order_file_data(order_data, file_path):
    """Saves the given order data to the given file
    path.

    @param order_data: list of MenuItem objects that
    represents an order.

    @param file_path: str representing the file path
    that the data should be saved as.

    @return: None
    """
    with open(file_path, 'w') as data_file:
        order_data_str = jsonpickle.encode(order_data)
        data_file.write(order_data_str)


def undo_checkout_file(original_checkout_name, checkout_time, new_name):
    """Undoes the given original checkout by removing the data
    from the CHECKOUT_DIRECTORY and storing it in the CONFIRMED_DIRECTORY.

    @param original_checkout_name: str representing the original name
    of the order.

    @param checkout_time: float representing the number of seconds
    since epoch that this original order was checked out at.

    @param new_name: str representing the new name that the
    order should be stored as.

    @return: list of MenuItem objects that represents the
    checkout data that was undone.
    """
    new_name += TOGO_SEPARATOR + UNDONE_CHECKOUT_SEPARATOR
    standardized_name = standardize_file_name(original_checkout_name,
                                              is_checkout=True,
                                              set_time=checkout_time)

    data = _remove_order_file(standardized_name, directory=CHECKOUT_DIRECTORY)
    _save_confirmed_order(data, new_name, CONFIRMED_DIRECTORY)
    return data


#====================================================================================
# This block represents functions that are used to modify and update the databases
# that store the orders information beyond the standard single day period.
#====================================================================================
def update_database():
    """Updates the databases to include
    all currently checked out information.
    Information is pulled from the
    CHECKOUT_DIRECTORY and added to the
    the databases.

    @warning: This method may be slow and
    should only be performed at infrequent
    instances. Preferably at a time when
    the process would have adequate time
    to complete.

    @return: None
    """
    date = time.localtime()
    dirpath, dirnames, filenames = os.walk(CHECKOUT_DIRECTORY).next()

    for filename in filenames:
        order_time, order_name, file_type = parse_standardized_file_name(filename)
        order_data = _load_data(dirpath + '/' + filename)

        for item in _update_order_table(order_time, order_data, order_name):
            _update_item_table(order_time, item)

        _remove_order_file(filename, directory=dirpath)

    _update_date_table(date)


def _update_date_table(date, database=ORDERS_DATABASE):
    """Updates the date database to store the respective data given.

    @param date: float that represents the number of seconds
    since the epoch.

    @keyword database: sqlite3.connection that represents
    the database that has been opened. By default this
    is the ORDERS_DATABASE for the module. Expected database
    schema is:

        Date NUMERIC,
        DateNumOfOrders_standard INT,
        DateNumOfOrders_togo INT,
        DateSubtotal REAL,
        DateTax REAL,
        DateTotal REAL

    @warning: Relies heavily on OrderData table to generate
    its information. This function will not operate appropriately
    without a OrderData table present in its database connection.

    @return: None
    """
    date = time.localtime(date)
    data = [sqlite3.datetime.date(date[0], date[1], date[2]) for x in range(6)]
    db = database.cursor()
    db.execute('INSERT OR REPLACE INTO DateData '
               '     VALUES '
               '         (  ?, '
               '            (   SELECT SUM(OrderType_standard) '
               '                FROM OrderData '
               '                WHERE date(OrderDate)=?'
               '             ), '
               '            (   SELECT SUM(OrderType_togo) '
               '                FROM OrderData '
               '                WHERE date(OrderDate)=?'
               '            ), '
               '            (   SELECT SUM(OrderSubtotal) '
               '                FROM OrderData '
               '                WHERE date(OrderDate)=?'
               '            ), '
               '            (   SELECT SUM(OrderTax) '
               '                FROM OrderData '
               '                WHERE date(OrderDate)=?'
               '            ), '
               '            (   SELECT SUM(OrderTotal) '
               '                FROM OrderData '
               '                WHERE date(OrderDate)=?'
               '            )'
               '         );', tuple(data))
    database.commit()


def _update_order_table(date, order_data, order_name, database=ORDERS_DATABASE):
    """Updates the order data table that displays information
    on orders made.

    @param date: float representing the number of seconds
    since the epoch.

    @param order_data: list of MenuItem objects that
    represents this order that was checked out.

    @param order_name: str representing the name of this
    order.

    @keyword database: sqlite3.connection object that represents
    the database that the data will be added to. Expected column
    values for this database are:

        OrderNumber INT,
        OrderDate NUMERIC,
        OrderSubtotal REAL,
        OrderTax REAL,
        OrderTotal REAK,
        OrderHasNotification INT (bool),
        OrderNotificationData_json TEXT,
        OrderItemFrequency_json TEXT,
        OrderType_standard INT (bool),
        OrderType_togo INT (bool),
        OrderData_json TEXT

    @return: returns a generator that iterates over the yield
    data.

    @yield: Yields every MenuItem that was stored in the order
    data.
    """
    subtotal = CheckOperations.get_order_subtotal(order_data)
    tax = CheckOperations.get_total_tax(subtotal)
    total = CheckOperations.get_total(order_data)

    notification_data = []
    item_frequency = Counter()

    is_standard = True
    is_togo = False

    if TOGO_SEPARATOR in order_name:
        is_togo = True
        is_standard = False

    for menu_item in order_data:
        item_frequency[menu_item.get_name()] += 1
        if menu_item.is_notification():
            notification_data.append(menu_item)

        yield menu_item

    data = (current_order_counter,
            date,
            order_name,
            subtotal,
            tax,
            total,
            len(notification_data) > 0,
            jsonpickle.encode(notification_data),
            jsonpickle.encode(item_frequency),
            is_standard,
            is_togo,
            jsonpickle.encode(order_data))

    db = database.cursor()
    db.execute('INSERT INTO OrderData '
               '    VALUES'
               '        (   ?, '
               '            datetime(?, "unixepoch", "localtime"),'
               '            ?, '
               '            ?, '
               '            ?, '
               '            ?, '
               '            ?, '
               '            ?, '
               '            ?, '
               '            ?, '
               '            ?, '
               '            ?'
               '        );', data)
    database.commit()


def _update_item_table(date, menu_item, database=ORDERS_DATABASE):
    """Updates the item table data that stores item data.

    @param date: float representing the number of seconds
    since the epoch.

    @param menu_item: MenuItem object that represents a
    MenuItem that is to be stored in the table.

    @param database: sqlite3.Connection object that
    represents the database that the data will be stored
    in. Expected column values:

        ItemName TEXT,
        ItemDate NUMERIC,
        ItemIsNotification INT (bool),
        ItemData_json TEXT

    @return: None
    """
    data = (menu_item.get_name(),
            date,
            jsonpickle.encode(menu_item),
            menu_item.is_notification())

    db = database.cursor()
    db.execute('INSERT INTO ItemData '
               '    VALUES'
               '        (   ?, '
               '            datetime(?, "unixepoch", "localtime"), '
               '            ?, '
               '            ?'
               '        );', data)
    database.commit()


def add_reservation_to_database(reserver, database=RESERVATIONS_DATABASE):
    """Adds the given reservation to the database.

    @param reserver: Reserver object that
    represents the reservation that it to be
    added.

    @return: None
    """
    name = reserver.name
    number = reserver.number
    arrival_time = reserver.get_arrival_time()

    reserver_data_json = jsonpickle.encode(reserver)

    data = (name,
            time.mktime(arrival_time),
            number,
            reserver_data_json)

    db = database.cursor()
    db.execute('INSERT INTO ReservationsData'
               '    VALUES (    ?,'
               '                datetime(?, "unixepoch", "localtime"),'
               '                ?,'
               '                ?'
               '           );', data)
    database.commit()


#====================================================================================
# This blocks represents functions that are used for temporary storage prior to
# being processed by the databases. These functions are used to store their
# respective data in the respective areas.
#====================================================================================
def order_confirmed(order_name, priority_list,
                    non_priority_list, full_order):
    """Confirms an order by dumping a binary
    file representing the confirmed order into
    the parent directories confirmed folder.

    @param order_name: str representing the name of the
    order

    @param priority_list: list of MenuItem objects that
    represents the associated priority order

    @param non_priority_list: list of MenuItems objects that
    do not have priority.

    @param full_order: list of MenuItem objects that includes
    previous confirmed and non-kitchen MenuItem objects. This
    is included for purposes of printing and retrieving
    accurate data.
    """
    for file_paths in _find_order_name_paths(order_name, CONFIRMED_DIRECTORY):
        os.remove(file_paths)

    _save_confirmed_order(full_order, order_name, directory=CONFIRMED_DIRECTORY)
    print_order(order_name, non_priority_list, priority_list=priority_list)


def _save_confirmed_order(order_data, order_name, directory=CONFIRMED_DIRECTORY,
                           set_time=None):
    """Standardizes the file name and saves it in the
    given directory.

    @param order_data: list of MenuItem objects that represents the order.

    @param order_name: str representing the order. This string will be
    standardized and shouldn't contain the following characters:

        [ ] / .

    @keyword directory: str representing the path to the
    directory that the file will be saved to.

    @return: None
    """
    is_checkout = directory == CHECKOUT_DIRECTORY
    order_name = standardize_file_name(order_name, is_checkout=is_checkout,
                                       set_time=set_time)
    _save_order_file_data(order_data, directory + '/' + order_name)


def checkout_confirmed(order_name, orders, order_list):
    """Generates the necessary checkout files
    and adds the given order to that file for
    storage. This is utilized later.

    @param order_name: str representing the name
    associated with the given order.

    @param orders: n-tuple that comprises a order.
    This tuple structure allows for n subdivided
    checks to be sent to the checkout confirmation
    if there was a split operation performed. If
    no split operation was performed then expect
    a single entry for the order.

    @param order_list: list of MenuItem objects
    that comprises the total order. This is utilized
    for logging purposes.
    """
    for file_paths in _find_order_name_paths(order_name, CONFIRMED_DIRECTORY):
        os.remove(file_paths)

    _save_confirmed_order(order_list, order_name, directory=CHECKOUT_DIRECTORY)
    print_check(order_name, order_list)


#====================================================================================
# This block represents functions that are used to send the data to external
# procedures such as printing.
#====================================================================================
def print_order(order_name, order_list, priority_list=None):
    """Send the given order to the order
    printer. If given a priority order the
    priority order is given special priority
    status and printed first. The remaining
    order is printed last.

    @param order_name: str representation of
    the order.

    @param order_list: list of MenuItem objects
    that represents the order to be sent to the
    order printer.

    @keyword priority_list: list of MenuItem
    objects that represents the priority order to
    be sent to the order printer.

    @return: None
    """
    #TODO print order to order printer
    print 'TO ORDER'
    print order_name
    if priority_list:
        print priority_list

    print order_list
    print ''


def print_check(order_name, order_list):
    """Send the given order to the check
    printer.

    @param order_name: str representation
    of the orders name

    @param order_list: list of MenuItem objects
    that is to be printed to the check printer.

    @return: None
    """
    #TODO send order to checkout printer
    print 'TO CHECK'
    print order_name
    print order_list
    print''

    subtotal = CheckOperations.get_order_subtotal(order_list)

    print 'Subtotal : ' + str(subtotal)
    print 'Tax : ' + str(CheckOperations.get_total_tax(subtotal))
    print 'Total : ' + str(CheckOperations.get_total(order_list))


if __name__ == "__main__":
    update_database()

