"""This module is designed to test the ConfirmationSystem module.

Importing this module will cause several initial tests to execute.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""

import os
import bisect
import shutil
import random
import string
import unittest
import jsonpickle

jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)

from collections import Counter
from datetime import date, time, datetime, timedelta


from src.peonordersystem import path
from src.peonordersystem.MenuItem import MenuItem, DiscountItem
from src.peonordersystem.interface.Reservations import Reserver
from src.peonordersystem.Settings import (TOGO_SEPARATOR,
                                          TYPE_SUFFIX_CHECKOUT,
                                          TYPE_SUFFIX_STANDARD_ORDER,
                                          DATE_DATA_COLS,
                                          ORDER_DATA_COLS,
                                          ITEM_DATA_COLS,
                                          RESERVATIONS_DATA_COLS,
                                          SQLITE_DATE_TIME_FORMAT_STR,
                                          SQLITE_DATE_FORMAT_STR,
                                          FILENAME_BLACKLIST_CHARS as BLACKLIST,
                                          MAX_DATETIME,
                                          MIN_DATETIME)


TABS = '    '
POSSIBLE_CHARS = string.printable * 10 + TOGO_SEPARATOR * 6
NUMBER_OF_ITEMS_TO_GENERATE = 50

#====================================================================================
#====================================================================================
# Initialization testing for the initialization of the module. This section tests
# that the module correctly creates all the necessary information for the system
# when it is imported.
#
# This requires the initial clearing of the data areas prior to initialization.
#
# Case 1:
#
#   Checks for creation of the Confirmed orders area having been generated.
#
# Case 2:
#
#   Checks for creation of the Checkout orders area having been generated.
#
# Case 3:
#
#   Checks for the creation of the databases and the database area.
#
#====================================================================================
#====================================================================================
# Generating initial set up for testing database generation
#====================================================================================
if os.path.exists(path.SYSTEM_DATABASE_PATH):
    shutil.rmtree(path.SYSTEM_DATABASE_PATH)
if os.path.exists(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY):
    shutil.rmtree(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY)
if os.path.exists(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY):
    shutil.rmtree(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY)

from src.peonordersystem import ConfirmationSystem

#====================================================================================
# Case 1: Testing creation of the Confirmed directory.
#====================================================================================
assert (os.path.exists(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY))

#====================================================================================
# Case 2: Testing for creation of the Checkout directory.
#====================================================================================
assert (os.path.exists(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY))

#====================================================================================
# Case 3: Testing for creation of database directory, and creation of both
# reservations and orders databases
#====================================================================================
assert (os.path.exists(path.SYSTEM_DATABASE_PATH))
assert (os.path.exists(path.SYSTEM_ORDERS_DATABASE))
assert (os.path.exists(path.SYSTEM_RESERVATIONS_DATABASE))


#====================================================================================
# This area contains module wide functions and constants that are used for testing
# purposes.
#====================================================================================
def _add_data_to_file(order_data, file_path):
    """Adds the given data to the given file path
    overwriting any data the currently exists.

    The given data will be written by utilizing
    jsonpickle to serialize the data.

    @param order_data: data to be serialized.

    @param file_path: str representing the path
    of the file to be saved to.

    @return: data that was saved to the file,
    as it would return from decoding it from
    the file.
    """
    data = jsonpickle.encode(order_data)
    with open(file_path, 'w') as f:
        f.write(data)

    return jsonpickle.decode(data)


def _add_order_data_to_database(order_data, database):
    """Adds the given order data to the given database.

    @param order_data: values that are generated from
    the populate_directory_with_random_orders function.
    Specifically expecting a list of tuples, where each
    tuple is a (str, str, list of MenuItems) representing
    the standardized name, file path and order data
    respectively.

    @param database: sqlite3.connection object that
    represents the database to have the order added.

    @return: tuple representing the data that was
    stored in the database. Each entry represents
    the column
    """
    data = []

    for std_name, file_path, file_data in order_data:

        f_time, f_name, f_type = \
            ConfirmationSystem.parse_standardized_file_name(std_name)

        notification_data = []
        item_frequency = Counter()

        for menu_item in file_data:
            item_frequency[menu_item.get_name()] += 1

            if menu_item.is_notification():
                notification_data.append(menu_item)

        curr_data = ConfirmationSystem._update_order_table(f_time, file_data, f_name,
                        notification_data, item_frequency, database=database)

        data.append(curr_data)

    return data


def _get_data_from_file(file_path):
    """Gets the data from the file and decodes
    it using jsonpickle.

    The given file path will be read and any
    data contained will be decoded and returned.

    @param file_path: file path of file that
    stores serialized json data.

    @return: decoded data that was stored
    in the object.
    """
    with open(file_path, 'r') as f:
        return jsonpickle.decode(f.read())


def _generate_random_names(from_chars=POSSIBLE_CHARS,
                           n=NUMBER_OF_ITEMS_TO_GENERATE, num_of_chars=100):
    """Generates a list of str that represent random
    names generated from the given character set. The list
    will be of n length.

    the randomly generated names are guaranteed to be
    unique and not repeated in the list

    @keyword from_chars: str representing the characters
    to be chosen from. Default POSSIBLE_CHARS

    @keyword n: int representing the number of names to
    generate and populate the list with.

    @keyword num_of_chars: int representing the number of
    characters each name should be in length. Default 100

    @return: list of n length, where each index represents
    a str that was randomly generated from the given from_chars
    and is num_of_chars long.
    """
    data = set()

    while len(data) < n:
        name = ''.join(random.sample(from_chars, num_of_chars))
        data.add(name)

    return list(data)


def _generate_random_times(from_time=MIN_DATETIME, until_time=MAX_DATETIME,
                           num=NUMBER_OF_ITEMS_TO_GENERATE):
    """Generates random times within the given time frame.

    @param from_time: datetime object that represents
    the starting time, inclusive.

    @param until_time: datetime object that represents
    the ending time, inclusive.

    @keyword num: number of datetimes to generate within
    the given constraints.

    @return: list of datetime objects that all fall
    within the date range given, that were randomly
    generated. To the second. milliseconds are automatically
    set at 0 for all.
    """
    max_time_delta = until_time - from_time
    max_time_seconds = int(max_time_delta.total_seconds())
    data = []

    for n in xrange(num):
        time_data = {'seconds': random.randint(1, max(1, max_time_seconds)),
                     'microseconds': 0}

        time_delta = timedelta(**time_data)
        data.append(until_time - time_delta)
    return data


def _generate_orders_data(directory):
    """Generates orders data in the
    given directory. This function is
    designed to return identical data to
    the unpacked functions.

    @warning: Testing method. This method relies
    heavily on the standardize and parse
    file name methods. Results from this function
    may be inaccurate if parse/standardize tests
    fail.

    @param directory: str representing the
    directory that the random data is to be added to.

    @return: tuple of dict values. Representing the
    order data and togo data respectively. Each dict
    maps keys of (str, datetime) representing the
    (order_name, order_time) to list of MenuItem objects
    that represents the order. This output is identical
    to that generated by the unpack functions in the
    ConfirmationSystem module.
    """
    result = []

    for curr_data in _populate_directory_with_random_orders(directory):
        data = {}
        generated_data = curr_data.items()
        for name, (std_name, file_path, order_data) in generated_data:

            p_time, p_name, p_type = \
                ConfirmationSystem.parse_standardized_file_name(std_name)

            data[name, p_time] = order_data
        result.append(data)

    return tuple(result)


def _generate_non_parseable_random_files(directory):
    """Generates random non-parseable files
    in the given directory.

    This function is used to add "filler" to
    a directory.

    @param directory: str representing the
    directory to be filled with random file data.

    @return: None
    """
    from_chars = (string.ascii_letters + string.digits) * 10

    for name in _generate_random_names(from_chars=from_chars):
        _add_data_to_file(name, directory + '/' + name)


def _generate_reservations_data(n=NUMBER_OF_ITEMS_TO_GENERATE):
    """Generates a dict of random Reservers
    that represent the reservation data.

    @param n: int representing the number
    of Reserver objects to generate.

    @return: tuple representing first
    a list of reservations data, second
    a dict that categories all reservations
    by date.
    """
    # Generate intial data.
    reserver_data = []
    reserver_data_by_date = {}

    random_names = _generate_random_names(n=n)
    random_nums = _generate_random_names(n=n)
    random_times = _generate_random_times(datetime.now() + timedelta(minutes=30),
                                          MAX_DATETIME, num=n)


    for name, num, rsvr_time  in zip(random_names, random_nums, random_times):
        # Generate reservation
        reserver = Reserver(name, num, rsvr_time)
        reserver_data.append(reserver)

        # Store data in appropriate area.
        rsvr_date = datetime.combine(rsvr_time.date(), time.min)
        if rsvr_date in reserver_data_by_date:
            bisect.insort(reserver_data_by_date[rsvr_date], reserver)
        else:
            reserver_data_by_date[rsvr_date] = [reserver]

    return reserver_data, reserver_data_by_date


def _get_current_num_database_rows(db, table_name):
    """Gets the current database tables number
    of rows.

    @param db: sqlite3.connection that represents
    the database that is having the data retrieved.

    @param table_name: str representing the table
    name associated with the database.

    @return: int representing the number of rows
    that the table contains in the given database.
    """
    c = db.cursor()
    data = c.execute('SELECT '
                     '     COUNT (*) '
                     'FROM'
                     '     {}'.format(table_name))
    return data.next()[0]


def _populate_directory_with_random_orders(directory, num_of_chars=100,
    n=NUMBER_OF_ITEMS_TO_GENERATE, save_data=True):
    """Populates the given directory with n random orders.

    @param directory: str pointing to the directory that
    is to have the data added to it.

    @keyword num_of_chars: int representing The number
    of characters that each file should be created with.
    Draws characters from String.printable. Must be greater
    than 0.

    @keyword n: int representing the number
    of files to generate.

    @keyword save_data: bool value representing if the data
    should be saved to the directory. Default True, if false
    all items are generated with their file paths as having
    the directory as a prefix, but are not saved there.

    @return: 2 tuple representing two dicts. The first dict
    is considered the togo_dict and contains file names with
    the togo separator. The second dict is the orders dict
    and doesn't contain file names with the togo separator.

    Each dict maps a file_name to a tuple of
    (str, str, str) representing the
    (standardized name, file_path, file_data)
    respectively.
    """
    # Generate initial data
    togo_data = {}
    order_data = {}

    is_checkout = directory is path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY

    random_times = _generate_random_times(num=n)
    random_names = _generate_random_names(num_of_chars=num_of_chars)

    for order_name, file_time in zip(random_names, random_times):
        # Generate name and file path
        std_name = ConfirmationSystem.standardize_file_name(order_name,
                        is_checkout=is_checkout, set_time=file_time)

        file_path = directory + '/' + str(std_name)
        curr_order = []

        for name in _generate_random_names(n=random.randint(1, 30), num_of_chars=30):
            price = random.randint(1, 100)
            item = MenuItem(name, price)

            if random.randint(1, 10) > 7:
                item.comp(True, ''.join(random.sample(POSSIBLE_CHARS, 30)))

            curr_order.append(item)

        # Generate type
        file_data = order_data
        if TOGO_SEPARATOR in order_name:
            file_data = togo_data

        # Create and save data if applicable.
        file_data[order_name] = (std_name, file_path, curr_order)

        if save_data:
            with open(file_path, 'w') as f:
                f.write(jsonpickle.encode(curr_order))

    return order_data, togo_data


#====================================================================================
#====================================================================================
class ConfirmationSystemTest(unittest.TestCase):
    """Class for testing the ConfirmationSystem modules
    functions.
    """
    @classmethod
    def setUpClass(cls):
        """Sets up the initial data for testing. Only
        called once at the beginning of testing.

        @return: None
        """
        print TABS + 'BEGIN: Testing ConfirmationSystem module'


    @classmethod
    def tearDownClass(cls):
        """Finishes the initial data for testing. Only
        called once at the ending of testing.

        @param cls:
        @return:
        """
        if not os.path.exists(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY):
            os.mkdir(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY)
        if not os.path.exists(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY):
            os.mkdir(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY)
        if not os.path.exists(path.SYSTEM_DATABASE_PATH):
            os.mkdir(path.SYSTEM_DATABASE_PATH)

        ConfirmationSystem.ORDERS_DATABASE = \
            ConfirmationSystem._check_and_create_orders_database()

        ConfirmationSystem.RESERVATIONS_DATABASE = \
            ConfirmationSystem._check_and_create_reservations_database()

        print TABS + 'FINISHED: Testing ConfirmationSystem module'

    def setUp(self):
        """Override Method

        Used to set up the ConfirmationSystem test
        cases.

        @return: None
        """
        if not os.path.exists(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY):
            os.mkdir(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY)
        if not os.path.exists(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY):
            os.mkdir(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY)

        ConfirmationSystem.ORDERS_DATABASE = \
            ConfirmationSystem._check_and_create_orders_database(':memory:')
        ConfirmationSystem.RESERVATIONS_DATABASE = \
            ConfirmationSystem._check_and_create_reservations_database(':memory:')

    def tearDown(self):
        """Override Method

        Used to tear down the ConfirmationSystem test cases.

        @return: None
        """
        if os.path.exists(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY):
            shutil.rmtree(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY)
        if os.path.exists(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY):
            shutil.rmtree(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY)

        ConfirmationSystem.current_order_counter = 0
        ConfirmationSystem.ORDERS_DATABASE.close()
        ConfirmationSystem.RESERVATIONS_DATABASE.close()

    def test_standardize_and_parse_standardized_file_name_functions(self):
        """Test the standardize and parse standardized file
        name functions.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing standardize and parse name functions'
        #============================================================================
        # Testing the standardize and parse file name functions. Both functions
        # represent the inverse of each other. Standardizing a filename yields a
        # standardized file name. Parsing a standardized file name yields the time,
        # original name, and file type respectively.
        #
        # This test case will test the various potential problems that could exist
        # with standardizing/parsing file names.
        #
        # Case 1:
        #   Standard Case. Test general standardize/parse with random str data.
        #   Randomized str data will have the potential to have "black list"
        #   characters. Given original name as str, this will be standardized,
        #   and then parsed. Expect original name to match returned parsed name,
        #   and parsed/standardized pairs to match each other.
        #
        # Case 2:
        #   Test standardize/parse with specific time. Expect all values to be
        #   standardized with the given time, and parsed with the given time.
        #
        # Case 3:
        #   Test standardize/parse with specific bool value given as checkout.
        #   Expect all standardized/parse to have file type of checkout.
        #
        # Case 4:
        #   Test with empty order_name. Should raise ValueError
        #
        # Case 5:
        #   Test with order_name containing invalid characters.
        #
        # Case 6:
        #    Attempt to parse a non-pattern type of string. Should raise
        #    ValueError
        #
        # Case 7:
        #
        #   Invalid dates data passed in to standardize. Expect standardize to
        #   generate date at time of call.
        #============================================================================
        # Generate initial data to test
        #============================================================================
        curr_dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY

        def standardize_names(name_data, is_checkout=False, set_time=None):
            data = {}

            for name in name_data:
                std_name = ConfirmationSystem.standardize_file_name(name,
                               is_checkout=is_checkout, set_time=set_time)
                data[name] = std_name
            return data

        def parse_names(std_name_data, togo_separator=TOGO_SEPARATOR):
            data = {}
            alt_data = {}

            for std_name in std_name_data:
                p_time, p_name, p_type = \
                    ConfirmationSystem.parse_standardized_file_name(std_name,
                        togo_separator=togo_separator)
                data[p_name] = std_name
                alt_data[std_name] = (p_time, p_name, p_type)
            return data, alt_data

        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        name_data = _generate_random_names()
        name_data.sort()

        standardized_data = standardize_names(name_data)
        parsed_data, _ = parse_names(standardized_data.values())

        #============================================================================
        # Case 1: Testing that the a given name can be standardized, then parsed
        # and reverts to its original name.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertEqual(name_data, sorted(parsed_data.keys()))
        self.assertEqual(parsed_data, standardized_data)

        print 'done'

        #============================================================================
        # Generate data for testing Case 2
        #============================================================================
        standardized_data_by_value = {}
        parsed_data_by_value = {}
        data_by_time = {}

        for curr_time in _generate_random_times(num=10):
            names = _generate_random_names()
            standardized_data = standardize_names(names, set_time=curr_time)
            standardized_data_by_value[curr_time] = standardized_data

            parsed_data, alt_parsed_data = parse_names(standardized_data.values())
            parsed_data_by_value[curr_time] = parsed_data

            data_by_time[curr_time] = alt_parsed_data

        #============================================================================
        # Case 2: Testing first that the standardized data matches the parsed data.
        # Next testing that the auto generated time was accurately displayed in
        # both the standardized and parsed data.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertEqual(standardized_data_by_value, parsed_data_by_value)

        for curr_time, alt_parsed_data in data_by_time.items():
            for p_time, p_name, p_type in alt_parsed_data.values():
                self.assertEqual(p_time, curr_time)

        print 'done'

        #============================================================================
        # Generating data for test Case 3
        #============================================================================
        standardized_data_by_value = {True: [], False: []}
        parsed_data_by_value = {True: [], False: []}
        data_by_value = {True: [], False: []}

        for is_checkout in [random.choice([True, False]) for _ in xrange(10)]:
            names = _generate_random_names()

            standardized_data = standardize_names(names, is_checkout=is_checkout)
            standardized_data_by_value[is_checkout].append(standardized_data)

            parsed_data, alt_parsed_data = parse_names(standardized_data.values())
            parsed_data_by_value[is_checkout].append(parsed_data)

            data_by_value[is_checkout] = alt_parsed_data

        #============================================================================
        # Case 3: Testing first the standardized data matches the parsed data. Next
        # testing that the parsed bool values match the generated bool values.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        self.assertEqual(standardized_data_by_value, parsed_data_by_value)

        for is_checkout, alt_parsed_data in data_by_value.items():
            for p_time, p_name, p_type in alt_parsed_data.values():
                self.assertEqual(is_checkout, p_type == TYPE_SUFFIX_CHECKOUT)

        print 'done'

        #============================================================================
        # Testing Case 4: Testing for empty order name. Should raise ValueError
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        self.assertRaises(StandardError, ConfirmationSystem.standardize_file_name, '')
        self.assertRaises(StandardError,
                          ConfirmationSystem.parse_standardized_file_name, '')

        print 'done'

        #============================================================================
        # Generate Case 5 data: Generating the data the execute test case 5.
        #============================================================================
        invalid_chars = ''.join(BLACKLIST.keys())
        names = _generate_random_names(from_chars=(POSSIBLE_CHARS + invalid_chars * 5))
        names.sort()

        standardized_data = standardize_names(names)
        parsed_data, _ = parse_names(standardized_data.values())

        #============================================================================
        # Testing Case 5: Testing for situation involving name where known invalid
        # blacklisted characters are given. First test is checking for original
        # names being equal to the names retrieved after standardization. Second
        # test is checking tha the standardized data input/output was the same as
        # the parsed data output/input.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        self.assertEqual(names, sorted(parsed_data.keys()))
        self.assertEqual(standardized_data, parsed_data)

        print 'done'

        #============================================================================
        # Generate data for testing Case 6
        #============================================================================
        values = _generate_random_names()
        values.append('antidisestablishmentaranism')
        values.append(lambda x: x)
        values.append(10)
        values.append(10.0)
        values.append(self)

        #============================================================================
        # Testing Case 6: non pattern string given to parse function. Expect error
        # to be raised.
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        for name in values:
            self.assertRaises(StandardError,
              ConfirmationSystem.parse_standardized_file_name, name)

        print 'done'

        #============================================================================
        # Generating data to test Case 7
        #============================================================================
        standardized_data_by_value = {}
        for date in values:
            standardized_data = standardize_names(names, set_time=date)
            standardized_data_by_value[date] = standardized_data

        parsed_data_by_value = {}
        alt_parsed_data_by_value = {}

        for date in standardized_data_by_value:

            data = standardized_data_by_value[date]
            parsed_data, alt_parsed_data = parse_names(data.values())
            parsed_data_by_value[date] = parsed_data

            alt_parsed_data_by_value[date] = alt_parsed_data

        #============================================================================
        # Testing Case 7: Given invalid date. Expect all dates to be set to the
        # current date, within an error range of 5 seconds.
        print TABS * 3 + 'Testing Case 7...',
        #============================================================================
        self.assertEqual(standardized_data_by_value, parsed_data_by_value)

        for alt_parsed_data in alt_parsed_data_by_value.values():
            for p_time, p_name, p_type in alt_parsed_data.values():
                self.assertTrue(p_time - datetime.now() < timedelta(seconds=5))

        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing standardize and parse name functions'
        #============================================================================

    def test_orders_database_creation_functions(self):
        """Tests the functions that are used to generate the
        orders database and its subsequent tables.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing database creation function'
        #============================================================================
        # Test the creation and generation of the databases
        # that are created in the confirmation system via
        # the functions. Three tables are generated from these
        # databases.
        #
        # Testing will consist of generating the database into a
        # temporary directory. Checking to make sure it matches
        # the required format.
        #
        #
        #   Case 1:
        #       Test that the schema for the given tables matches the
        #       schema stored in the generated database tables.
        #============================================================================
        # Generate database to perform checks on, and load schema data.
        #============================================================================
        database = ConfirmationSystem._check_and_create_orders_database(':memory:')
        cursor = database.cursor()

        schema_data = (('ItemData', ITEM_DATA_COLS),
                       ('OrderData', ORDER_DATA_COLS),
                       ('DateData', DATE_DATA_COLS))

        #============================================================================
        # Case 1: Testing that schema matches with loaded schema data for tables.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        for table_name, schema in schema_data:
            values = cursor.execute('PRAGMA table_info({});'.format(table_name))

            for entries in values:
                self.assertTrue(entries[1] in schema)
                self.assertEqual(entries[2], schema[entries[1]])

        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing database creation function'
        #============================================================================

    def test_reservations_database_creation_function(self):
        """Tests the generation of the reservations database
        and its subsequent table.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing Reservations database creation function'
        #============================================================================
        # Test the generation of the reservations database
        # that are created via the ConfirmationSystem function.
        #
        #   Case 1:
        #       Schema has loaded appropriately into the database
        #       table. As such it should match the constants that
        #       represent the schema.
        #============================================================================
        # Generate initial database to perform checks.
        #============================================================================
        database = ConfirmationSystem._check_and_create_reservations_database(
            ':memory:')
        cursor = database.cursor()

        values = cursor.execute('PRAGMA table_info(ReservationsData);')
        schema_data = RESERVATIONS_DATA_COLS
        #============================================================================
        # Case 1: Test that schema appropriately is in place in database table.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        for entries in values:
            self.assertTrue(entries[1] in schema_data)
            self.assertEqual(entries[2], schema_data[entries[1]])

        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing Reservations database creation function'
        #============================================================================

    def test_load_data_function(self):
        """Tests the function that loads data from
        a given file.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing load data function'
        #============================================================================
        # Testing the function will have the following
        # cases:
        #
        # Case 1:
        #
        #   Generate several files known to exist. Pull data from files and
        #   sources and compare. Expect equality.
        #
        #   Case 2:
        #
        #   several files that are known not to exist. This includes cases where
        #   the file path given is invalid. Expect to receive error.
        #============================================================================
        # Generate initial data for comparison.
        #============================================================================
        curr_dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY
        order_data, togo_data = _populate_directory_with_random_orders(curr_dir)
        file_data = togo_data.values() + order_data.values()

        #============================================================================
        # Case 1: Checking that data loads properly
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        for file_name, file_path, order_data in file_data:
            data = ConfirmationSystem._load_data(file_path)
            self.assertEqual(data, order_data)

        print 'done'

        #============================================================================
        # Generate data for Case 2
        #============================================================================
        file_paths = []
        for file_name, file_path, order_data in file_data:
            file_paths.append(file_path)
            os.remove(file_path)

        file_paths += _generate_random_names()

        #============================================================================
        # Case 2: Checking that data doesn't load and raises error instead.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        for file_path in file_paths:
            self.assertRaises(StandardError, ConfirmationSystem._load_data, file_path)

        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing load data function'
        #============================================================================

    def test_find_order_name_paths_function(self):
        """Tests the function that is used to search for
        file paths of the given name.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing find order name paths function'
        #============================================================================
        # WARNING THIS TEST METHOD RELIES HEAVILY ON STANDARDIZE/PARSE NAMES
        # AS SUCH ITS RESULTS ARE DEPENDENT ON STANDARDIZE/PARSE TESTS FAILURES HERE
        # COULD BE UNRELIABLE IF THE STANDARDIZE/PARSE TESTS HAVE NOT PASSED.
        #
        # Testing cases here should check that the correct file has been
        # identified. Data stored in the file is entirely irrelevant. All that we
        # are searching for here is teh correct path pointing tot he file.
        #
        # Case 1: Unique names
        #
        #   This case should test whether the function is able to retrieve known
        #   existing files with a specific unique generated name.
        #
        # Case 2: Similar names
        #
        #   This case should test whether the function is able to retrieve files
        #   associated with unique, but similar names.
        #
        # Case 3: Identical names
        #
        #   This testing case will most certainly fail. The
        #   system cannot decide between near identical names.
        #   As such near identical names (those that only differ
        #   in regards to their time/date stamp) are discouraged
        #   and steps should be taken to prevent users from providing
        #   identical names and utilizing this function.
        #
        #   However Case 3 may still be tested. The function itself
        #   returns a list of paths. It will be considered a success
        #   if the ideal path is contained within the paths that were
        #   returned.
        #
        # Case 4: order name error
        #
        #   Given invalid order name (non-str or non-parseable) expect error raised.
        #
        # Case 5: directory error
        #
        #   Given invalid directory (non-str or doesn't exist) expect error raised.
        #============================================================================
        # Generate initial data for testing: Generating necessary functions and
        # random data. Two sets of random data are generated. First is a larger
        # set of 70 items that represents the potential for failures. The second
        # is a smaller set of 30 items that will be manipulated throughout this
        # testing. This set is intentionally smaller because of the length of time
        # executing this testing. The time growth of these test methods and the
        # function being tested are both high. As such it is best to operate with
        # a smaller data set where necessary.
        #===========================================================================
        curr_dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY

        def get_generated_data(curr_data):
            data = {}

            for order_name, (std_name, file_path, file_type) in curr_data:
                data_files = [file_path]

                if order_name in data:
                    data[order_name] += data_files
                else:
                    data[order_name] = data_files

            return data

        def get_order_data(curr_data, dir, set_time=None):
            data = {}

            for order_name in curr_data:
                data_files = ConfirmationSystem._find_order_name_paths(order_name,
                                                                       dir)
                if order_name in data:
                    data[order_name] += data_files
                else:
                    data[order_name] = data_files

            return data

        def clear_directory(dir):
            shutil.rmtree(dir)
            os.mkdir(dir)

        _populate_directory_with_random_orders(curr_dir, n=70)
        order_data, togo_data = _populate_directory_with_random_orders(curr_dir, n=30)

        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        generated_data = get_generated_data(order_data.items() + togo_data.items())
        unpacked_data = get_order_data(order_data.keys() + togo_data.keys(),
                                       curr_dir)

        #============================================================================
        # Case 1: All values returned should be exactly the correct path.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertEqual(generated_data, unpacked_data)

        for data in unpacked_data.values():
            self.assertEqual(len(data), 1)

        print 'done'

        #============================================================================
        # Generate data for testing Case 2: Data generated will be identical to
        # the previous data which is still stored in the directory, save a single
        # index. The index will be changed to be nearly identical to the previous
        # order name. For completeness there are multiple indexes chosen,
        # and multiple index shifts (addition vs replacement) that occurs to allow
        # for a sufficiently large data set to be gathered and analyzed.
        #============================================================================
        generated_data = {}
        for order_name in order_data.keys() + togo_data.keys():

            # ensure that the index replacement works at both limits and any random
            # index in the range.
            index_data = [0,
                          random.randint(1, len(order_name)),
                          len(order_name)]

            for index in index_data:
                char = random.choice(string.printable)
                name = order_name[:index] + char + order_name[index:]

                std_name = ConfirmationSystem.standardize_file_name(name)
                file_path = curr_dir + '/' + std_name

                _add_data_to_file('test', file_path)

                # All generated order data is unique. However there could
                # exist a potential conflict that this would randomly select
                # an identical index and shift a name to another name. As such
                # an update would be the correct way to add it.
                if name in generated_data:
                    bisect.insort(generated_data[name], file_path)
                else:
                    generated_data[name] = [file_path]

        unpacked_data = get_order_data(generated_data.keys(), curr_dir)

        #============================================================================
        # Case 2: Expect all generated dicts to match the unpacked dicts. This
        # means that the order names have been found without pulling the
        # previously stored data.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(unpacked_data, generated_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 3: Test case 3 is testing the identical
        # order name but differing time stamps. As such data is generated that
        # matches this description. This means pulling the previous data and
        # resaving it with a new time stamp.
        #============================================================================
        generated_data = {}

        for order_name in order_data.keys() + togo_data.keys():
            new_time = datetime.now() + timedelta(days=1)

            std_name = ConfirmationSystem.standardize_file_name(order_name,
                                                                set_time=new_time)

            file_path = curr_dir + '/' + std_name
            _add_data_to_file('test', curr_dir + '/' + std_name)

            # order data and keys data are known to be unique.
            generated_data[order_name] = [file_path]


        unpacked_data = get_order_data(generated_data.keys(), curr_dir)

        #============================================================================
        # Case 3: Expect the list to contain the correct file path, but not
        # necessarily that specific unique file path.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        self.assertTrue(unpacked_data > 0)
        self.assertEqual(len(unpacked_data), len(generated_data))

        for key in unpacked_data:
            self.assertTrue(set(generated_data[key]).issubset(set(unpacked_data[key])))

        print 'done'

        #============================================================================
        # Generating data for test Case 4: Generating values that can be
        # substituted in for parameters.
        #============================================================================
        values = (10.0,
                  10,
                  lambda x: x,
                  self,
                  None)

        f = ConfirmationSystem._find_order_name_paths

        #============================================================================
        # Case 4: Testing that given an invalid order name standard error is raised.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        for order_name in values:
            self.assertRaises(StandardError, f, order_name, curr_dir)
        print 'done'

        #============================================================================
        # Generating data for test Case 5: additional str added that would have
        # passed previous tests.
        #============================================================================
        values = values + ('antidisestablishmetaranism', '~/some/made/up/dir/s')

        #============================================================================
        # Case 5: Testing that given an invalid directory standard error is raised.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for directory in values:
            self.assertRaises(StandardError, f, 'test', directory)
        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing find order name paths function'
        #============================================================================

    def test_unpack_order_data_function(self):
        """Tests the unpack order data function
        if it is operating appropriately.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing unpack order data function'
        #============================================================================
        # Testing the unpack order data function requires both testing for
        # standard table orders and togo orders. Thus we have two cases Since this
        # function relies on the load data function we can guarantee its success
        # at retrieving the data, with the only requirement being that we are
        # pulling the correct data, with the correct names, and correct
        # labels.
        #
        # Multiple tests also perform a check that the given data sets contain
        # actual data and their length is greater than 0. This is to ensure that
        # empty sets are not being tested.
        #
        # Case 1:
        #
        #   Standard table order data that is pulled. Needs to
        #   be checked for accurate name, and date/times. Also that
        #   all available data has been pulled.
        #
        # Case 2:
        #
        #   Repopulated area. Check that all data is returned appropriately.
        #   This is equivalent to performing case 1 again, but ensuring that
        #   the data that was added as well as the data that was previously added
        #   is unpacked.
        #
        # Case 3:
        #
        #   Change directory. Pulled data should be empty
        #
        # Case 4:
        #
        #   Populate empty directory with random files that are non-parse-able.
        #   Expect empty data unpacked.
        #
        #
        # Case 5:
        #
        #   Perform Case 1 with new directory and random files. Data should unpack
        #   properly.
        #
        # Case 6:
        #
        #   Perform Case 2 with new directory and random files. Data should unpack
        #   properly.
        #
        # Case 7:
        #
        #   Error raised when invalid directory is given (non-str or doesn't exist)
        #===========================================================================
        # This block generates data to be assessed.
        #===========================================================================
        curr_dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY

        #============================================================================
        # Generate data for Case 1
        #============================================================================
        generated_data = _generate_orders_data(curr_dir)
        unpacked_data = ConfirmationSystem.unpack_order_data(curr_dir)

        #============================================================================
        # Testing Case 1: Checking that the generated data and unpacked data are
        # equal.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertTrue(len(unpacked_data[0]) > 0)
        self.assertTrue(len(unpacked_data[1]) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for Case 2
        #============================================================================
        prev_generated_data = generated_data

        generated_data = _generate_orders_data(curr_dir)
        generated_data[0].update(prev_generated_data[0])
        generated_data[1].update(prev_generated_data[1])

        unpacked_data = ConfirmationSystem.unpack_order_data(curr_dir)

        #============================================================================
        # Testing Case 2: Checking that all appropriately returned data has been
        # returned in the appropriate form of key = (str, float) representing the
        # associated order name and time respectively.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertTrue(len(unpacked_data[0]) > 0)
        self.assertTrue(len(unpacked_data[1]) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for Case 3
        #============================================================================
        curr_dir = path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY

        generated_data = {}, {}
        unpacked_data = ConfirmationSystem.unpack_order_data(curr_dir)

        #============================================================================
        # Case 3: Testing that changing the directory passed into the function as
        # an argument actually changes the directory unpacked from.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for Case 4
        #============================================================================
        _generate_non_parseable_random_files(curr_dir)

        generated_data = {}, {}
        unpacked_data = ConfirmationSystem.unpack_order_data(curr_dir)

        #============================================================================
        # Case 4: Testing that the newly selected directory operates appropriately.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for Case 5
        #============================================================================
        generated_data = _generate_orders_data(curr_dir)
        unpacked_data = ConfirmationSystem.unpack_order_data(curr_dir)

        #============================================================================
        # Case 5: Testing similar to Case 1 with added constraints of new
        # directory and randomly generated non-parse-able files. Expect for only
        # generated data to be unpacked.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        self.assertTrue(len(unpacked_data[0]) > 0)
        self.assertTrue(len(unpacked_data[1]) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for Case 6
        #============================================================================
        prev_generated_data = generated_data

        generated_data = _generate_orders_data(curr_dir)
        generated_data[0].update(prev_generated_data[0])
        generated_data[1].update(prev_generated_data[1])

        unpacked_data = ConfirmationSystem.unpack_order_data(curr_dir)

        #============================================================================
        # Case 6: Testing similar to Case 2 with added constraints of new
        # directory and randomly generated non-parse-able files. Expect for
        # previously generated data and new generated data to be unpacked.
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        self.assertTrue(len(unpacked_data[0]) > 0)
        self.assertTrue(len(unpacked_data[1]) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing unpack order data function'
        #============================================================================

    def test_add_reservation_to_database(self):
        """Tests the add_reservation_to_database function
        for proper behavior.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing add reservation to database function'
        #============================================================================
        # WARNING: THIS METHOD RELIES HEAVILY ON THE CREATE RESERVATIONS DATABASE
        # FUNCTIONING PROPERLY.
        #
        # Tests the add reservation to database function. This will be composed
        # of several cases:
        #
        # Case 1:
        #
        #   Generate random reservations. Test if the add function correctly adds
        #   all the data by unpacking the data and comparing to the known data added.
        #
        # Case 2:
        #
        #   Generate random reservations. Test if the add function correctly adds
        #   all the data by unpacking the data and comparing to the accumulated
        #   generated data.
        #
        # Case 3:
        #
        #   Non-Reserver object passed in as reservation. Expect error.
        #
        # Case 4:
        #
        #   Non-sqlite3 object passed in as database. Expect error
        #============================================================================
        # Generate initial data setup
        #============================================================================
        db = ConfirmationSystem._check_and_create_reservations_database(':memory:')

        def generate_reserver_data(database):
            data = {}

            reserver_data, _ = _generate_reservations_data()
            for reserver in reserver_data:
                key = (reserver.name,
                       reserver._arrival_time,
                       reserver.number)

                ConfirmationSystem.add_reservation_to_database(reserver,
                                                               database=database)
                if key in data:
                    data[key] += [reserver]
                else:
                    data[key] = [reserver]

            return data

        def unpack_reserver_data(reserver_data, database):
            data = {}

            c = database.cursor()
            for key, reserver in reserver_data:
                cols_data = (key[0],
                             key[1].strftime(SQLITE_DATE_TIME_FORMAT_STR),
                             key[2])

                rsvr_data = c.execute('SELECT '
                                      '     ReservationData_json '
                                      'FROM '
                                      '     ReservationsData '
                                      'WHERE ('
                                      '     ReservationName=?'
                                      ' AND '
                                      '     ReservationTime=datetime(?)'
                                      ' AND '
                                      '     ReservationNumber=?'
                                      '      );', cols_data)

                for rsvr_json in rsvr_data.fetchall():
                    rsvr = jsonpickle.decode(rsvr_json[0])
                    key = rsvr.name, rsvr._arrival_time, rsvr.number

                    if key in data:
                        data[key] += [rsvr]
                    else:
                        data[key] = [rsvr]
            return data

        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        generated_data = generate_reserver_data(db)
        unpacked_data = unpack_reserver_data(generated_data.items(), db)

        #============================================================================
        # Case 1: Testing for accurate reservations data unpacked.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 2
        #============================================================================
        prev_generated_data = generated_data

        generated_data = generate_reserver_data(db)
        generated_data.update(prev_generated_data)

        unpacked_data = unpack_reserver_data(generated_data.items(), db)

        #============================================================================
        # Case 2: Testing for accurate reservations data unpacked after updated
        # reservations database. Expect unpacked data to include previously
        # generated data and new generated data.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 3
        #============================================================================
        values = ('antidisestablishmentaranism',
                  10.0,
                  10,
                  None,
                  self,
                  lambda x: x)
        f = ConfirmationSystem.add_reservation_to_database
        r = Reserver('a', 'b', datetime.now() + timedelta(days=1))

        db_data = (db, 'ReservationsData')

        db_counter = _get_current_num_database_rows(*db_data)

        #============================================================================
        # Case 3: Testing for error raised when given non-Reserver reservation,
        # and database left unaffected.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for reserver in values:
            self.assertRaises(StandardError, f, reserver, db)

        self.assertEqual(db_counter, _get_current_num_database_rows(*db_data))
        print 'done'

        #============================================================================
        # Case 4: Testing for error raised when given a non-sqlite3.connection for
        # database.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        for database in values:
            self.assertRaises(StandardError, f, r, database)
        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing add reservation to database function'
        #============================================================================

    def test_unpack_reservations_data(self):
        """Tests the unpack reservations data function
        for proper behavior.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing unpack reservations data function.'
        #============================================================================
        # WARNING: THIS METHOD RELIES HEAVILY ON THE ADD_RESERVATION TO DATABASE
        # FUNCTION OPERATING PROPERLY. ANY ERRORS IN THIS METHOD COULD BE
        # UNRELIABLE IF THE ADD RESERVATION TO DATABASE FUNCTION FAILED ITS TEST.
        #
        # Here we are testing that the database is accurately returning all of the
        # information of the specified date. As such first we will need to
        # populate the database with reservation data. The next step will be
        # pulling said data from the database through the unpack_reservations_data
        # function and seeing if it matches the generated data.
        #
        #
        # Case 1:
        #
        #   Check if generated reservation data, which has been stored matches the
        #   unpacked stored data.
        #
        # Case 2:
        #
        #   Select a date range known to exist, and ensure that all reservations
        #   grabbed are greater than the datetime selected.
        #
        # Case 3:
        #
        #   Check within a date range known not to exist. Should return empty
        #   data set.
        #
        # Case 4:
        #
        #   Check that the returned unpacked reservation data is already sorted.
        #
        # Case 5:
        #
        #   Given invalid datetime object expect current datetime to be chosen and
        #   data to be pulled in regards to that point
        #
        # Case 6:
        #
        #   non-sqlite3.connection given as database. Expect error raised,
        #   expect data unaltered.
        #============================================================================
        # Generating initial data.
        #============================================================================
        db = ConfirmationSystem._check_and_create_reservations_database(':memory:')

        def generate_reservation_data(db):
            rsvr_list, reserver_data = _generate_reservations_data()

            for rsvr in rsvr_list:
                ConfirmationSystem.add_reservation_to_database(rsvr, db)

            return rsvr_list, reserver_data

        def get_random_reservation_data(reserver_data):
            data = {}

            for date, rsvr in reserver_data.items():
                rsvr.sort()
                median_data = rsvr[:len(reserver_data)/2]

                start_datetime = median_data[0]._arrival_time
                data[start_datetime] = median_data

            return data

        def get_unpacked_reserver_data_by_datetimes(datetimes, db):
            data = {}

            for curr_date in datetimes:
                rsvr_data = ConfirmationSystem.unpack_reservations_data(curr_date,
                                                                        database=db)
                data[curr_date] = rsvr_data

            return data

        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        _, generated_data = generate_reservation_data(db)
        unpacked_data = get_unpacked_reserver_data_by_datetimes(
            generated_data.keys(), db)

        #============================================================================
        # Case 1: Testing for data matching to specific date
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case2
        #============================================================================
        generated_data = get_random_reservation_data(generated_data)
        unpacked_data = get_unpacked_reserver_data_by_datetimes(
            generated_data.keys(), db)

        #============================================================================
        # Case 2: Testing for pulling data from a specific arbitrary order
        # datetime. All pulled data is expected to be equal to the given date,
        # but greater than the given time.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 4.
        #============================================================================
        limit_datetimes = []

        limit_datetimes.append(max(generated_data.keys()) + timedelta(days=1))
        limit_datetimes.append(min(generated_data.keys()) - timedelta(days=1))

        #============================================================================
        # Case 3: Testing that a date beyond the given date range returns an empty
        # list.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for limit_datetime in limit_datetimes:
            unpacked_data = ConfirmationSystem.unpack_reservations_data(
                curr_date=limit_datetime, database=db)

            self.assertEqual(unpacked_data, [])

        print 'done'

        #============================================================================
        # Generating data for test Case 4
        #============================================================================
        prev_generated_data = generated_data
        unpacked_data = get_unpacked_reserver_data_by_datetimes(
            prev_generated_data.keys(), db)

        #============================================================================
        # Case 4: Testing that the returned reservations data is already in sorted
        # order.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        for data_list in unpacked_data.values():
            self.assertEqual(data_list, sorted(data_list))

        print 'done'

        #============================================================================
        # Generate data for test Case 5
        #============================================================================
        values = ('antidisestablishmentaranism',
                  10,
                  10.0,
                  None,
                  lambda x: x,
                  self)
        expected_datetime = datetime.now()

        #============================================================================
        # Case 5: Testing that given a non-datetime object the function assumes
        # that the current datetime is the correct one and returns data associated
        # with that
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for date in values:
            for data in ConfirmationSystem.unpack_reservations_data(date, db):
                for rsvr in data:
                    self.assertTrue((rsvr._arrival_time - expected_datetime) >= 0)
        print 'done'

        #============================================================================
        # Generate data for test Case 6
        #============================================================================
        rsvr_data = [Reserver('test', 'test', datetime.now() + timedelta(days=1))]
        f = ConfirmationSystem.unpack_reservations_data

        #============================================================================
        # Case 6: Testing that given a non-sqlite3.connect object as the database
        # an error is raised.
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        for database in values:
            self.assertRaises(StandardError, f, rsvr_data, database)
        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing unpack reservations data'
        #============================================================================

    def test_unpack_checkout_data(self):
        """Tests the unpack checkout data function

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing unpack checkout data function'
        #============================================================================
        # WARNING THIS TESTING METHOD RELIES HEAVILY ON THE UNPACK ORDER DATA
        # FUNCTION. ANY ERRORS IN THE UNPACK ORDER DATA FUNCTION MAY CAUSE THIS
        # METHOD TO GIVE A FALSE NEGATIVE.
        #
        # Testing the unpack order data function. This function utilizes the
        # unpack order data. The main difference is that the data returned is a
        # single dict with both order data and togo data contained. Further that
        # each key in the dict is unique regardless of duplicate names with repeated
        #
        #
        # Case 1:
        #
        #   Directory contains only parseable file names. Expect dict returned to
        #   contain the data of both the order data and togo data.
        #
        # Case 2:
        #
        #   Directory contains both parseable and non parseable file names. Expect
        #   dict returned to contain the data of both the order data and togo data.
        #
        # Case 3:
        #
        #   Directory contains only non-parseable file names. Expect empty dict.
        #
        #============================================================================
        # Generate initial data for testing
        #============================================================================
        curr_dir = path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY

        def generate_data(dir):
            data = {}

            order_data, togo_data = _populate_directory_with_random_orders(dir)
            items = order_data.items() + togo_data.items()

            for order_name, (std_name, path, f_data) in items:

                p_time, p_name, p_type = \
                    ConfirmationSystem.parse_standardized_file_name(std_name)

                data[order_name, p_time] = f_data

            return data

        def clear_directory(dir):
            shutil.rmtree(dir)
            os.mkdir(dir)

        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        generated_data = generate_data(curr_dir)
        unpacked_data = ConfirmationSystem.unpack_checkout_data()

        #============================================================================
        # Case 1: Expect unpacked data to match the items of the combined order
        # data and togo data.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 2
        #============================================================================
        clear_directory(curr_dir)
        _generate_non_parseable_random_files(curr_dir)

        generated_data = generate_data(curr_dir)
        unpacked_data = ConfirmationSystem.unpack_checkout_data()

        #============================================================================
        # Case 2: Expect unpacked data to match the items of the combined order
        # data and togo data.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 3
        #============================================================================
        clear_directory(curr_dir)
        _generate_non_parseable_random_files(curr_dir)
        unpacked_data = ConfirmationSystem.unpack_checkout_data()

        #============================================================================
        # Case 3: Expect unpacked data to be empty.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        self.assertEqual(unpacked_data, {})
        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing unpack checkout function.'
        #============================================================================

    def test_remove_order_file(self):
        """Tests the remove order file function.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing remove order file function'
        #============================================================================
        # Testing the remove order file requires populating the necessary area
        # with file names. It should be sufficient to populate and then attempt
        # removes under certain conditions
        #
        # Case 1:
        #
        #   Empty directory populated with only parseable order files. Perform
        #   operation. Ensure that both files are removed and they returned the
        #   correct information
        #
        # Case 2:
        #
        #   Directory populated with both parseable and non-parseable files.
        #   Expect data returned to be accurate and all parseable files removed.
        #
        # Case 3:
        #
        #   Invalid standardized file name given. Expect error.
        #
        # Case 4:
        #
        #   Invalid directory given. Expect error.
        #
        #============================================================================
        # Generate initial data for testing
        #============================================================================
        curr_dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY

        def generate_files_data(dir):
            data = {}

            order_data, togo_data = _populate_directory_with_random_orders(dir)

            for name, path, file_data in order_data.values() + togo_data.values():
                data[name] = file_data
            return data

        def remove_files(std_names, dir):
            data = {}

            for name in std_names:
                file_data = ConfirmationSystem._remove_order_file(name, dir)

                data[name] = file_data
            return data

        def check_files_removed(std_names, dir):
            for name in std_names:

                if os.path.exists(dir + '/' + name):
                    return False
            return True

        #============================================================================
        # Generate data for test Case 1
        #============================================================================
        generated_data = generate_files_data(curr_dir)
        unpacked_data = remove_files(generated_data, curr_dir)

        #============================================================================
        # Case 1: Testing removal of order files from specified directory and
        # accurate return data.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        self.assertTrue(check_files_removed(generated_data, curr_dir))
        print 'done'

        #============================================================================
        # Generate data for test Case 2
        #============================================================================
        _generate_non_parseable_random_files(curr_dir)
        generated_data = generate_files_data(curr_dir)
        unpacked_data = remove_files(generated_data, curr_dir)

        #============================================================================
        # Case 2: Testing removal of order files from specific directory and
        # accurate return data in situation where non-parseable files and
        # parseable files occupy the directory.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        self.assertTrue(check_files_removed(generated_data, curr_dir))
        print 'done'

        #============================================================================
        # Generate data for testing Case 3
        #============================================================================
        values = ('antidisestablishmentaranism',
                  10.0,
                  10,
                  None,
                  lambda x: x,
                  self)

        f = ConfirmationSystem._remove_order_file
        #============================================================================
        # Case 3: Given invalid standardized name expect error raised.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for std_name in values:
            self.assertRaises(StandardError, f, std_name, curr_dir)
        print 'done'

        #============================================================================
        # Generate data for testing Case 4
        #============================================================================
        std_name = generated_data.keys()[0]

        #============================================================================
        # Case 4: Given invalid directory expect error raised.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        for directory in values:
            self.assertRaises(StandardError, f, std_name, directory)
        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing remove order file function'
        #============================================================================

    def test_save_order_file_data(self):
        """Tests the save order file data

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing save order file data function'
        #============================================================================
        # WARNING THIS TEST RELIES HEAVILY ON THE LOAD DATA FUNCTION. IF ERRORS
        # EXIST IN THE LOAD DATA FUNCTION THAN THIS TEST MAY NOT BE RELIABLY
        # OPERATING.
        #
        # Tests the save order file data function. This function takes order data
        # and a file path and jsonpickles the data into the filepath. Since this
        # is a rather simple process this method will test these general cases:
        #
        # Case 1:
        #
        #   Generate and save random data. Pull data and ensure that unpacked data
        #   was accurately saved. Saved with unique name.
        #
        # Case 2:
        #
        #   Generate and save random data. Pull data and ensure that unpacked data
        #   was accurately saved. Data saved with duplicate name. Original data is
        #   expected to be replaced.
        #
        # Case 3:
        #
        #   Given Invalid file path. Which is invalid for not being
        #   standardized. Expect error to be raised.
        #============================================================================
        # Generate data
        #============================================================================
        curr_dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY

        def generate_data(dir):
            data = {}

            order, togo = _populate_directory_with_random_orders(dir,
                                                                 save_data=False)
            for std_name, file_path, file_data in order.values() + togo.values():
                data[file_path] = file_data

                ConfirmationSystem._save_order_file_data(file_data, file_path)

            return data

        def unpack_data(file_paths, dir):
            data = {}

            for file_path in file_paths:
                data[file_path] = ConfirmationSystem._load_data(file_path)

            return data

        #============================================================================
        # Generate data for test Case 1
        #============================================================================
        generated_data = generate_data(curr_dir)
        unpacked_data = unpack_data(generated_data.keys(), curr_dir)

        #============================================================================
        # Case 1: Testing data saved accurately by checking unpacked data.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for test Case 2
        #============================================================================
        _generate_non_parseable_random_files(curr_dir)
        unpacked_data = unpack_data(generated_data.keys(), curr_dir)

        #============================================================================
        # Case 2: Testing data saved accurately by checking unpacked data.
        # Directory has been populated with random files.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for test Case 3
        #============================================================================
        values = ("antidisestablishmentarnism",
                  "this/is/a/test",
                  10.0,
                  10,
                  None,
                  lambda x: x,
                  self)
        f = ConfirmationSystem._save_order_file_data

        #============================================================================
        # Case 3: Testing given invalid file_path expect error raised.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for file_path in values:
            self.assertRaises(StandardError, f, ['a'], file_path)
        print 'done'
        #============================================================================
        print TABS * 2 + 'Finished testing save order file data function'
        #============================================================================

    def test_undo_checkout_file(self):
        """Tests the undo_checkout_file function

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing undo checkout file'
        #============================================================================
        # WARNING: RELIES HEAVILY ON THE PARSE STANDARDIZE NAME FUNCTION AND LOAD
        # DATA FUNCTIONS. IF THOSE FUNCTIONS ARE NOT OPERATING PROPERLY THEN THIS
        # TEST METHOD IS CONSIDERED UNRELIABLE.
        #
        # Testing the undo checkout file removes the file from the checkout
        # directory and then adds it tot he confirmed directory as well as returns
        # the data associated with the file that was moved.
        #
        # Case 1:
        #
        #   Directory populated only with parseable file names that are to be
        #   undone. Expect unpacked data form the save directory to match the
        #   generated data.
        #
        # Case 2:
        #
        #   Directory populated with both parseable and non-parseable file names
        #   with only the parseable file names to be undone.
        #
        # Case 3:
        #
        #   Given checkout name and checkout time that do not exist. Expect error
        #   to be raised.
        #
        # Case 4:
        #
        #   Given non-str for original checkout name. Expect error to be raised.
        #
        # Case 5:
        #
        #   Given non-datetime for checkout time. Expect error to be raised.
        #
        # Case 6:
        #
        #   Given non-str for new name. Expect error to be raised.
        #
        #============================================================================
        # Generate initial data to test undo checkout file function
        #============================================================================
        curr_dir = path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY
        save_dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY

        def generate_data(dir):
            data = {}
            data_paths = []

            order, togo = _populate_directory_with_random_orders(dir)

            for name, path, file_data in order.values() + togo.values():
                p_time, p_name, p_type = \
                    ConfirmationSystem.parse_standardized_file_name(name)

                data[p_name, p_time] = file_data
                _add_data_to_file(file_data, path)

                data_paths.append(path)

            return data, data_paths

        def unpack_data(file_data):
            data = {}
            names = _generate_random_names(num_of_chars=20)

            for (p_name, p_time), name in zip(file_data, names):
                new_path, _ = ConfirmationSystem.undo_checkout_file(p_name,  p_time,
                                                                    name)
                data[p_name, p_time] = ConfirmationSystem._load_data(new_path)

            return data

        def all_files_removed(file_data):
            for file_path in file_data:
                if os.path.exists(file_path):
                    return False

            return True

        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        generated_data, data_paths = generate_data(curr_dir)
        unpacked_data = unpack_data(generated_data)

        #============================================================================
        # Case 1: Testing that order information from the checkout directory is
        # correctly undone and added to the confirmed directory with no loss of
        # data.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertTrue(all_files_removed(data_paths))
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 2
        #============================================================================
        _generate_non_parseable_random_files(curr_dir)
        generated_data, data_paths = generate_data(curr_dir)
        unpacked_data = unpack_data(generated_data)

        #============================================================================
        # Case 2: Testing that the order information from the checkout directory
        # is correctly
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertTrue(all_files_removed(data_paths))
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for test Case 3
        #============================================================================
        p_name, p_time = generated_data.keys()[0]

        values = ((p_name, datetime.now()),
                  ('bad name', p_time))

        f = ConfirmationSystem.undo_checkout_file
        #============================================================================
        # Case 3: Testing non existent checkout time with ok name, and vice versa.
        # Expect error to be raised in both cases.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for p_name, p_time in values:
            self.assertRaises(StandardError, f, p_name, p_time, 'test')
        print 'done'

        #============================================================================
        # Generate data for test Case 4
        #============================================================================
        values = (10.0,
                  10,
                  True,
                  None,
                  self,
                  lambda x: x)

        #============================================================================
        # Case 4: Testing that a non-str original checkout name raises an error.
        print TABS * 3 + 'Testing Case 4...',
        #===========================================================================
        for name in values:
            self.assertRaises(StandardError, f, name, datetime.now(), 'test')
        print 'done'

        #============================================================================
        # Case 5: Testing that a non-datetime object given as the datetime raises
        # an error.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for d_time in ('antidisestablishmentaranism',) + values:
            self.assertRaises(StandardError, f, 'test', d_time, 'test')
        print 'done'

        #============================================================================
        #Case 6: Testing that a non-str object given as the new name raises an
        # error.
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        for name in values:
            self.assertRaises(StandardError, f, 'test', datetime.now(), name)
        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing undo checkout file'
        #============================================================================

    def test_update_orders_database(self):
        """Test the update orders database function.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing update orders database function'
        #============================================================================
        # Testing the update orders database requires the checkout directory to be
        # populated with files that are to be added to the database. All database
        # operations are performed from the RAM by using the ":memory:" parameter
        # for connection. This is to allow the tests to be executed quickly. All
        # database functions take an optional keyword argument that sets the
        # database being operated on.
        #
        #   Case 1:
        #
        #       Fully populated Checkout directory. Every order is pulled and
        #       added to a specific temporary database.
        #
        #   Case 2:
        #
        #       Empty Checkout directory. Nothing is added to the temporary
        #       database.
        #
        #   Case 3:
        #
        #       Checkout area is populated with no parse-able file names. Expect
        #       empty list
        #
        #   Case 4:
        #
        #       Checkout area is populated with parse-able and non-parse-able
        #       names. Expect the appropriate list returned.
        #
        #   Case 5:
        #
        #       Ensure that all order numbers for items match with order numbers
        #       for orders.
        #
        #   Case 6:
        #
        #       Ensure that all item frequencies between orders and items match.
        #
        # All other cases of functionality in a single database will be
        # considered in their respective methods.
        #============================================================================
        # Generate initial data for database.
        #============================================================================
        dir = path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY
        db = ConfirmationSystem._check_and_create_orders_database(':memory:')

        order_data, togo_data = _populate_directory_with_random_orders(dir)

        data = order_data.values() + togo_data.values()

        def test_database_size(self, database, data):
            ConfirmationSystem.update_orders_database(database=database)
            orders_database_row = ConfirmationSystem.current_order_counter

            self.assertEqual(orders_database_row, len(data))

        #============================================================================
        # Case 1: Fully populated checkout directory. Pulling all data from
        # checkout and loading it into the temporary database. This case will
        # check that the data is pulled, that the temporary database was updated.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        test_database_size(self, db, data)

        print 'done'

        #============================================================================
        # Generating data for Case 2.
        #============================================================================
        new_db = ConfirmationSystem._check_and_create_orders_database(':memory:')

        ConfirmationSystem.current_order_counter = 0

        #============================================================================
        # Case 2: Testing empty list and empty Checkout directory. Expected 0 rows
        # added to database.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        test_database_size(self, new_db, [])
        print 'done'

        #============================================================================
        # Generating data for testing Case 3
        #============================================================================
        for x in xrange(30):
            name = ''.join(random.sample(POSSIBLE_CHARS.replace('/', '_'), 30))
            with open(dir + '/' + name, 'w') as f:
                f.write('')

        #============================================================================
        # Case 3: Testing for directory containing non-parsable file names. These
        # filenames should be ignored, leaving only the file names that fit the
        # pattern as parsed and read into the database. As such I expect the new
        # database to remain empty.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        test_database_size(self, new_db, [])

        print 'done'

        #============================================================================
        # Generate data for testing case 4
        #============================================================================
        orders_data, togo_data = _populate_directory_with_random_orders(dir)

        #============================================================================
        # Case 4: Testing for directory containing both parsable and non-parasable
        # files. The non-parasable filenames should be ignored but the parsable
        # file names should be parsed and added to the database. As such I expect
        # the new database to contain only that data drawn from the generated
        # order and togo data.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        test_database_size(self, new_db, orders_data.keys() + togo_data.keys())
        print 'done'

        #============================================================================
        # Generating data for test case 5
        #============================================================================

        def get_items_data_for_order_number(num, db):
            c = db.cursor()
            data = c.execute('SELECT '
                             '      ItemData_json '
                             'FROM '
                             '      ItemData '
                             'WHERE '
                             '      OrderNumber=?', (num,))
            db.commit()

            item_data = []

            for item_json in data:
                item_data.append(jsonpickle.decode(item_json[0]))

            return item_data

        c = db.cursor()
        curr_data = c.execute('SELECT '
                              '        OrderNumber, OrderData_json '
                              'FROM'
                              '        OrderData '
                              'ORDER BY '
                              '        OrderNumber;')
        db.commit()

        order_data = {}
        for order_num, orderdata_json in curr_data:
            order_data[order_num] = jsonpickle.decode(orderdata_json)

        #============================================================================
        # Case 5: Testing that he order numbers match with the item numbers. This
        # means any given orders stored json data should contain all menu items
        # that share the same order number.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for order_number in order_data:
            item_data = get_items_data_for_order_number(order_number, db)
            self.assertTrue(len(item_data) > 0)
            self.assertEqual(order_data[order_number], item_data)

        print 'done'

        #============================================================================
        # Generate data for testing Case 6
        #============================================================================

        def get_items_data_for_frequencies(num, db):
            c = db.cursor()
            curr_data = c.execute('SELECT '
                                  '    ItemName '
                                  'FROM '
                                  '     ItemData '
                                  'WHERE '
                                  '     OrderNumber=?;', (num,))
            item_freq = Counter()
            db.commit()

            for row in curr_data:
                item_name = row[0]
                item_freq[item_name] += 1

            return item_freq

        c = db.cursor()
        curr_data = c.execute('SELECT '
                              '     OrderNumber, OrderItemFrequency_json '
                              'FROM '
                              '     OrderData;')
        db.commit()

        order_data = {}
        for order_number, order_item_freq in curr_data:
            order_data[order_number] = jsonpickle.decode(order_item_freq)

        #============================================================================
        # Case 6: Testing that the item frequencies are accurately represented in
        # the orders table. This means pulling the data from the items for every
        # order and calculating their frequency. Then checking against the stored
        # frequency data in order.
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        for order_number in order_data:
            item_freq = get_items_data_for_frequencies(order_number, db)

            self.assertTrue(len(item_freq) > 0)
            self.assertEqual(order_data[order_number], item_freq)

        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing update orders database function'
        #============================================================================

    def test_update_date_table(self):
        """Tests the update date table function.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing update date table function'
        #============================================================================
        # WARNING: THIS METHOD RELIES HEAVILY ON THE UPDATE ORDER TABLE,
        # CHECK AND CREATE ORDERS DATABASE, AND THE STANDARDIZE ORDER NAME
        # FUNCTIONS AND AS SUCH ANY ERRORS IN THE FUNCTIONS WILL RESULT
        # IN THIS TEST BEING UNRELIABLE.
        #
        # Testing the date table. This method will check for the correct data
        # being displayed in the date table. Because of this checking the database
        # is necessary. However a hard disk based database will be slow. So
        # instead a RAM based database will be utilized for simplicity. This
        # further requires a fully updated orders database that the data can be
        # populated from. As such this method will rely heavily
        #
        #   Case 1:
        #
        #       Requires an adequately populated Orders database for this method to
        #       function. As such Case 1 is that the orders are populated,
        #       and then the date is updated with the correct data.
        #
        #   Case 2:
        #
        #       Empty Checkout data. Unaffected Dates database.
        #
        #   Case 3:
        #
        #       Repopulated Checkout data. Should contain only a single row
        #       representing the date, which has now been updated.
        #
        #   Case 4:
        #
        #       AttributeError when non-datetime object is passed in as date.
        #
        #   Case 5:
        #
        #       AttributeError when non-Sqlite3.connection object is passed in as
        #       database
        #============================================================================
        # Generate initial data to perform tests.
        #============================================================================
        dir = path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY
        db = ConfirmationSystem._check_and_create_orders_database(':memory:')

        order_data, togo_data = _populate_directory_with_random_orders(dir,
                                    save_data=False)

        date_data_info =[]

        def get_order_info(db, curr_date):
            c = db.cursor()
            data = c.execute('SELECT '
                             '      date(OrderDate), '
                             '      SUM(OrderType_standard), '
                             '      SUM(OrderType_togo), '
                             '      SUM(OrderSubtotal), '
                             '      SUM(OrderTax), '
                             '      SUM(OrderTotal) '
                             'FROM'
                             '      OrderData '
                             'WHERE '
                             '      date(OrderDate)=? '
                             'ORDER BY '
                             '      OrderDate;', (curr_date,))
            rows = data.fetchall()
            return rows

        def get_date_data(db):
            c = db.cursor()
            data = c.execute('SELECT '
                             '      * '
                             'FROM '
                             '      DateData '
                             'ORDER BY '
                             '      Date;')
            return data.fetchall()

        def load_order_data(data, db):
            curr_data = _add_order_data_to_database(data, database=db)
            return set([datetime.strptime(x[1], SQLITE_DATE_TIME_FORMAT_STR)
                        for x in curr_data])

        def load_date_data(dates, db):
            for date in dates:
                ConfirmationSystem._update_date_table(date, database=db)

        #============================================================================
        # Generate data for Case 1
        #============================================================================
        dates = load_order_data(order_data.values() + togo_data.values(), db)
        load_date_data(dates, db)

        #============================================================================
        # Case 1: Testing that the DateData table is populated with the correct
        # information.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        for date_data in get_date_data(db):

            order_info = get_order_info(db, date_data[0])

            for order in order_info:
                date_data_info.append(date_data)
                self.assertEqual(date_data, order)

        print 'done'

        #============================================================================
        # Generate data for Case 2
        #============================================================================
        dates = load_order_data([] + [], db)

        #============================================================================
        # Case 2: Testing no change
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        index = 0
        for date_data in get_date_data(db):
            self.assertEqual(date_data, date_data_info[index])
            index += 1

        print 'done'

        #============================================================================
        # Generate data for Case 3
        #============================================================================
        order_data, togo_data = _populate_directory_with_random_orders(dir,
                                    save_data=False)
        dates = load_order_data(order_data.values() + togo_data.values(), db)
        load_date_data(dates, db)

        #============================================================================
        # Case 3: Testing that the order data is accurately updated, and previous
        # data remains.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        dates_data = sorted(get_date_data(db))

        # ensure data is still formatted and updated correctly.
        for date_data in dates_data:
            order_info = get_order_info(db, date_data[0])

            for order in order_info:
                date_data_info.append(date_data)
                self.assertEqual(date_data, order)

        # ensure that all rows are direct references to dates with
        # no repeats.
        self.assertEqual(len(dates_data), len(set(dates_data)))

        print 'done'

        #============================================================================
        # Generate data for Case 4
        #============================================================================
        values = (MenuItem('should raise an error', 1.0),
                 'antidisestablishmentaranism',
                 42,
                 self)

        #============================================================================
        # Case 4: Testing for appropriate error be raised given non-datetime date
        # object.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        for date in values:
            self.assertRaises(StandardError, ConfirmationSystem._update_date_table,
                              date, database=db)

        print 'done'

        #============================================================================
        # Case 5: Testing for appropriate error to be raised given non-sqlite3
        # .connection object for database.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for database in values:
            self.assertRaises(StandardError, ConfirmationSystem._update_date_table,
                              datetime.now(), database=database)

        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing date table function'
        #============================================================================

    def test_update_order_table(self):
        """Tests the update order table function

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing update order table function'
        #============================================================================
        # Testing the function that takes order data, compiles the totals,
        # item frequencies and other information and then places each unique order
        # into its own row on the table. Each table has a number representing the
        # order number.
        #
        # Initial data will be generated and then passed to the method for storage
        # as each order. Using RAM based database to ensure speed. Expect all
        # functionality performed on RAM database to be identical to that
        # performed on the standard stored database.
        #
        # Case 1:
        #
        #       Pass data and ensure that it has been created with the proper
        #       format and data for the entire row.
        #
        # Case 2:
        #
        #       Pass data that is empty. Expect raise Error
        #
        # Case 3:
        #
        #       Pass data that contains a specific number of notification items.
        #       Ensure that the table displays the appropriate number of
        #       notifications and the notification flag.
        #
        # Case 4:
        #
        #       Pass data that is specifically togo or order and ensure the
        #       correct area displays which type of order it was.
        #
        # Case 5:
        #
        #       Pass in specific number of MenuItem objects for the order,
        #       expect specific frequency data to be displayed
        #
        # Case 6:
        #
        #       Error raised when non-MenuItem order is passed in as order.
        #
        # Case 7:
        #
        #       Error raised when non-datetime object is passed in as date.
        #
        # Case 8:
        #
        #       Error raised when non-sqlite3.connection object is passed
        #       in as database.
        #============================================================================
        # Generate initial data for testing cases.
        #============================================================================
        dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY
        order_data, togo_data = _populate_directory_with_random_orders(dir,
                                    save_data=False)

        db = ConfirmationSystem._check_and_create_orders_database(':memory:')

        data = \
            _add_order_data_to_database(order_data.values() + togo_data.values(), db)

        def get_order_data(db):
            c = db.cursor()
            row_data = c.execute('SELECT '
                                 '     *'
                                 'FROM '
                                 '     OrderData;')
            return row_data.fetchall()

        def get_specific_order_data(order_number, db):
            c = db.cursor()
            row_data = c.execute('SELECT '
                                 '      *'
                                 'FROM '
                                 '      OrderData '
                                 'WHERE '
                                 '      OrderNumber=?;', (order_number,))
            return row_data.fetchall()

        #============================================================================
        # Case 1: Testing general data parsing and storage by the database. Expect
        # for the row to be accurately displayed.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertEqual(get_order_data(db), data)
        print 'done'

        #============================================================================
        # Case 2: Testing empty order given. Expect error raised
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertRaises(StandardError, ConfirmationSystem._update_order_table,
                          datetime.now(), [], 'test name', [], [], database=db)
        print 'done'

        #============================================================================
        # Generate data for Case 3.
        #============================================================================
        # Generate random names for order.
        order_name = ''.join(random.sample(POSSIBLE_CHARS, 30))
        std_name = ConfirmationSystem.standardize_file_name(order_name)

        # Generate notification list to test for.
        notification_list = []

        for x in xrange(15):

            item = DiscountItem('.'.join(random.sample(POSSIBLE_CHARS, 30)),
                                random.randint(1, 100), 'a')
            notification_list.append(item)

        notification_data = (std_name, std_name, notification_list)

        # Insert list and find order number to check for proper storage.
        updated_data = _add_order_data_to_database((notification_data,), db)

        order_number = ConfirmationSystem.current_order_counter - 1

        unpacked_data = get_specific_order_data(order_number, db)
        data += updated_data

        #============================================================================
        # Case 3: Testing notification data flag and notification data json.
        # Passing in specific notification items. Items are expected to be parsed
        # and displayed accurately in the notifications json file.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        # index 7 is the column that the notification data is in.
        self.assertEqual(unpacked_data, updated_data)
        self.assertEqual(data, get_order_data(db))
        print 'done'

        #============================================================================
        # Generating data for Case 4
        #============================================================================
        order_data, togo_data = _populate_directory_with_random_orders(dir,
                                  save_data=False)

        #============================================================================
        # Case 4: Testing order type data storage in database. Passing in a
        # specific, different order type. Expecting the specific order type to be
        # displayed correctly.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        data += _add_order_data_to_database(order_data.values(), database=db)
        unpacked_data = get_order_data(db)
        self.assertEqual(data, unpacked_data)

        data += _add_order_data_to_database(togo_data.values(), database=db)
        unpacked_data = get_order_data(db)
        self.assertEqual(data, unpacked_data)

        print 'done'

        #============================================================================
        # Generate data to test item frequency
        #============================================================================

        item_counter = Counter()

        for x in xrange(50):

            name = ''.join(random.sample(POSSIBLE_CHARS, 30))

            for num in xrange(random.randint(1, 50)):
                item_counter[name] += 1

        order_data = [MenuItem('test', 1.0)]

        data = ConfirmationSystem._update_order_table(datetime.now(), order_data,
                                                      'test_name', [],
                                                      item_counter, database=db)
        # Because the returned unpacked data will be in a list
        data = [data]

        #============================================================================
        # Case 5: Testing item frequency data storage. Passing in a specific
        # number of MenuItems in the order. Expect the frequency to be adequately
        # represented.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        unpacked_data = get_specific_order_data(
            ConfirmationSystem.current_order_counter - 1, db)
        self.assertEqual(data, unpacked_data)

        print 'done'

        #============================================================================
        # Generate data for testing error raising cases.
        #============================================================================
        values = ('antidisestablishmentaranism',
                  10.0,
                  10,
                  self,
                  [])

        #============================================================================
        # Case 6: Testing for AttributeError raised when given a list of non
        # menuitem objects as order data.
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        for order_data in values:
            self.assertRaises(StandardError, ConfirmationSystem._update_order_table,
                              datetime.now(), order_data, '', [], [], db)

        print 'done'

        #============================================================================
        # Case 7: Testing for AttributeError raised when given a non datetime
        # object as the order date.
        print TABS * 3 + 'Testing Case 7...',
        #============================================================================
        for date in values:
            self.assertRaises(StandardError, ConfirmationSystem._update_order_table,
                              date, [MenuItem('test', 1.0)], '', [], [], db)

        print 'done'

        #============================================================================
        # Case 8: Testing for AttributeError raised when given a non
        # sqlite3.connection object as the database
        print TABS * 3 + 'Testing Case 8...',
        #============================================================================
        for database in values:
            self.assertRaises(StandardError, ConfirmationSystem._update_order_table,
                              datetime.now, [MenuItem('test', 1.0)], '', [], [],
                              database=database)

        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing update order table function.'
        #============================================================================

    def test_update_item_table(self):
        """Tests the update item table function

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing update item table function'
        #============================================================================
        # This method will be testing the update item table function. It will do
        # this by generating random MenuItems and then placing them inside of the
        # table via the specified method. Each row stores specific data, some of
        # which will be tested in general with randomly generated dates, and names.
        #
        # Case 1:
        #
        #       Standard Case. Generating random names, dates and associated json
        #       data to be stored. This is the general case and any errors in the
        #       stored name, date or json text data should be uncovered here.
        #
        # Case 2:
        #
        #       Notification flag case. Test the notification flag occurs when the
        #       given MenuItem is a notification item.
        #
        # Case 3:
        #       Error raised when non datetime object is given as date
        #
        #
        # Case 4:
        #
        #       Error raised when non menu_item object is given as MenuItem.
        #
        # Case 5:
        #
        #       Error raised when non sqlite3.connection is given for database.
        #============================================================================
        # Generating initial data to perform tests
        #============================================================================
        dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY

        db = ConfirmationSystem._check_and_create_orders_database(':memory:')

        order_data, togo_data = _populate_directory_with_random_orders(dir,
                                    save_data=False)

        item_data = []
        counter = 0
        for std_name, file_path, items in order_data.values() + togo_data.values():

            f_time, f_name, f_type = \
                ConfirmationSystem.parse_standardized_file_name(std_name)

            for item in items:

                curr_data = ConfirmationSystem._update_item_table(f_time, item, db)
                item_data.append(curr_data)

            counter += 1

        def get_item_data(db):
            c = db.cursor()
            data = c.execute('SELECT '
                             '      * '
                             'FROM '
                             '      ItemData;')
            return data.fetchall()

        #============================================================================
        # Case 1: Testing the standard Case looking for matching data on a row by
        # row basis. Randomly generated menu item names, times, and prices. Focus
        # is on date, menu item data, and json str.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        unpacked_data = get_item_data(db)
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(unpacked_data, item_data)

        print 'done'

        #============================================================================
        # Generate data for test case 2.
        #============================================================================
        for x in range(random.randint(1, 100)):

            name = ''.join(random.sample(POSSIBLE_CHARS, 30))
            price = random.randint(1, 100)
            note = ''.join(random.sample(POSSIBLE_CHARS, 50))

            curr_data = ConfirmationSystem._update_item_table(datetime.now(),
                          DiscountItem(name, price, note), database=db)

            item_data.append(curr_data)


        #============================================================================
        # Case 2: Notification flag case. Testing for notification flag being
        # tripped on data.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        unpacked_data = get_item_data(db)
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(unpacked_data, item_data)

        print 'done'

        #============================================================================
        # Generate data necessary to test errors.
        #============================================================================
        values = ('antidisestalbishmentaranism',
                  10.0,
                  10,
                  True,
                  self)
        def ensure_database_unchanged(db):
            return unpacked_data == get_item_data(db)
        #============================================================================
        # Case 3: Testing error raised when a non datetime object is given as date.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for date in values:
            self.assertRaises(StandardError, ConfirmationSystem._update_item_table,
                              date, MenuItem('test', 1.0), database=db)

        self.assertTrue(ensure_database_unchanged(db))

        print 'done'

        #============================================================================
        # Case 4: Testing error raised when non menu item object is given as the
        # item.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        for item in values:
            self.assertRaises(StandardError, ConfirmationSystem._update_item_table,
                              datetime.now(), item, database=db)
        self.assertTrue(ensure_database_unchanged(db))

        print 'done'

        #============================================================================
        # Case 5: Testing error raised when a non sqlite3.connection object is
        # given as database.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for database in values:
            self.assertRaises(StandardError, ConfirmationSystem._update_item_table,
                              datetime.now(), MenuItem('test', 1.0),
                              database=database)

        self.assertTrue(ensure_database_unchanged(db))

        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing update item table function'
        #============================================================================

    def test_order_confirmed(self):
        """Tests the order confirmed function.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing order confirmed function'
        #============================================================================
        # WARNING THIS METHOD RELIES HEAVILY ON THE PARSE STANDARDIZED FILE NAME
        # FOR ITS FUNCTIONALITY. ERRORS IN THE PARSE STANDARDIZED FILE NAME SHOULD
        # BE CHECKED FIRST AND TESTING RERUN AS FAILURES COULD BE FALSE POSITIVES
        # IN THIS TEST.
        #
        # Testing the order confirmed function. This will require the generation
        # of order data that will be passed to the order
        # ConfirmationSystem.order_confirmed function.
        #
        # Case 1:
        #
        #       Standard Case. Directory doesn't contain any duplicates,
        #       adding unique orders. Expect data pulled to match identically.
        #
        # Case 2:
        #
        #       Duplicate Case. Directory contains duplicates order names. Expect
        #       duplicate to be removed from directory, and the given order to
        #       replace it entirely.
        #
        # Case 3:
        #
        #       Populated directory. All order names are parse-able.
        #
        # Case 4:
        #
        #       Given non-str order_name expect Error raised.
        #
        # //TODO provide more tests cases to test for data being accurately sent
        # //to print functions.
        #============================================================================
        # Generate initial data for test cases.
        #============================================================================
        dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY

        def pull_directory_files(dir):
            files = {}
            dirnames, dirpaths, filenames = os.walk(dir).next()

            for filename in filenames:
                with open(dir + '/' + filename, 'r') as f:
                    files[filename] = jsonpickle.decode(f.read())

            return files

        def generate_and_store_data(dir):
            data = {}

            order_data = _populate_directory_with_random_orders(dir, save_data=False)
            order_data = order_data[0].items() + order_data[1].items()

            for order_name, (std_name, file_path, file_data) in order_data:
                file_name = ConfirmationSystem.order_confirmed(order_name, [],
                                [], file_data)
                data[file_name] = file_data

            return data

        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        data = generate_and_store_data(dir)
        unpacked_data = pull_directory_files(dir)

        #============================================================================
        # Case 1: Testing standard case. Adding unique names/values as files in
        # the directory. Pulling that data and then checking they are identical.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertTrue(len(data) > 0)
        self.assertEqual(data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 2
        #============================================================================
        prev_data = data
        data = generate_and_store_data(dir)

        for file_name, order_data in prev_data.items():
            f_time, f_name, f_type = \
                ConfirmationSystem.parse_standardized_file_name(file_name)

            file_name = ConfirmationSystem.order_confirmed(f_name, [],
                                                           [], order_data)
            data[file_name] = order_data

        unpacked_data = pull_directory_files(dir)

        #============================================================================
        # Case 2: Testing
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertTrue(len(data) > 0)
        self.assertEqual(data, unpacked_data)

        print 'done'

        #============================================================================
        # Generating data for test Case 3
        #============================================================================
        order_names = unpacked_data

        #============================================================================
        # Case 3: We know at this point that both prev_data and the unpacked data
        # will be equal at any given time. This is necessary for them to pass
        # through both tests and have no other code executed. As such now I will
        # simply check that all file names are parsable.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for order_name in order_names:
            self.assertIsNotNone(
                ConfirmationSystem.parse_standardized_file_name(order_name))

        print 'done'

        #============================================================================
        # Generate data for test Case 4
        #============================================================================
        values = (10.0,
                  10,
                  self,
                  ['a', 'b', 'c', 'd'])

        order_data = [MenuItem('test', 1.0)]
        order_name = 'antidisestablishmentaranism'
        priority_order = order_data

        #============================================================================
        # Case 4: Testing error raised when improper order name is given.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        for order_names in values:
            self.assertRaises(StandardError, ConfirmationSystem.order_confirmed,
                              order_names, priority_order, order_data, order_data)
        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing order confirmed function'
        #============================================================================

    def test_checkout_confirmed(self):
        """Tests the checkout confirmed function

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing checkout confirmed function'
        #============================================================================
        # Testing the checkout confirmed function. Expect this function to add a
        # new file to the checkout directory, and remove any similarly named files
        # from the confirmed directory.
        #
        # Case 1:
        #
        #   Standard Case. unpopulated confirmed directory, unpopulated checkout
        #   directory. Adds each order to checkout directory, confirmed directory
        #   is left untouched.
        #
        # Case 2:
        #
        #   Confirmed directory is populated with non-parse-able file names that
        #   do not represent orders. previously populated checkout directory.
        #   Expect checkout directory to contain previously data and updated
        #   data. All confirmed directory files remain.
        #
        # Case 3:
        #
        #   Confirmed directory populated with only parse-able file names that
        #   represent orders. Previously populated checkout directory. Expect
        #   checkout directory to contain previous data and updated data. All
        #   confirmed directory files have been removed.
        #
        # Case 4:
        #
        #   Confirmed directory populated with both parse-able and non-parse-able
        #   filenames that represent orders and non-orders respectively.
        #   Previously populated checkout directory. Expect checkout directory to
        #   contain previous data and updated data. All parseable confirmed
        #   directory files have been removed.
        #
        # Case 5:
        #
        #   Confirmed directory populated with both parse-able and non-parse-able
        #   filenames that represent orders and non-orders respectively. Previously
        #   populated checkout directory. Given orders that represents an order
        #   split into several checks. Expect data to accurately be displayed in
        #   filenames as single order. All parse-able confirmed directory files
        #   have been removed.
        #
        # Case 6:
        #
        #   non string order name given. Expect error raised.
        #
        # //TODO provide additional test cases to test for data being accurately
        # //sent to print functions.
        #
        #============================================================================
        # Generate initial data to begin testing
        #============================================================================
        checkout_dir = path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY
        confirm_dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY

        def add_orders_data(curr_data, split_orders=False):
            data = {}

            if split_orders:
                split_data = [(x,) for x in curr_data]
            else:
                split_data = curr_data

            for order_name, (std_name, file_path, order_data) in curr_data:
                name = ConfirmationSystem.checkout_confirmed(order_name,
                                                             (split_data,),
                                                             order_data)
                data[name] = order_data

            return data

        def add_non_parseable_data(dir):
            data = {}

            for x in xrange(random.randint(1, 100)):
                name = ''.join(random.sample(string.ascii_letters, 30))
                file_data = name
                data[name] = name

                with open(dir + '/' + name, 'w') as f:
                    f.write(jsonpickle.encode(file_data))

            return data

        def pull_directory_data(dir):
            data = {}

            dirnames, dirpaths, file_names = os.walk(dir).next()
            for file_name in file_names:

                with open(dir + '/' + file_name, 'r') as f:
                    order_data = jsonpickle.decode(f.read())
                    data[file_name] = order_data

            return data

        def clear_directory(dir):
            shutil.rmtree(dir)
            os.mkdir(dir)

        #============================================================================
        # Generate data for test Case 1
        #============================================================================
        order_data, togo_data = _populate_directory_with_random_orders(
            checkout_dir, save_data=False)

        updated_data = add_orders_data(order_data.items() + togo_data.items())
        unpacked_data = pull_directory_data(checkout_dir)

        #============================================================================
        # Case 1: Testing standard care. With empty directories the given orders
        # are added and the files saved as expected.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertEqual(updated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for test Case 2
        #============================================================================
        prev_updated_data = updated_data
        non_parsed_data = add_non_parseable_data(confirm_dir)
        order_data, togo_data = _populate_directory_with_random_orders(confirm_dir,
                                   save_data=False)

        updated_data = add_orders_data(order_data.items() + togo_data.items())

        # This makes sense. Since ever file name will contain a unique time stamp.
        updated_data.update(prev_updated_data)

        unpacked_data = pull_directory_data(checkout_dir)

        unpacked_confirm_data = pull_directory_data(confirm_dir)

        #============================================================================
        # Case 2: Testing multiple files case. In this case multiple non-parse-able
        # files exist in the confirmed directory, with a list of orders that is to
        # be updated. Each file should be created in their respective area,
        # and the non-parse-able files should be left untouched and intact.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertEqual(updated_data, unpacked_data)
        self.assertEqual(non_parsed_data, unpacked_confirm_data)
        print 'done'

        #============================================================================
        # Generate data for test Case 3
        #============================================================================
        prev_updated_data = updated_data
        clear_directory(confirm_dir)

        order_data, togo_data = _populate_directory_with_random_orders(confirm_dir)

        updated_data = add_orders_data(order_data.items() + togo_data.items())
        updated_data.update(prev_updated_data)

        unpacked_data = pull_directory_data(checkout_dir)
        unpacked_confirm_data = pull_directory_data(confirm_dir)

        #============================================================================
        # Case 3: Testing confirmed directory contains only parse-able file names.
        # Orders are added that share the same file names are the parse-able files.
        # Expect that all parse-able files (all in the confirmed directory) have
        # been removed and the checkout directory contains the data.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        self.assertEqual(updated_data, unpacked_data)
        self.assertEqual(len(unpacked_confirm_data), 0)

        print 'done'

        #============================================================================
        # Generate data for test Case 4
        #============================================================================
        prev_updated_data = updated_data
        order_data, togo_data = _populate_directory_with_random_orders(confirm_dir)
        non_parsed_data = add_non_parseable_data(confirm_dir)

        updated_data = add_orders_data(order_data.items() + togo_data.items())
        updated_data.update(prev_updated_data)

        unpacked_data = pull_directory_data(checkout_dir)
        unpacked_confirm_data = pull_directory_data(confirm_dir)

        #============================================================================
        # Case 4: Testing confirmed directory contains only non-parse-able file
        # names after it has contained both parseable and non-parseable file names.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        self.assertEqual(updated_data, unpacked_data)
        self.assertEqual(unpacked_confirm_data, non_parsed_data)

        print 'done'

        #============================================================================
        # Generate data for test Case 5
        #============================================================================
        prev_updated_data = updated_data
        prev_non_parsed_data = non_parsed_data
        order_data, togo_data = _populate_directory_with_random_orders(confirm_dir)

        updated_data = add_orders_data(order_data.items() + togo_data.items(),
                                       split_orders=True)
        updated_data.update(prev_updated_data)

        unpacked_data = pull_directory_data(checkout_dir)
        unpacked_confirm_data = pull_directory_data(confirm_dir)

        #============================================================================
        # Case 5: Testing that the introduction of a split check doesn't alter the
        # functionality of the function.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        self.assertEqual(updated_data, unpacked_data)
        self.assertEqual(unpacked_confirm_data, prev_non_parsed_data)

        print 'done'

        #============================================================================
        # Generate data for test Case 6
        #============================================================================
        values = (open,
                  10.0,
                  10,
                  self)

        order_data = [MenuItem('testing', 1.0)]

        #============================================================================
        # Case 6: Testing for a non-string given as order name
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        for order_name in values:
            self.assertRaises(StandardError, ConfirmationSystem.checkout_confirmed,
                              order_name, (order_data,), order_data)

        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing checkout confirmed function'
        #============================================================================
