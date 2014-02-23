"""This module provides functionality for the confirmation system.
Importing the module implicitly builds the necessary directories
to store in the data folder of the project.

The ConfirmationSystem is built on two principles.

First a standard human readable confirmation/checkout system
incase of system failure exists in the orders area of the data.

Second a database that stores the data after it has been used
and is no longer necessary to have around. This is for later
usage.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""
import os
import sqlite3
import jsonpickle
from datetime import datetime
from collections import Counter

import SystemPath
from src.peonordersystem.confirmationSystem.bundlers.DateDataBundle \
    import DateDataBundle
from src.peonordersystem.confirmationSystem.bundlers.ItemDataBundle \
    import ItemDataBundle
from src.peonordersystem.confirmationSystem.bundlers.OrderDataBundle \
    import OrderDataBundle
from src.peonordersystem import CheckOperations
from src.peonordersystem.standardoperations import (check_date,
                                                    check_datetime,
                                                    check_date_range,
                                                    check_datetime_range,
                                                    check_directory,
                                                    check_database)
from src.peonordersystem.Settings import (TOGO_SEPARATOR,
                                          TYPE_SUFFIX_STANDARD_ORDER,
                                          TYPE_SUFFIX_CHECKOUT,
                                          UNDONE_CHECKOUT_SEPARATOR,
                                          SQLITE_DATE_TIME_FORMAT_STR,
                                          SQLITE_DATE_FORMAT_STR,
                                          TRANSLATION_FROM_BLACKLIST_CHARS_TO_CHARS
                                          as BLACKLIST_TO_CHARS,
                                          TRANSLATION_FROM_CHARS_TO_BLACKLIST_CHARS
                                          as CHARS_TO_BLACKLIST,
                                          FILENAME_PATTERN,
                                          FILENAME_TEMPLATE)


jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)

#====================================================================================
# This block represents constants that are utilized throughout the module.
# Furthermore this block also ensures the basic structure of the directories
# necessary for the ConfirmationSystem module to work.
#====================================================================================

DIRECTORY = SystemPath.SYSTEM_ORDERS_PATH

ORDERS_DATABASE_PATH = SystemPath.SYSTEM_ORDERS_DATABASE
RESERVATIONS_DATABASE_PATH = SystemPath.SYSTEM_RESERVATIONS_DATABASE

CONFIRMED_DIRECTORY = SystemPath.SYSTEM_ORDERS_CONFIRMED_DIRECTORY
CHECKOUT_DIRECTORY = SystemPath.SYSTEM_ORDERS_CHECKOUT_DIRECTORY


for dirs in (DIRECTORY, CHECKOUT_DIRECTORY, CONFIRMED_DIRECTORY,
             SystemPath.SYSTEM_DATABASE_PATH):
    if not os.path.exists(dirs):
        os.mkdir(dirs)

# Expected to be surrounded by '[', ']' brackets, with any
# valid format for time.strftime function.
STANDARD_TIME_FORMAT = SQLITE_DATE_TIME_FORMAT_STR

# global module wide variable utilized for counting the number of orders.
global current_order_counter


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
#                specific MenuItems for any order).
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
               '        DateTotal REAL,'
               '        PRIMARY KEY (Date)'
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
               '        OrderType_togo INT,'
               '        OrderData_json TEXT,'
               '        PRIMARY KEY (OrderNumber)'
               '    );')

    db.execute('CREATE TABLE IF NOT EXISTS ItemData '
               '    (   OrderNumber INT,'
               '        ItemName TEXT, '
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
    if not order_name:
        raise ValueError('Cannot standardize empty order name')

    try:
        check_datetime(set_time)
    except ValueError:
        set_time = datetime.now()

    order_name = order_name.translate(CHARS_TO_BLACKLIST)

    if is_checkout:
        file_type = TYPE_SUFFIX_CHECKOUT
    else:
        file_type = TYPE_SUFFIX_STANDARD_ORDER

    data = {'name': order_name,
            'timestamp': set_time.strftime(STANDARD_TIME_FORMAT),
            'file_type': file_type}

    return FILENAME_TEMPLATE.format(**data)


def parse_standardized_file_name(file_name, togo_separator=' '):
    """Parses the str that represents the
    standard files information that is stored
    as the file name.

    @param file_name: str representing the file
    name that is to be parsed. This file name should
    have been processed through the BLACKLIST translator
    at some time.

    @keyword togo_separator: str representing the character
    to be placed between the name and number representation
    representing the togo name. By default is whitespace. Thus
    'WXYZ 1234' is the standard format.

    @return: tuple of length 3. Representing the
    (time, order_name, type) respectively as three
    str types.

        order_time = datetime object representing
        the orders date and time.

        order_name = standard order name

        file_type = checkout, order, togo, or log types
    """
    is_parseable_file_name(file_name)
    match = FILENAME_PATTERN.match(file_name)
    order_data = match.groupdict()
    order_datetime = datetime.strptime(order_data['timestamp'], STANDARD_TIME_FORMAT)

    order_name = order_data['name'].translate(BLACKLIST_TO_CHARS)

    return order_datetime, order_name, order_data['file_type']


def is_parseable_file_name(file_name):
    """Checks if the given file name is
    parseable.

    @raise ValueError: if the file name
    is not parseable in accordance with
    the FILENAME_PATTERN

    @param file_name: object to be tested.

    @return: bool value representing if
    the test was passed.
    """
    if not FILENAME_PATTERN.match(file_name):
        raise ValueError("Cannot parse the given standardized name."
                         " It doesn't match the template.")
    return True


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
    is_parseable_file_name(file_path)
    with open(file_path, 'r') as file_data:
        data = file_data.read()
        return jsonpickle.decode(data)


def _find_order_name_paths(order_name, directory):
    """Finds the file paths that are in the specific
    directory and match the given order name without
    reference to their stored time values.

    @param order_name: str representing the order name
    of the stored value that is to be found.

    @param directory: str representing the file path
    of the directory to be searched.

    @return: list of str representing the file paths
    for each of the values that matched the given order
    name.
    """
    check_directory(directory)
    std_name = standardize_file_name(order_name)
    order_time, order_name, file_type = parse_standardized_file_name(std_name)

    dirpath, dirnames, filenames = os.walk(directory).next()

    matching_file_paths = []

    for filename in filenames:
        try:
            order_time, name, file_type = parse_standardized_file_name(filename)
            if name == order_name:
                matching_file_paths.append(directory + '/' + filename)

        except ValueError:
            pass

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
def unpack_order_data(directory=CONFIRMED_DIRECTORY):
    """Unpacks the information stored in
    the confirmed order directory.

    @keyword directory: str representing the
    directory from which the data should be pulled.

    @return: 2-tuple of dict types. Each
    dict maps a 2-tuple key to a list of MenuItem
    objects. Each key is a (str, float),
    that represents the name and time of order
    respectively. They are mapped to values that
    represent the order as a list of MenuItem
    objects.
    """
    check_directory(directory)
    table_orders = {}
    togo_orders = {}
    itr = os.walk(directory)

    dirpath, dirnames, filenames = itr.next()

    for name in filenames:
        try:
            order_time, order_name, file_type = parse_standardized_file_name(name,
                togo_separator=TOGO_SEPARATOR)

            current_order = table_orders
            if TOGO_SEPARATOR in order_name:
                current_order = togo_orders

            file_path = dirpath + '/' + name
            current_order[order_name, order_time] = _load_data(file_path)

        except ValueError:
            pass

    return table_orders, togo_orders


def unpack_checkout_data():
    """Unpacks the information stored
    in the checkout area, of the date
    designated

    @return: dict of key (str, datetime)
    repersenting the name and time of order.
    This is mapped to values of list representing
    the order. All togo and orders data is combined.
    """
    order_data, togo_data = unpack_order_data(CHECKOUT_DIRECTORY)
    # Expect each value to have unique key. Regardless of duplicate names time and
    # name duplicates are impossible.
    order_data.update(togo_data)
    return order_data


def unpack_reservations_data(curr_date=None, database=RESERVATIONS_DATABASE):
    """Unpacks the reservation data on
    the specified date.

    @keyword curr_date: datetime object representing
    the selected date that the data should be
    pulled from. All reservations that are pulled
    will be only those which exceed the datetime.

    @return: list of Reserver objects that represents
    the reservations that are greater than the given
    datetime but are expected on the date.
    """
    check_database(database)
    try:
        check_datetime(curr_date)

    except ValueError:
        curr_date = datetime.now()

    db = database.cursor()

    data = db.execute('SELECT '
                      '     ReservationData_json '
                      'FROM '
                      '     ReservationsData '
                      'WHERE    '
                      '     date(ReservationTime) = date(?) '
                      'AND  '
                      '     ReservationTime >= datetime(?)'
                      'ORDER BY'
                      '     ReservationTime;',
                      (curr_date.strftime(SQLITE_DATE_FORMAT_STR),
                       curr_date.strftime(SQLITE_DATE_TIME_FORMAT_STR)))
    database.commit()

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
    is_parseable_file_name(standardized_file_name)
    check_directory(directory)

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
    is_parseable_file_name(file_path)
    with open(file_path, 'w') as data_file:
        order_data_str = jsonpickle.encode(order_data)
        data_file.write(order_data_str)


def undo_checkout_file(original_checkout_name, checkout_time, new_name):
    """Undoes the given original checkout by removing the data
    from the CHECKOUT_DIRECTORY and storing it in the CONFIRMED_DIRECTORY.

    @param original_checkout_name: str representing the original name
    of the order.

    @param checkout_time: datetime object representing the time
    of the initial checkout.

    @param new_name: str representing the new name that the
    order should be stored as.

    @return: 2 tuple representing the file_path and a
    list of items that represents the undone checkout
    respectively.
    """
    check_datetime(checkout_time)
    new_name += TOGO_SEPARATOR + UNDONE_CHECKOUT_SEPARATOR
    standardized_name = standardize_file_name(original_checkout_name,
                                              is_checkout=True,
                                              set_time=checkout_time)

    data = _remove_order_file(standardized_name, directory=CHECKOUT_DIRECTORY)
    file_name = _save_confirmed_order(data, new_name, CONFIRMED_DIRECTORY)
    return CONFIRMED_DIRECTORY + '/' + file_name, data


#====================================================================================
# This block represents functions that are used to modify and update the databases
# that store the orders information beyond the standard single day period.
#====================================================================================
def update_orders_database(database=ORDERS_DATABASE):
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
    dates_list = set()
    dirpath, dirnames, filenames = os.walk(CHECKOUT_DIRECTORY).next()

    for filename in filenames:
        try:
            order_time, order_name, file_type = parse_standardized_file_name(filename)
            order_data = _load_data(dirpath + '/' + filename)

            order_item_frequency = Counter()
            order_notification_data = []

            for menu_item in order_data:
                _update_item_table(order_time, menu_item, database=database)

                order_item_frequency[menu_item.get_name()] += 1

                if menu_item.is_notification():
                    order_notification_data.append(menu_item)

            _update_order_table(order_time, order_data, order_name,
                                order_notification_data, order_item_frequency,
                                database=database)

            _remove_order_file(filename, directory=dirpath)

            dates_list.add(order_time)

        except ValueError:
            pass

    for curr_date in dates_list:
        _update_date_table(curr_date, database=database)


def _update_date_table(curr_date, database=ORDERS_DATABASE):
    """Updates the date database to store the respective data given.

    @param curr_date: datetime object that represents the datetime
    for the given date update.

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
    check_date(curr_date)
    dates = sqlite3.datetime.date(curr_date.year, curr_date.month, curr_date.day)
    db = database.cursor()

    order_data = db.execute('SELECT '
                            '       SUM(OrderType_standard),'
                            '       SUM(OrderType_togo),'
                            '       SUM(OrderSubtotal),'
                            '       SUM(OrderTax),'
                            '       SUM(OrderTotal)'
                            'FROM '
                            '       OrderData '
                            'WHERE '
                            '       date(OrderDate)=?;', (dates,))
    data = order_data.fetchall()

    if len(data) > 1 or not(data[0] == (None, None, None, None, None)):
        for curr_data in data:
            db.execute('INSERT OR REPLACE INTO DateData (   Date,'
                       '                                    DateNumOfOrders_standard,'
                       '                                    DateNumOfOrders_togo,'
                       '                                    DateSubtotal,'
                       '                                    DateTax,'
                       '                                    DateTotal'
                       '                                ) '
                       '    VALUES (   ?, ?, ?, ?, ?, ?);', (dates,) + curr_data)
    database.commit()

    return (str(dates), ) + data[0]


def _update_order_table(curr_date, order_data, order_name, notification_data,
                        item_frequency, database=ORDERS_DATABASE):
    """Updates the order data table that displays information
    on orders made.

    @param curr_date: datetime object that
    represents the date of the order.

    @param order_data: list of MenuItem objects that
    represents this order that was checked out.

    @param order_name: str representing the name of this
    order.

    @keyword database: sqlite3.connection object that represents
    the database that the data will be added to. Expected column
    values for this database are:

        OrderNumber INT,
        OrderDate NUMERIC,
        OrderName,
        OrderSubtotal REAL,
        OrderTax REAL,
        OrderTotal REAL,
        OrderHasNotification INT (bool),
        OrderNotificationData_json TEXT,
        OrderItemFrequency_json TEXT,
        OrderType_standard INT (bool),
        OrderType_togo INT (bool),
        OrderData_json TEXT

    @return: tuple representing the entries
    placed in the table.
    """
    check_datetime(curr_date)
    global current_order_counter

    if not order_data:
        raise ValueError('Expected list of MenuItems for order data. Got empty '
                         'list or none type instead.')

    subtotal = CheckOperations.get_order_subtotal(order_data)
    tax = CheckOperations.get_total_tax(subtotal)
    total = CheckOperations.get_total(order_data)

    is_standard = True
    is_togo = False

    if TOGO_SEPARATOR in order_name:
        is_togo = True
        is_standard = False

    data = (current_order_counter,
            curr_date.strftime(SQLITE_DATE_TIME_FORMAT_STR),
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

    current_order_counter += 1

    db = database.cursor()
    db.execute('INSERT INTO OrderData '
               '    VALUES'
               '        (   ?, '
               '            datetime(?),'
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

    return data


def _update_item_table(curr_date, menu_item, database=ORDERS_DATABASE):
    """Updates the item table data that stores item data.

    @param curr_date: datetime object that represents the
    MenuItems associated datetime of order.

    @param menu_item: MenuItem object that represents a
    MenuItem that is to be stored in the table.

    @param database: sqlite3.Connection object that
    represents the database that the data will be stored
    in. Expected column values:

        OrderNumber INT,
        ItemName TEXT,
        ItemDate NUMERIC,
        ItemIsNotification INT (bool),
        ItemData_json TEXT

    @return: tuple representing the entries
    placed in the table.
    """
    check_datetime(curr_date)
    data = (current_order_counter,
            menu_item.get_name(),
            curr_date.strftime(SQLITE_DATE_TIME_FORMAT_STR),
            int(menu_item.is_notification()),
            jsonpickle.encode(menu_item))
    db = database.cursor()
    db.execute('INSERT INTO ItemData '
               '    VALUES'
               '        (   ?, '
               '            ?, '
               '            datetime(?), '
               '            ?, '
               '            ? '
               '        );', data)
    database.commit()

    return data


def add_reservation_to_database(reserver, database=RESERVATIONS_DATABASE):
    """Adds the given reservation to the database.

    @param reserver: Reserver object that
    represents the reservation that it to be
    added.

    @return: None
    """
    name = reserver.name
    number = reserver.number
    arrival_time = reserver._arrival_time
    reserver_data_json = jsonpickle.encode(reserver)

    data = (name,
            arrival_time.strftime(SQLITE_DATE_TIME_FORMAT_STR),
            number,
            reserver_data_json)

    db = database.cursor()
    db.execute('INSERT INTO ReservationsData'
               '    VALUES (    ?,'
               '                datetime(?),'
               '                ?,'
               '                ?'
               '           );', data)
    database.commit()


#====================================================================================
# This block represents function that are used to retrieve data from the specific
# databases.
#====================================================================================
def get_stored_date_data(start_date, end_date, database=ORDERS_DATABASE):
    """Gets the stored date data that is stored
    in the given database between the given datetime
    ranges, inclusive.

    @param start_date: datetime.datetime object
    that represents the starting date for the
    range, inclusive.

    @param end_date: datetime.datetime object
    that represents the ending date for the
    range, inclusive.

    @param database: sqlite3.Connection that represents
    the database that is to have the data pulled from
    it.

    @return: Generator

    @yield: DateDataBundle that represents the
    data at any given date sorted by date.
    """
    check_date_range(start_date, end_date)
    check_database(database)
    c = database.cursor()

    dates = (start_date.strftime(SQLITE_DATE_FORMAT_STR),
             end_date.strftime(SQLITE_DATE_FORMAT_STR))

    row_data = c.execute('SELECT '
                         '     * '
                         'FROM '
                         '     DateData '
                         'WHERE '
                         '     Date >= ? '
                         ' AND '
                         '     Date <= ? '
                         'ORDER BY '
                         '     Date;', dates)

    for data in row_data:
        yield DateDataBundle(data)


def get_stored_order_data(start_date, end_date, database=ORDERS_DATABASE):
    """Gets the stored order data that is stored
    in the given database, between the given datetime
    ranges, inclusive.

    @param start_date: datetime.datetime object
    that represents the starting datetime for the
    range.

    @param end_date: datetime.datetime object that
    represents the ending datetime for the range.

    @keyword database: Testing parameter. Database
    for the data to be pulled from. By default is
    ORDERS_DATABASE.

    @return: Generator

    @yield: OrderDataBundle objects that represent
    rows in sorted order by date.
    """
    check_datetime_range(start_date, end_date)
    check_database(database)
    c = database.cursor()

    dates = (start_date.strftime(SQLITE_DATE_TIME_FORMAT_STR),
             end_date.strftime(SQLITE_DATE_TIME_FORMAT_STR))

    row_data = c.execute('SELECT '
                         '      * '
                         'FROM '
                         '      OrderData '
                         'WHERE '
                         '      OrderDate >= ? '
                         '  AND '
                         '      OrderDate <= ? '
                         'ORDER BY '
                         '      OrderDate;', dates)
    for data in row_data:
        yield OrderDataBundle(data)


def get_stored_item_data(start_date, end_date, database=ORDERS_DATABASE):
    """Gets the stored item data that is
    stored in the given database, between
    the given time range, inclusive.

    @param start_date: datetime.datetime object
    that represents the starting date for
    the range of items to be selected. Inclusive.

    @param end_date: datetime.datetime object
    that represents the ending date for the
    range of items to be selected. Inclusive.

    @keyword database: Testing keyword argument.
    Default is ORDERS_DATABASE

    @return: Generator

    @yield: ItemDataBundle that represents the
    data at any given row ordered by the date.
    """
    check_datetime_range(start_date, end_date)
    check_database(database)
    c = database.cursor()

    dates = (start_date.strftime(SQLITE_DATE_TIME_FORMAT_STR),
             end_date.strftime(SQLITE_DATE_TIME_FORMAT_STR))

    row_data = c.execute('SELECT '
                          '      * '
                          'FROM '
                          '      ItemData '
                          'WHERE '
                          '      ItemDate >= ? '
                          '  AND '
                          '      ItemDate <= ? '
                          'ORDER BY '
                          '      ItemDate;', dates)

    for data in row_data:
        yield ItemDataBundle(data)

#====================================================================================
# This blocks represents functions that are used for temporary storage prior to
# being processed by the databases. These functions are used to store their
# respective data in the respective areas.
#====================================================================================
def order_confirmed(order_name, priority_list, non_priority_list, full_order,
                    set_time=None):
    """Confirms an order by dumping the data into a text
    file that will be utilized at a later time. This text
    file will be pickled into json using jsonpickle.

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

    print_order(order_name, non_priority_list, priority_list=priority_list)
    return _save_confirmed_order(full_order, order_name,
                                 directory=CONFIRMED_DIRECTORY, set_time=set_time)


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
    is_checkout = (directory == CHECKOUT_DIRECTORY)
    order_name = standardize_file_name(order_name, is_checkout=is_checkout,
                                       set_time=set_time)
    _save_order_file_data(order_data, directory + '/' + order_name)
    return order_name


def checkout_confirmed(order_name, orders, order_list, set_time=None):
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

    print_check(order_name, orders)
    return _save_confirmed_order(order_list, order_name, directory=CHECKOUT_DIRECTORY,
                                 set_time=set_time)


#====================================================================================
# This block represents functions that are used to send the data to external
# procedures such as printing.
#====================================================================================
def print_order(order_name, order_list, priority_list=None, print_data=False):
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
    if print_data:
        print 'TO ORDER'
        print order_name
        if priority_list:
            print priority_list

        print order_list
        print ''


def print_check(order_name, order_data, print_data=False):
    """Send the given order to the check
    printer.

    @param order_name: str representation
    of the orders name

    @param order_list: list where each index
    represents a list of Menuitem objects
    that represents an order.

    @return: None
    """
    #TODO send order to checkout printer
    for order in order_data:
        if print_data:
            print 'TO CHECK'
            print order_name
            print order
            print''

            subtotal = CheckOperations.get_order_subtotal(order)

            print 'Subtotal : ' + str(subtotal)
            print 'Tax : ' + str(CheckOperations.get_total_tax(subtotal))
            print 'Total : ' + str(CheckOperations.get_total(order))