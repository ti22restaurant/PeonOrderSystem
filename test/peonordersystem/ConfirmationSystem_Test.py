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

import heapq
from collections import Counter, deque
from datetime import date, time, datetime, timedelta


from src.peonordersystem import path
from src.peonordersystem.interface.Reservations import Reserver
from src.peonordersystem.MenuItem import MenuItem, DiscountItem

from src.peonordersystem.CheckOperations import (get_order_subtotal,
                                                 get_total_tax,
                                                 get_total)
from src.peonordersystem.PackagedData import (PackagedDateData,
                                              PackagedOrderData,
                                              PackagedItemData)

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

from test.TestingFunctions import (save_data_to_file,
                                   get_data_from_file,
                                   generate_random_names,
                                   generate_random_times,
                                   generate_random_menu_items,
                                   generate_random_reservations)

from test.Settings import (POSSIBLE_CHARS,
                           TABS,
                           NUMBER_OF_ITEMS_TO_GENERATE,
                           NUM_OF_CHARS,
                           GENERATOR_MAX)

NUM_OF_CYCLES = NUMBER_OF_ITEMS_TO_GENERATE
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
# This block contains generator functions that are utilized in the module to
# generate data.
#====================================================================================
def _populate_non_parseable_random_files(directory, n=NUMBER_OF_ITEMS_TO_GENERATE,
                                         from_chars=string.ascii_letters + string.digits):
    """Generates random non-parseable files
    in the given directory.

    This function is used to add "filler" to
    a directory.

    @param directory: str representing the
    directory to be filled with random file data.

    @return: None
    """
    file_names = []
    rand_names = generate_random_names(from_chars=from_chars * 10)

    for x in xrange(n):
        name = rand_names.next()
        save_data_to_file(name, directory + '/' + name)

        heapq.heappush(file_names, name)

    return sorted(file_names)


def _populate_orders_data_files(directory, n=NUM_OF_CYCLES,
                                num_of_chars=NUM_OF_CHARS,
                                is_checkout=False):
    """Populates the given directory with n
    number of random order files.

    @param directory: str representing the directory
    that the files should be saved to.

    @keyword n: int representing the number of files
    to generate. Default NUM_OF_CYCLES.

    @return dict of (datetime, str, str) keys which
    represent the parsed file data. Mapped to str
    representing the files location.
    """
    data = {}

    rand_orders = _generate_random_order(num_of_chars=num_of_chars,
                                         is_checkout=is_checkout)
    for x in xrange(n):
        std_name, order_data = rand_orders.next()
        file_path = directory + '/' + std_name

        save_data_to_file(order_data, file_path)

        p_time, p_name, p_type = ConfirmationSystem.parse_standardized_file_name(
            std_name)

        data[p_time, p_name, p_type] = file_path, order_data

    rand_orders.close()
    return data


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
    reserver_data = []
    reserver_data_by_date = {}
    rand_rsvr = generate_random_reservations()

    for x in xrange(n):
        reserver = rand_rsvr.next()
        reserver_data.append(reserver)

        # Store data in appropriate area.
        rsvr_date = datetime.combine(reserver._arrival_time.date(), time.min)
        if rsvr_date in reserver_data_by_date:
            bisect.insort(reserver_data_by_date[rsvr_date], reserver)
        else:
            reserver_data_by_date[rsvr_date] = [reserver]

    rand_rsvr.close()

    return reserver_data, reserver_data_by_date


def _generate_random_order(num_of_chars=NUM_OF_CHARS,
                           notification=0.0, is_checkout=False, n=GENERATOR_MAX):
    """Gives a generator that yields a random
    order.

    @keyword num_of_chars: int representing the
    number of characters that should be present
    in any given generated name. Default 100.

    @keyword notification: float representing the
    probability of any given notification item
    being a notification item. Default 0.0

    @keyword is_checkout: bool value representing
    if this random order should be standardized as
    a checkout order or not. Default False

    @keyword n: int representing the number of
    items this generator should be capable of
    generating. This is to ensure that an
    indefinite loop doesn't occur. Default
    GENERATOR_MAX.

    @return: generator that yields values

    @yield: str, list of MenuItem objects
    representing the standardized name and
    the order data.
    """
    rand_times = generate_random_times()
    rand_names = generate_random_names(num_of_chars=num_of_chars)
    rand_items = generate_random_menu_items(n=n*30, is_notification=notification)

    counter = 0

    while counter < n:
        order_name = rand_names.next()
        file_time = rand_times.next()
        order_data = [rand_items.next() for x in xrange(NUM_OF_CYCLES)]

        std_name = ConfirmationSystem.standardize_file_name(order_name,
                                                            is_checkout=is_checkout,
                                                            set_time=file_time)

        yield std_name, order_data

        counter += 1

    rand_times.close()
    rand_names.close()
    rand_items.close()


# This is a subset utilized to generate ordered data.

def _generate_ordered_times(start_date=MIN_DATETIME, end_date=MAX_DATETIME,
                               n=NUMBER_OF_ITEMS_TO_GENERATE):
    """Generates an ordered list of datetime.datetime objects that
    all adhere to the specific date range.

    @param start_date: datetime.datetime object that
    represents the start date. Inclusive.

    @param end_date: datetime.datetime object that
    represents the end date. Inclusive.

    @param n: int representing the number of dates
    to generate.

    @return: Generator that yields

    @yield: Yields a datetime object within the specifics range.
    """
    prev_date = start_date
    maximum_change_in_time = (end_date - start_date) / n

    counter = 0
    while counter < n:
        time_data = {
            'days': random.randint(1, maximum_change_in_time.days),
            'seconds': random.randint(1, maximum_change_in_time.seconds),
            'microseconds': 0
        }
        data = prev_date + timedelta(**time_data)
        prev_date = data

        counter += 1
        yield data


#====================================================================================
# This block contains helper functions that are used through multiple tests to
# add, push, pull, parse, unpack, convert, or otherwise interact with stored data
# or alter input to have same values are stored data.
#====================================================================================

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
                     'FROM '
                     '     {}'.format(table_name))
    return data.next()[0]


def _get_random_stored_date_data(generated_stored_data,
                                 n=NUMBER_OF_ITEMS_TO_GENERATE / 2):
    """Gets a dict of date ranges, where each key is mapped
    to a deque of the data within the date ranges.

    All data ranges will be chosen from 6 cases:

        1.  Exceeding both bounds from generated_stored_data and
            expecting it to encompass all data given

        2.  Proceeding lower bound from generated_stored_data, matching
            upper bound and expecting it to encompass all data given

        3.  Exceeding upper bound from generated_stored_data, matching
            lower bound and expecting it to encompass all data given

        4.  Both proceeding lower bound from generated_stored_data and
            expecting it to be an empty data set

        5.  Both exceeding upper bound from generated_stored_data and
            expecting it to be an empty data set

        6.  Randomly chosen dates within the upper and lower bounds
            expect data set to match those whose date range they span.

    @param generated_stored_data: collection of
    PackagedData subclasses that represent
    the data.

    @param n: number of items to generate. Will
    generate n + 5 items. Encompassing all possibilities.

    @return: dict of tuple (datetime.datetime, datetime.datetime)
    representing the date range of the data set. This is mapped
    to the values which represent a deque of the data sorted by
    date.
    """
    data = {}
    itr = iter(generated_stored_data)
    subsection_range = int(len(generated_stored_data) / n)

    begin_date = generated_stored_data[0].date
    end_date = generated_stored_data[-1].date

    #add data that exceeds both bounds. Expect it to match all data.
    data[begin_date - timedelta(days=100),
         end_date + timedelta(days=100)] = generated_stored_data

    #add data that exceeds start bounds but matches end bounds
    data[begin_date - timedelta(days=100), end_date] = generated_stored_data

    #add data that exceeds end bounds but matches start bounds
    data[begin_date, end_date + timedelta(days=100)] = generated_stored_data

    #add data that is outside of range on the lower side
    data[begin_date - timedelta(days=100),
         begin_date - timedelta(days=1)] = deque()

    #add data that is outside of range on the higher side
    data[end_date + timedelta(days=1),
         end_date + timedelta(days=100)] = deque()

    for x in xrange(n - 1):
        curr_data = deque()
        info = itr.next()
        curr_data.append(info)

        date1 = info.date

        counter = 1
        while counter < (subsection_range - 2):
            curr_data.append(itr.next())
            counter += 1

        info = itr.next()
        date2 = info.date
        curr_data.append(info)

        data[date1, date2] = curr_data

    return data


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
        #   Invalid dates data passed in to standardize. Expect standardize to
        #   generate date at time of call.
        #============================================================================
        # Generate initial data to test
        #============================================================================
        standardize = ConfirmationSystem.standardize_file_name
        parse = ConfirmationSystem.parse_standardized_file_name

        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        rand_name = generate_random_names()

        #============================================================================
        # Case 1: Testing that the a given name can be standardized, then parsed
        # and reverts to its original name.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        for x in xrange(NUM_OF_CYCLES):
            name = rand_name.next()

            std_name = standardize(name)
            _, p_name, _ = parse(std_name)

            self.assertEqual(name, p_name)

        print 'done'

        #============================================================================
        # Generate data for testing Case 2
        #============================================================================
        rand_time = generate_random_times()

        #============================================================================
        # Case 2: Testing first that the standardized data matches the parsed data.
        # Next testing that the auto generated time was accurately displayed in
        # both the standardized and parsed data.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        for x in xrange(NUM_OF_CYCLES):
            name = rand_name.next()
            t = rand_time.next()

            std_name = standardize(name, set_time=t)
            p_time, p_name, _ = parse(std_name)

            self.assertEqual(t, p_time)
            self.assertEqual(name, p_name)

        print 'done'

        #============================================================================
        # Case 3: Testing first the standardized data matches the parsed data. Next
        # testing that the parsed bool values match the generated bool values.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for x in xrange(NUM_OF_CYCLES):
            name = rand_name.next()
            is_checkout = random.choice([True, False])

            std_name = standardize(name, is_checkout=is_checkout)
            _, p_name, p_type = parse(std_name)

            self.assertEqual(is_checkout, p_type == TYPE_SUFFIX_CHECKOUT)
            self.assertEqual(name, p_name)

        print 'done'

        #============================================================================
        # Testing Case 4: Testing for empty order name. Should raise ValueError
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        self.assertRaises(StandardError, standardize, '')
        self.assertRaises(StandardError, parse, '')

        print 'done'

        #============================================================================
        # Generate Case 5 data: Generating the data the execute test case 5.
        #============================================================================
        rand_name.close()
        rand_time.close()

        chr = ''.join(BLACKLIST.keys())
        rand_name = generate_random_names(from_chars=(POSSIBLE_CHARS * 10 + chr))

        #============================================================================
        # Testing Case 5: Testing for situation involving name where known invalid
        # blacklisted characters are given. First test is checking for original
        # names being equal to the names retrieved after standardization. Second
        # test is checking tha the standardized data input/output was the same as
        # the parsed data output/input.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for x in xrange(NUM_OF_CYCLES):
            name = rand_name.next()

            std_name = standardize(name)
            _, p_name, _ = parse(std_name)

            self.assertEqual(name, p_name)

        print 'done'

        #============================================================================
        # Generate data for testing Case 6
        #============================================================================
        values = (rand_name.next(),
                  'antidisestablishmentaranism',
                  10.0,
                  10,
                  lambda x: x,
                  self)

        #============================================================================
        # Testing Case 6: non pattern string given to parse function. Expect error
        # to be raised.
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        for name in values:
            self.assertRaises(StandardError, parse, name)
        print 'done'

        #============================================================================
        # Testing Case 7: Given invalid date. Expect all dates to be set to the
        # current date, within an error range of 5 seconds.
        print TABS * 3 + 'Testing Case 7...',
        #============================================================================
        for set_time in values:
            name = rand_name.next()

            std_name = standardize(name, set_time=set_time)
            p_time, p_name, _, = parse(std_name)

            self.assertEqual(name, p_name)
            self.assertTrue((p_time - datetime.now()) < timedelta(seconds=1))

        print 'done'

        rand_name.close()
        rand_time.close()
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

        load = ConfirmationSystem._load_data
        rand_order = _generate_random_order()

        #============================================================================
        # Case 1: Checking that data loads properly
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        for x in xrange(NUM_OF_CYCLES):
            std_name, order_data = rand_order.next()
            file_path = curr_dir + '/' + std_name

            save_data_to_file(order_data, file_path)
            unpacked_data = load(file_path)

            self.assertTrue(len(unpacked_data) > 0)
            self.assertEqual(unpacked_data, order_data)
        print 'done'

        #============================================================================
        # Case 2: Checking that data doesn't load and raises error instead.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        std_name, _ = rand_order.next()

        self.assertRaises(StandardError, load, curr_dir + '/' + std_name)
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

        find = ConfirmationSystem._find_order_name_paths
        _populate_non_parseable_random_files(curr_dir, from_chars=string.ascii_letters)
        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        order_data = _populate_orders_data_files(curr_dir)

        #============================================================================
        # Case 1: All values returned should be exactly the correct path.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        for key in order_data:
            _, order_name, _ = key

            data = find(order_name, curr_dir)
            file_path, _ = order_data[key]
            self.assertEqual(data, [file_path])

        print 'done'

        #============================================================================
        # Generate data for testing Case 2: Data generated will be identical to
        # the previous data which is still stored in the directory, save a single
        # index. The index will be changed to be nearly identical to the previous
        # order name. For completeness there are multiple indexes chosen,
        # and multiple index shifts (addition vs replacement) that occurs to allow
        # for a sufficiently large data set to be gathered and analyzed.
        #============================================================================
        prev_order_data = order_data
        order_data = {}
        for p_time, p_name, p_type in prev_order_data:

            # ensure that the index replacement works at both limits and any random
            # index in the range.
            for index in [0, random.randint(1, len(order_name)), len(order_name)]:

                for shift in [0, 1]:
                    order_name = p_name[:index] + p_name[index + shift:]
                    std_name = ConfirmationSystem.standardize_file_name(order_name,
                                                                        set_time=p_time)
                    file_path = curr_dir + '/' + std_name
                    save_data_to_file(None, file_path)
                    order_data[p_time, p_name, p_type] = [file_path]

        #============================================================================
        # Case 2: Expect all generated dicts to match the unpacked dicts. This
        # means that the order names have been found without pulling the
        # previously stored data.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        for key in order_data:
            _, order_name, _ = key

            data = find(order_name, curr_dir)
            self.assertEqual(data, order_data[key])
        print 'done'

        #============================================================================
        # Generate data for testing Case 3: Test case 3 is testing the identical
        # order name but differing time stamps. As such data is generated that
        # matches this description. This means pulling the previous data and
        # resaving it with a new time stamp.
        #============================================================================
        for p_time, p_name, p_type in order_data:
            for x in range(1, 3):
                curr_time = datetime.now() + timedelta(days=x)
                std_name = ConfirmationSystem.standardize_file_name(p_name,
                                                                    set_time=curr_time)
                file_path = curr_dir + '/' + std_name
                save_data_to_file(None, file_path)

                order_data[p_time, p_name, p_type] += [file_path]

        #============================================================================
        # Case 3: Expect the list to contain the correct file path, but not
        # necessarily that specific unique file path.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for key in order_data:
            _, order_name, _ = key

            data = find(order_name, curr_dir)
            self.assertEqual(data.sort(), order_data[key].sort())
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

        def generate_data_comparison(generated_data, unpacked_data):
            for key in generated_data:
                order_time, order_name, _ = key
                _, g_data = generated_data[key]

                if TOGO_SEPARATOR in order_name:
                    u_data = unpacked_data[1][order_name, order_time]
                else:
                    u_data = unpacked_data[0][order_name, order_time]

                yield u_data, g_data

        unpack = ConfirmationSystem.unpack_order_data
        #============================================================================
        # Generate data for Case 1
        #============================================================================
        generated_data = _populate_orders_data_files(curr_dir)
        unpacked_data = unpack(curr_dir)

        #============================================================================
        # Testing Case 1: Checking that the generated data and unpacked data are
        # equal.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        for u_data, g_data in generate_data_comparison(generated_data, unpacked_data):
            self.assertEqual(u_data, g_data)
        print 'done'

        #============================================================================
        # Generate data for Case 2
        #============================================================================
        prev_generated_data = generated_data

        generated_data = _populate_orders_data_files(curr_dir)
        generated_data.update(prev_generated_data)

        unpacked_data = unpack(curr_dir)

        #============================================================================
        # Testing Case 2: Checking that all appropriately returned data has been
        # returned in the appropriate form of key = (str, float) representing the
        # associated order name and time respectively.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        for u_data, g_data in generate_data_comparison(generated_data, unpacked_data):
            self.assertEqual(u_data, g_data)
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
        _populate_non_parseable_random_files(curr_dir)

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
        generated_data = _populate_orders_data_files(curr_dir)
        unpacked_data = unpack(curr_dir)

        #============================================================================
        # Case 5: Testing similar to Case 1 with added constraints of new
        # directory and randomly generated non-parse-able files. Expect for only
        # generated data to be unpacked.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for u_data, g_data in generate_data_comparison(generated_data, unpacked_data):
            self.assertEqual(u_data, g_data)
        print 'done'

        #============================================================================
        # Generate data for Case 6
        #============================================================================
        prev_generated_data = generated_data

        generated_data = _populate_orders_data_files(curr_dir)
        generated_data.update(prev_generated_data)

        unpacked_data = unpack(curr_dir)

        #============================================================================
        # Case 6: Testing similar to Case 2 with added constraints of new
        # directory and randomly generated non-parse-able files. Expect for
        # previously generated data and new generated data to be unpacked.
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        for u_data, g_data in generate_data_comparison(generated_data, unpacked_data):
            self.assertEqual(u_data, g_data)
        print 'done'

        #============================================================================
        # Generate data for Case 7
        #============================================================================
        values = ('antidisestablishmentaranism',
                  10.0,
                  10,
                  None,
                  lambda x: x,
                  self)

        #============================================================================
        # Case 7: Given non existing directory or non str expect error.
        print TABS * 3 + 'Testing Case 7...',
        #============================================================================
        for directory in values:
            self.assertRaises(StandardError, unpack, directory)
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
        #   Directory contains only non-parseable file names. Expect empty dict.
        #
        # Case 2:
        #
        #   Directory contains only parseable file names. Expect dict returned to
        #   contain the data of both the order data and togo data.
        #
        # Case 3:
        #
        #   Directory contains both parseable and non parseable file names. Expect
        #   dict returned to contain the data of both the order data and togo data.
        #
        #============================================================================
        # Generate initial data for testing
        #============================================================================
        curr_dir = path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY

        def generate_data_comparison(generated_data, unpacked_data):
            for key in generated_data:
                order_time, order_name, _ = key
                _, g_data = generated_data[key]

                u_data = unpacked_data[order_name, order_time]

                yield u_data, g_data

        def clear_directory(dir):
            shutil.rmtree(dir)
            os.mkdir(dir)

        unpack = ConfirmationSystem.unpack_checkout_data

        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        _populate_non_parseable_random_files(curr_dir)

        generated_data = {}
        unpacked_data = unpack()

        #============================================================================
        # Case 1: Expect unpacked data to match the items of the combined order
        # data and togo data.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 2
        #============================================================================
        clear_directory(curr_dir)

        generated_data = _populate_orders_data_files(curr_dir)
        unpacked_data = unpack()

        #============================================================================
        # Case 2: Expect unpacked data to match the items of the combined order
        # data and togo data.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        for u_data, g_data in generate_data_comparison(generated_data,  unpacked_data):
            self.assertEqual(u_data, g_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 3
        #============================================================================
        _populate_non_parseable_random_files(curr_dir)

        prev_generated_data = generated_data
        generated_data = _populate_orders_data_files(curr_dir)
        generated_data.update(prev_generated_data)

        unpacked_data = unpack()

        #============================================================================
        # Case 3: Expect unpacked data to be empty.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for u_data, g_data in generate_data_comparison(generated_data,  unpacked_data):
            self.assertEqual(u_data, g_data)
        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing unpack checkout function.'
        #============================================================================

    def test_get_stored_date_data(self):
        """Tests the get stored date data function

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing get stored date data function'
        #============================================================================
        # This function should retrieve the stored date database data in the given
        # date range, from the keyword database which is default the
        # ORDERS_DATABASE constant for the module.
        #
        # Case 1:
        #
        #   Empty database. Given specific range. Expect empty data to be returned.
        #
        # Case 2:
        #
        #   Populated database, given specific range. Expect data returned to
        #   match the range, inclusive.
        #
        # Case 3:
        #
        #   Given date range such that start date > end date. Expect error.
        #
        # Case 4:
        #
        #   Given non-datetime object for start date. Expect error.
        #
        # Case 5:
        #
        #   Given non-datetime object for end date. Expect error.
        #
        # Case 6:
        #
        #
        #   Given non sqlite3.Connection object as database. Expect error.
        #============================================================================
        # Generate initial data for testing.
        #============================================================================
        db = ConfirmationSystem._check_and_create_orders_database(':memory:')

        def generate_data(db, n=NUMBER_OF_ITEMS_TO_GENERATE, num_of_orders=10):
            data = deque()

            rand_time = _generate_ordered_times(n=n)
            rand_name = generate_random_names(n=n * num_of_orders)
            rand_item = generate_random_menu_items(n=10*n)

            for x in xrange(n):
                order_time = rand_time.next()
                order_data = [rand_item.next() for x in xrange(10)]

                for y in xrange(num_of_orders):
                    update_order(order_time, order_data, rand_name.next(), [], [],
                                 database=db)

                date_data = update(order_time, database=db)

                data.append(PackagedDateData(date_data))

            return data



        update = ConfirmationSystem._update_date_table
        update_order = ConfirmationSystem._update_order_table

        unpack = ConfirmationSystem.get_stored_date_data
        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        start_date = datetime.now() - timedelta(days=1000)
        end_date = datetime.now() + timedelta(days=1000)

        unpacked_data = unpack(start_date, end_date, database=db)

        #============================================================================
        # Case 1: Testing case 1, given empty database pulled data is empty.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertEqual(unpacked_data, deque())
        print 'done'

        #============================================================================
        # Generate data for testing Case 2
        #============================================================================
        initial_generated_data = generate_data(db)
        generated_data = _get_random_stored_date_data(initial_generated_data)

        #============================================================================
        # Case 2: Testing data generated over multiple date ranges. Including
        # boundary cases.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        for (min_date, max_date), stored_data in generated_data.items():
            unpacked_data = unpack(min_date, max_date, database=db)
            self.assertEqual(unpacked_data, stored_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 3
        #============================================================================
        start_date = datetime.now()
        end_date = datetime.now()

        td = timedelta(seconds=1)

        f = unpack
        #============================================================================
        # Case 3: Testing start date > end date. Expect error.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        self.assertRaises(StandardError, f, start_date + td, end_date, db)
        print 'done'

        #============================================================================
        # Generate data for testing Case 4
        #============================================================================
        values = ('antidisestablishmentaranism',
                  10.0,
                  10,
                  None,
                  True,
                  lambda x: x,
                  self)

        from_date = datetime.now()
        until_date = datetime.now() + timedelta(seconds=1)

        #============================================================================
        # Case 4: Testing for non-datetime object for start date. Expect error.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        for start_date in values:
            self.assertRaises(StandardError, f, start_date, until_date, db)
        print 'done'

        #============================================================================
        # Case 5: Testing for non-datetime object for end date. Expect error.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for end_date in values:
            self.assertRaises(StandardError, f, from_date, end_date, db)
        print 'done'

        #============================================================================
        # Case 6: Testing for non-sqlite3.Connection object given as database.
        # Expect error.
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        for database in values:
            self.assertRaises(StandardError, f, from_date, until_date, database)
        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing get stored date data function'
        #============================================================================

    def test_get_stored_order_data(self):
        """Tests the get_stored_order_data function.

        @return: None
        """
        #============================================================================
        print TABS * 2 + 'Testing the get stored order data function'
        #============================================================================
        # This function should retrieve the stored database data in the given date
        # range, from the keyword database which is default the ORDERS_DATABASE
        # constant for the module.
        #
        # Case 1:
        #
        #   Empty database. Given specific range. Expect empty data to be returned.
        #
        # Case 2:
        #
        #   Populated database. Given specific range. Expect data returned
        #   to match data within that range
        #
        # Case 3:
        #
        #   Populated database. Given specific range where start date is less than
        #   the end date. Expect raise error.
        #
        # Case 4:
        #
        #   Populated database. Given non datetime start_date expect error raised.
        #
        # Case 5:
        #
        #   Populated database. Given non datetime end_date expect error raised.
        #
        # Case 6:
        #
        #   Populated database. Given non sqlite3.Connection object for database
        #   expect error raised.
        #============================================================================
        # Generate initial data for testing.
        #============================================================================
        db = ConfirmationSystem._check_and_create_orders_database(':memory:')

        def generate_data(package_class, n=NUMBER_OF_ITEMS_TO_GENERATE):
            data = deque()

            rand_name = generate_random_names(n=n)
            rand_ordered_time = _generate_ordered_times(n=n)
            rand_item = generate_random_menu_items(n=n*30)

            counter = 0

            for x in xrange(n):
                order_name = rand_name.next()
                order_date = rand_ordered_time.next()
                order_data = [rand_item.next() for y in xrange(30)]

                curr_data = ConfirmationSystem._update_order_table(order_date,
                                                                   order_data,
                                                                   order_name,
                                                                   [], [],
                                                                   database=db)

                curr_data = PackagedOrderData(curr_data)
                data.append(curr_data)

            return data

        unpack = ConfirmationSystem.get_stored_order_data
        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        start_date = datetime.now() - timedelta(days=1)
        end_date = datetime.now() + timedelta(days=1)

        unpacked_data = unpack(start_date, end_date, database=db)

        #============================================================================
        # Case 1: Empty data set. Expect empty data set returned.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertEqual(unpacked_data, deque())
        print 'done'

        #============================================================================
        # Generate data for testing Case 2. Each generated data is expected to be
        # a dict that has a key representing the dates range. This is mapped to
        # the expected dict outputted from any given call on get_stored_order_data.
        #============================================================================
        initial_generated_data = generate_data(db)
        generated_data = _get_random_stored_date_data(initial_generated_data)

        #============================================================================
        # Case 2: Populated data set. Randomly chosen times that represent both
        # inside and outside data range. Expect generated data and unpacked data
        # to be equal.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        for (min_date, max_date), stored_data in generated_data.items():
            unpacked_data = unpack(min_date, max_date, database=db)
            self.assertEqual(unpacked_data, stored_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 3
        #============================================================================
        start_date = datetime.now()
        end_date = datetime.now()

        change_in_date = timedelta(days=10)

        f = ConfirmationSystem.get_stored_order_data
        #============================================================================
        # Case 3: Testing for case where end date is less than start date. Expect
        # error raised.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        self.assertRaises(StandardError, f, start_date, end_date - change_in_date, db)
        print 'done'

        #============================================================================
        # Generate data for testing Case 4
        #============================================================================
        values = ('antidisestablishmentaranism',
                  10.0,
                  10,
                  lambda x: x,
                  self,
                  datetime.date)

        #============================================================================
        # Case 4: Testing for case where start date is non datetime object.
        # Expect error raised.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        for start_date in values:
            self.assertRaises(StandardError, f, start_date, end_date, db)
        print 'done'

        #============================================================================
        # Case 5: Testing for case where end date is non datetime object. Expect
        # error raised.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for end_date in values:
            self.assertRaises(StandardError, f, start_date, end_date, db)
        print 'done'

        #============================================================================
        # Case 6: Testing for case where database is non sqlite3.connection object.
        # Expect error raised.
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        for database in values:
            self.assertRaises(StandardError, f, start_date, end_date, database)
        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing the get stored order data function'
        #============================================================================

    def test_get_stored_item_data(self):
        """Tests the get stored item data function.

        @return: None
        """
        #============================================================================
        print TABS * 3 + 'Testing get stored item data function'
        #============================================================================
        # This function is expected to retrieve specific order item data within a
        # certain date range.
        #
        # Case 1:
        #
        #   Empty database. Attempting to pull data expect empty set.
        #
        # Case 2:
        #
        #   Populated database. Pull data within random given date ranges.
        #   Including boundary cases. Expect data to match generated data.
        #
        # Case 3:
        #
        #   Given date ranges such that start_date > end_date. Expect error.
        #
        # Case 4:
        #
        #   Given start date that is non-datetime object. Expect error.
        #
        # Case 5:
        #
        #   Given end date that is non-datetime object. Expect error.
        #
        # Case 6:
        #
        #   Given non-sqlite3.Connection for database. Expect error.
        #============================================================================
        # Generate initial data
        #============================================================================
        db = ConfirmationSystem._check_and_create_orders_database(':memory:')

        def generate_data(n=NUMBER_OF_ITEMS_TO_GENERATE):
            data = deque()

            rand_item = generate_random_menu_items(n=n)
            rand_date = _generate_ordered_times(n=n)

            for x in xrange(n):
                row_data = ConfirmationSystem._update_item_table(rand_date.next(),
                                                                 rand_item.next(),
                                                                 database=db)
                data.append(PackagedItemData(row_data))

            return data

        unpack = ConfirmationSystem.get_stored_item_data
        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        unpacked_data = unpack(datetime.now(),
                               datetime.now() + timedelta(days=1),
                               database=db)

        #============================================================================
        # Case 1: Testing that the data returned is empty because it is out of
        # known range.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertEqual(unpacked_data, deque())
        print 'done'

        #============================================================================
        # Generate data for testing Case 2
        #============================================================================
        generated_data = generate_data()
        generated_data = _get_random_stored_date_data(generated_data)

        #============================================================================
        # Case 2: Testing that the data returned matches the data generated
        # including boundary cases.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        for (min_date, max_date), order_data in generated_data.items():
            unpacked_data = unpack(min_date,  max_date, database=db)
            self.assertEqual(unpacked_data, order_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 3
        #============================================================================
        start_date = datetime.now()
        end_date = datetime.now()

        change = timedelta(seconds=1)

        #============================================================================
        # Case 3: Given start date > end date expect error.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        self.assertRaises(StandardError, unpack, start_date + change, end_date, db)
        print 'done'

        #============================================================================
        # Generate data for testing Case 4
        #============================================================================
        values = ('Antidisestablishmentaranism',
                  10,
                  10.0,
                  None,
                  date.today(),
                  lambda x: x,
                  self)

        #============================================================================
        # Case 4: Testing for non-datetime object in as the start date. Expect
        # error raised.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        for curr_date in values:
            self.assertRaises(StandardError, unpack, curr_date, end_date, db)
        print 'done'

        #============================================================================
        # Case 5: Testing for non-datetime object in as the end date. Expect error
        # raised.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for curr_date in values:
            self.assertRaises(StandardError, unpack, start_date, curr_date, db)
        print 'done'

        #============================================================================
        # Case 6: Testing for non-sqlite3.Connection object given as database.
        # Expect error raised.
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        for database in values:
            self.assertRaises(StandardError, unpack, start_date, end_date, database)
        print 'done'
        #============================================================================
        print TABS * 2 + 'Finished testing get stored item data function'
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

            order_data = _populate_orders_data_files(dir)

            for key in order_data:
                p_time, p_name, p_type = key
                _, file_data = order_data[key]

                name = ConfirmationSystem.standardize_file_name(p_name,
                                                                set_time=p_time)

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
        _populate_non_parseable_random_files(curr_dir)
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

        def generate_data(dir, n=NUM_OF_CYCLES):
            data = {}

            rand_name = generate_random_names(n=n)
            rand_item = generate_random_menu_items(n=n*10)

            for x in xrange(n):
                std_name = ConfirmationSystem.standardize_file_name(rand_name.next())
                file_path = dir + '/' + std_name

                file_data = [rand_item.next() for y in xrange(10)]
                data[file_path] = file_data

                ConfirmationSystem._save_order_file_data(file_data, file_path)

            rand_name.close()
            rand_item.close()
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
        _populate_non_parseable_random_files(curr_dir)
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

            order_data = _populate_orders_data_files(dir, is_checkout=True)

            for key in order_data:
                p_time, p_name, p_type = key

                file_path, file_data = order_data[key]

                data[p_name, p_time] = file_data

                data_paths.append(file_path)

            return data, data_paths

        def unpack_data(file_data):
            data = {}
            rand_name = generate_random_names(num_of_chars=50)

            for p_name, p_time in file_data:
                name = rand_name.next()
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
        _populate_non_parseable_random_files(curr_dir)
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
        # WARNING: This method relies heavily on the get unpacked data functions.
        # Any errors in the get unpacked data functions could cause errors here.
        #
        # Testing the update orders database requires the checkout directory to be
        # populated with files that are to be added to the database. All database
        # operations are performed from the RAM by using the ":memory:" parameter
        # for connection. This is to allow the tests to be executed quickly. All
        # database functions take an optional keyword argument that sets the
        # database being operated on.
        #
        #   Case 1:
        #
        #       Empty Checkout directory. Nothing is added to the temporary
        #       database
        #
        #   Case 2:
        #
        #       Fully populated Checkout directory. Every order is pulled and
        #       added to a specific temporary database.
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
        # Generate initial data for testing.
        #============================================================================
        curr_dir = path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY
        db = ConfirmationSystem._check_and_create_orders_database(':memory:')

        def generate_data_files(dir, n=NUM_OF_CYCLES, num_of_items=5):
            date_data = []
            order_data = []
            item_data = []

            rand_time = _generate_ordered_times()
            rand_name = generate_random_names()
            rand_item = generate_random_menu_items()

            for x in xrange(n):
                order_name = rand_name.next()
                curr_order = []

                item = rand_item.next()
                item_data.append((jsonpickle.encode(item),))
                curr_order.append(item)

                order_time = rand_time.next()
                order_data.append((jsonpickle.encode(curr_order),))
                date_data.append((order_time.strftime(SQLITE_DATE_FORMAT_STR),))

                std_name = ConfirmationSystem.standardize_file_name(order_name,
                                                                    set_time=order_time)
                save_data_to_file(curr_order, dir + '/' + std_name)

            return date_data, order_data, item_data

        update = ConfirmationSystem.update_orders_database

        def get_database_table_data(db):
            c = db.cursor()

            # Generate date database data
            row_data = c.execute('SELECT '
                                 '      Date '
                                 'FROM '
                                 '      DateData '
                                 'ORDER BY '
                                 '      Date;')
            date_data = row_data.fetchall()

            # Generate order database data
            row_data = c.execute('SELECT '
                                 '      OrderData_json '
                                 'FROM '
                                 '      OrderData '
                                 'ORDER BY '
                                 '      OrderDate;')
            order_data = row_data.fetchall()

            # Generate item database data
            row_data = c.execute('SELECT '
                                 '      ItemData_json '
                                 'FROM '
                                 '      ItemData '
                                 'ORDER BY '
                                 '      ItemDate;')
            item_data = row_data.fetchall()

            return date_data, order_data, item_data

        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        update(database=db)

        unpacked_item_data, unpacked_order_data, unpacked_date_data = \
            get_database_table_data(db)

        #============================================================================
        # Case 1: Testing empty list and empty Checkout directory. Expected 0 rows
        # added to database.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertEqual(unpacked_date_data, [])
        self.assertEqual(unpacked_order_data, [])
        self.assertEqual(unpacked_item_data, [])
        print 'done'

        #============================================================================
        # Generating data for Case 2.
        #============================================================================
        date_data, order_data, item_data = generate_data_files(curr_dir)

        update(database=db)

        unpacked_date_data, unpacked_order_data, unpacked_item_data = \
            get_database_table_data(db)

        #============================================================================
        # Case 2: Fully populated checkout directory. Pulling all data from
        # checkout and loading it into the temporary database. This case will
        # check that the data is pulled, that the temporary database was updated.
        print TABS * 3 + 'Testing Case 2...',
        #===========================================================================
        self.assertEqual(date_data, unpacked_date_data)
        self.assertEqual(order_data, unpacked_order_data)
        self.assertEqual(item_data, unpacked_item_data)
        print 'done'

        #============================================================================
        # Generating data for testing Case 3
        #============================================================================
        _populate_non_parseable_random_files(curr_dir)
        update(database=db)

        date_data = unpacked_date_data
        order_data = unpacked_order_data
        item_data = unpacked_item_data

        unpacked_date_data, unpacked_order_data, unpacked_item_data = \
            get_database_table_data(db)

        #============================================================================
        # Case 3: Testing for directory containing non-parsable file names. These
        # filenames should be ignored. Previous data should be
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        self.assertEqual(date_data, unpacked_date_data)
        self.assertEqual(order_data, unpacked_order_data)
        self.assertEqual(item_data, unpacked_item_data,)

        print 'done'

        #============================================================================
        # Generate data for testing case 4
        #============================================================================
        db = ConfirmationSystem._check_and_create_orders_database(':memory:')

        date_data, order_data, item_data = generate_data_files(curr_dir)
        update(database=db)

        unpacked_date_data, unpacked_order_data, unpacked_item_data = \
            get_database_table_data(db)

        #============================================================================
        # Case 4: Testing for directory containing both parsable and non-parasable
        # files. The non-parasable filenames should be ignored but the parsable
        # file names should be parsed and added to the database. As such I expect
        # the new database to contain only that data drawn from the generated
        # order and togo data.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        self.assertEqual(date_data, unpacked_date_data)
        self.assertEqual(order_data, unpacked_order_data)
        self.assertEqual(item_data, unpacked_item_data)
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
        #       Empty Checkout data. Unaffected Dates database.
        #
        #   Case 2:
        #
        #       Requires an adequately populated Orders database for this method to
        #       function. As such Case 1 is that the orders are populated,
        #       and then the date is updated with the correct data.
        #
        #   Case 3:
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
                             '      date(OrderDate)=?;',
                             (curr_date.strftime(SQLITE_DATE_FORMAT_STR),))
            return data.fetchall()

        def get_date_info(db, curr_date):
            c = db.cursor()
            data = c.execute('SELECT '
                             '      * '
                             'FROM '
                             '      DateData '
                             'WHERE '
                             '      Date = ?;',
                             (curr_date.strftime(SQLITE_DATE_FORMAT_STR),))
            return data.fetchall()

        def generate_data(db, n=NUM_OF_CYCLES, num_of_orders=10):
            dates = []

            rand_name = generate_random_names()
            rand_time = generate_random_times()
            rand_item = generate_random_menu_items()

            for x in xrange(n):
                order_time = rand_time.next()

                for y in xrange(num_of_orders):
                    order_name = rand_name.next()
                    order_data = [rand_item.next() for i in xrange(5)]

                    ConfirmationSystem._update_order_table(order_time, order_data,
                                                           order_name, [], [],
                                                           database=db)
                dates.append(order_time)

            return dates

        #============================================================================
        # Generate data for Case 1
        #============================================================================
        dates = generate_data(db)

        #============================================================================
        # Case 1: Testing empty database is.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        for curr_date in dates:
            generated_data = get_order_info(db, curr_date)
            ConfirmationSystem._update_date_table(curr_date, database=db)
            unpacked_data = get_date_info(db, curr_date)

            self.assertEqual(generated_data, unpacked_data)

        print 'done'

        #============================================================================
        # Case 2: Testing database is updated.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        for curr_date in [datetime.now()]:
            ConfirmationSystem._update_date_table(curr_date, database=db)
            unpacked_data = get_date_info(db, curr_date)

            self.assertEqual([], unpacked_data)

        print 'done'

        #============================================================================
        # Generate data for Case 3
        #============================================================================
        values = (MenuItem('should raise an error', 1.0),
                 'antidisestablishmentaranism',
                 42,
                 self)

        #============================================================================
        # Case 3: Testing for appropriate error be raised given non-datetime date
        # object.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for date in values:
            self.assertRaises(StandardError, ConfirmationSystem._update_date_table,
                              date, database=db)

        print 'done'

        #============================================================================
        # Case 4: Testing for appropriate error to be raised given non-sqlite3
        # .connection object for database.
        print TABS * 3 + 'Testing Case 4...',
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
        #       Pass in specific number of MenuItem objects for the order,
        #       expect specific frequency data to be displayed
        #
        # Case 5:
        #
        #       Error raised when non-MenuItem order is passed in as order.
        #
        # Case 6:
        #
        #       Error raised when non-datetime object is passed in as date.
        #
        # Case 7:
        #
        #       Error raised when non-sqlite3.connection object is passed
        #       in as database.
        #============================================================================
        # Generate initial data for testing cases.
        #============================================================================
        curr_dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY

        db = ConfirmationSystem._check_and_create_orders_database(':memory:')


        def get_order_data(db):
            c = db.cursor()
            row_data = c.execute('SELECT '
                                 '     *'
                                 'FROM '
                                 '     OrderData;')
            return row_data.fetchall()

        def generate_and_add_to_orders_database(db, n=GENERATOR_MAX,
                                                num_of_items=10,
                                                notification_data=False,
                                                item_frequency=False):
            rand_name = generate_random_names(n=n)
            rand_time = generate_random_times(n=n)
            rand_item = generate_random_menu_items(n=n)

            counter = _get_current_num_database_rows(db, 'OrderData')

            while counter < n:
                order_name = rand_name.next()
                order_date = rand_time.next()
                order_data = []

                notif_data = []
                item_freq = Counter()
                for x in xrange(num_of_items):
                    item = rand_item.next()

                    order_data.append(item)

                    if notification_data and item.is_notification():
                        notif_data.append(item)

                    if item_frequency:
                        item_freq[item.get_name()] += 1

                subtotal = get_order_subtotal(order_data)
                tax = get_total_tax(subtotal)
                total = get_total(order_data)

                order_standard = True
                order_togo = False

                if TOGO_SEPARATOR in order_name:
                    order_standard = False
                    order_togo = True

                u_data = update(order_date, order_data, order_name, notif_data,
                                item_freq, database=db)

                data = (counter,
                        order_date.strftime(SQLITE_DATE_TIME_FORMAT_STR),
                        order_name,
                        subtotal,
                        tax,
                        total,
                        notification_data,
                        jsonpickle.encode(notif_data),
                        jsonpickle.encode(item_freq),
                        order_standard,
                        order_togo,
                        jsonpickle.encode(order_data))

                self.assertEqual(data, u_data)
                yield data

                counter += 1

            rand_name.close()
            rand_time.close()
            rand_item.close()

        update = ConfirmationSystem._update_order_table

        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        rand_date_update = generate_and_add_to_orders_database(db)
        data = []
        #============================================================================
        # Case 1: Testing general data parsing and storage by the database. Expect
        # for the row to be accurately displayed.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        for x in xrange(NUM_OF_CYCLES):
            updated_data = rand_date_update.next()
            data.append(updated_data)

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
        rand_date_update.close()
        rand_date_update = generate_and_add_to_orders_database(db,
                                                               notification_data=True)

        #============================================================================
        # Case 3: Testing notification data flag and notification data json.
        # Passing in specific notification items. Items are expected to be parsed
        # and displayed accurately in the notifications json file.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for x in xrange(NUM_OF_CYCLES):
            updated_data = rand_date_update.next()

            data.append(updated_data)
            self.assertTrue(len(jsonpickle.decode(updated_data[7])) > 0)
            self.assertEqual(get_order_data(db), data)
        print 'done'

        #============================================================================
        # Generating data for Case 4
        #============================================================================
        rand_date_update.close()
        rand_date_update = generate_and_add_to_orders_database(db,
                                                               item_frequency=True)

        #============================================================================
        # Case 4: Testing order database for accuracy of displayed item frequency.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        for x in xrange(NUM_OF_CYCLES):
            updated_data = rand_date_update.next()

            data.append(updated_data)
            self.assertTrue(len(jsonpickle.encode(updated_data[8])) > 0)
            self.assertEqual(get_order_data(db), data)
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
        # Case 5: Testing for AttributeError raised when given a list of non
        # menuitem objects as order data.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for order_data in values:
            self.assertRaises(StandardError, ConfirmationSystem._update_order_table,
                              datetime.now(), order_data, '', [], [], db)

        print 'done'

        #============================================================================
        # Case 6: Testing for AttributeError raised when given a non datetime
        # object as the order date.
        print TABS * 3 + 'Testing Case 6...',
        #============================================================================
        for date in values:
            self.assertRaises(StandardError, ConfirmationSystem._update_order_table,
                              date, [MenuItem('test', 1.0)], '', [], [], db)

        print 'done'

        #============================================================================
        # Case 7: Testing for AttributeError raised when given a non
        # sqlite3.connection object as the database
        print TABS * 3 + 'Testing Case 7...',
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
        db = ConfirmationSystem._check_and_create_orders_database(':memory:')

        def get_item_data(db):
            c = db.cursor()
            data = c.execute('SELECT '
                             '      * '
                             'FROM '
                             '      ItemData;')
            return data.fetchall()

        def generate_and_add_item_data(db, n=GENERATOR_MAX, is_notification=0.5):
            rand_item = generate_random_menu_items(is_notification=is_notification)
            rand_time = generate_random_times()

            counter = ConfirmationSystem.current_order_counter

            while counter < n:

                item_date = rand_time.next()
                item = rand_item.next()



                u_data = update(item_date, item, database=db)

                data = (counter,
                        item.get_name(),
                        item_date.strftime(SQLITE_DATE_TIME_FORMAT_STR),
                        int(item.is_notification()),
                        jsonpickle.encode(item))

                self.assertEqual(data, u_data)

                yield data

                counter += 1
                ConfirmationSystem.current_order_counter += 1

            rand_item.close()
            rand_time.close()

        update = ConfirmationSystem._update_item_table
        data = []
        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        rand_item = generate_and_add_item_data(db, is_notification=0.0)

        #============================================================================
        # Case 1: Testing the standard Case looking for matching data on a row by
        # row basis. Randomly generated menu item names, times, and prices. Focus
        # is on date, menu item data, and json str.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        for x in xrange(NUM_OF_CYCLES):
            generated_data = rand_item.next()
            data.append(generated_data)

            unpacked_data = get_item_data(db)

            self.assertEqual(data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for test case 2.
        #============================================================================
        rand_item.close()
        rand_item = generate_and_add_item_data(db, is_notification=1.0)

        #============================================================================
        # Case 2: Notification flag case. Testing for notification flag being
        # tripped on data.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        for x in xrange(NUM_OF_CYCLES):
            generated_data = rand_item.next()
            data.append(generated_data)

            unpacked_data = get_item_data(db)

            self.assertEqual(data, unpacked_data)
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
            return data == get_item_data(db)
        #============================================================================
        # Case 3: Testing error raised when a non datetime object is given as date.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        for date in values:
            self.assertRaises(StandardError, update, date, MenuItem('test', 1.0),
                              database=db)

        self.assertTrue(ensure_database_unchanged(db))

        print 'done'

        #============================================================================
        # Case 4: Testing error raised when non menu item object is given as the
        # item.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        for item in values:
            self.assertRaises(StandardError, update, datetime.now(), item,
                              database=db)
        self.assertTrue(ensure_database_unchanged(db))

        print 'done'

        #============================================================================
        # Case 5: Testing error raised when a non sqlite3.connection object is
        # given as database.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for database in values:
            self.assertRaises(StandardError, update, datetime.now(),
                              MenuItem('test', 1.0), database=database)

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
        #       Testing Case 1 but with directory populated by randomly generated
        #       files. Expect identical outcome.
        #
        # Case 4:
        #
        #       Testing Case 2 but with directory populated by randomly generated
        #       files. Expect identical outcome
        #
        # Case 5.
        #
        #       Populated directory. All order names are parse-able.
        #
        # Case 6:
        #
        #       Given non-str order_name expect Error raised.
        #
        # //TODO provide more tests cases to test for data being accurately sent
        # //to print functions.
        #============================================================================
        # Generate initial data for test cases.
        #============================================================================
        curr_dir = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY

        def pull_directory_data(dir):
            data = {}
            dirname, dirpath, filenames = os.walk(dir).next()

            for filename in filenames:
                try:
                    ConfirmationSystem.parse_standardized_file_name(filename)
                    filepath = curr_dir + '/' + filename
                    with open(filepath, 'r') as f:
                        data[filepath] = jsonpickle.decode(f.read())

                except ValueError:
                    pass

            return data

        def generate_file_data(dir):
            data = {}

            rand_order = _generate_random_order()

            for x in xrange(NUM_OF_CYCLES):
                std_name, order_data = rand_order.next()

                p_time, p_name, p_type = \
                    ConfirmationSystem.parse_standardized_file_name(std_name)

                filepath = dir + '/' + std_name

                confirm(p_name, [], order_data, order_data, set_time=p_time)

                data[filepath] = order_data

            return data

        confirm = ConfirmationSystem.order_confirmed
        #============================================================================
        # Generate data for testing Case 1
        #============================================================================
        generated_data = generate_file_data(curr_dir)
        unpacked_data = pull_directory_data(curr_dir)

        #============================================================================
        # Case 1: Testing standard case. Adding unique names/values as files in
        # the directory. Pulling that data and then checking they are identical.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 2
        #============================================================================
        def generate_duplicate_names(dir, prev_data):
            data = {}

            rand_item = generate_random_menu_items()
            for filepath, order_data in prev_data.items():
                new_order_data = order_data + [rand_item.next()]
                _, std_name = filepath.split(dir + '/')

                p_time, p_name, p_type = \
                    ConfirmationSystem.parse_standardized_file_name(std_name)

                curr_time = datetime.now()

                std_name = ConfirmationSystem.standardize_file_name(p_name,
                            set_time=curr_time)

                confirm(p_name, [], new_order_data, new_order_data,
                        set_time=curr_time)

                data[dir + '/' + std_name] = new_order_data

            rand_item.close()
            return data

        generated_data = generate_duplicate_names(curr_dir, generated_data)
        unpacked_data = pull_directory_data(curr_dir)

        #============================================================================
        # Case 2: Testing
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)

        print 'done'

        #============================================================================
        # Generate data for testing Case 3
        #============================================================================
        shutil.rmtree(curr_dir)
        os.mkdir(curr_dir)

        _populate_non_parseable_random_files(curr_dir)
        generated_data = generate_file_data(curr_dir)
        unpacked_data = pull_directory_data(curr_dir)

        #============================================================================
        # Case 3: Testing Case 1 but with directory also containing randomly
        # generated files.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for testing Case 4
        #============================================================================
        generated_data = generate_duplicate_names(curr_dir, generated_data)
        unpacked_data = pull_directory_data(curr_dir)

        #============================================================================
        # Case 4: Testing Case 2 but with directory containing randomly generated
        # files.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generating data for test Case 5
        #============================================================================
        order_names = unpacked_data

        #============================================================================
        # Case 5: Testing that file data has been correctly saved as parseable.
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for order_name in order_names:
            _, name = order_name.split(curr_dir + '/')
            self.assertIsNotNone(ConfirmationSystem.parse_standardized_file_name(name))

        print 'done'

        #============================================================================
        # Generate data for test Case 6
        #============================================================================
        values = (10.0,
                  10,
                  self,
                  ['a', 'b', 'c', 'd'])

        order_data = [MenuItem('test', 1.0)]
        order_name = 'antidisestablishmentaranism'
        priority_order = order_data

        #============================================================================
        # Case 6: Testing error raised when improper order name is given.
        print TABS * 3 + 'Testing Case 6...',
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

        def generate_data(checkout_dir, confirm_dir, n=NUM_OF_CYCLES,
                          save_data=False):
            checkout_data = {}

            rand_order = _generate_random_order(is_checkout=True)
            rand_time = generate_random_times()

            for x in xrange(n):
                std_name, order_data = rand_order.next()

                p_time, p_name, p_type = \
                    ConfirmationSystem.parse_standardized_file_name(std_name)

                if save_data:
                    save_data_to_file(order_data, confirm_dir + '/' + std_name)

                confirm(p_name, (order_data,), order_data, set_time=p_time)

                checkout_data[std_name] = order_data

            return checkout_data

        def pull_file_data(curr_dir):
            data = {}

            dirpath, dirname, filenames = os.walk(curr_dir).next()

            for filename in filenames:

                try:
                    ConfirmationSystem.parse_standardized_file_name(filename)
                    filepath = curr_dir + '/' + filename
                    with open(filepath, 'r') as f:
                        order_data = jsonpickle.decode(f.read())

                    data[filename] = order_data

                except ValueError:
                    pass

            return data

        def pull_all_file_data(curr_dir):
            dirpath, dirname, filenames = os.walk(curr_dir).next()
            return sorted(filenames)

        confirm = ConfirmationSystem.checkout_confirmed
        #============================================================================
        # Generate data for test Case 1
        #============================================================================
        generated_data = generate_data(checkout_dir, confirm_dir)
        unpacked_data = pull_file_data(checkout_dir)

        #============================================================================
        # Case 1: Testing standard care. With empty directories the given orders
        # are added and the files saved as expected.
        print TABS * 3 + 'Testing Case 1...',
        #============================================================================
        self.assertTrue(len(unpacked_data) > 0)
        self.assertEqual(generated_data, unpacked_data)
        print 'done'

        #============================================================================
        # Generate data for test Case 2
        #============================================================================
        non_parsed_data = _populate_non_parseable_random_files(confirm_dir)

        prev_generated_data = generated_data
        generated_data = generate_data(checkout_dir, confirm_dir)
        generated_data.update(prev_generated_data)

        unpacked_data = pull_file_data(checkout_dir)

        unpacked_confirm_data = pull_all_file_data(confirm_dir)


        #============================================================================
        # Case 2: Testing multiple files case. In this case multiple non-parse-able
        # files exist in the confirmed directory, with a list of orders that is to
        # be updated. Each file should be created in their respective area,
        # and the non-parse-able files should be left untouched and intact.
        print TABS * 3 + 'Testing Case 2...',
        #============================================================================
        self.assertEqual(unpacked_data, generated_data)
        self.assertEqual(non_parsed_data, unpacked_confirm_data)
        print 'done'

        #============================================================================
        # Generate data for test Case 3
        #============================================================================
        shutil.rmtree(confirm_dir)
        shutil.rmtree(checkout_dir)
        os.mkdir(confirm_dir)
        os.mkdir(checkout_dir)

        generated_data = generate_data(checkout_dir, confirm_dir, save_data=True)
        unpacked_data = pull_file_data(checkout_dir)

        unpacked_confirm_data = pull_all_file_data(confirm_dir)

        #============================================================================
        # Case 3: Testing confirmed directory contains only parse-able file names.
        # Orders are added that share the same file names are the parse-able files.
        # Expect that all parse-able files (all in the confirmed directory) have
        # been removed and the checkout directory contains the data.
        print TABS * 3 + 'Testing Case 3...',
        #============================================================================
        self.assertEqual(generated_data, unpacked_data)
        self.assertEqual(len(unpacked_confirm_data), 0)

        print 'done'

        #============================================================================
        # Generate data for test Case 4
        #============================================================================
        non_parsed_data = _populate_non_parseable_random_files(confirm_dir)

        prev_generated_data = generated_data
        generated_data = generate_data(checkout_dir, confirm_dir, save_data=True)
        generated_data.update(prev_generated_data)

        unpacked_data = pull_file_data(checkout_dir)

        unpacked_confirm_data = pull_all_file_data(confirm_dir)

        #============================================================================
        # Case 4: Testing confirmed directory contains only non-parse-able file
        # names after it has contained both parseable and non-parseable file names.
        print TABS * 3 + 'Testing Case 4...',
        #============================================================================
        self.assertEqual(generated_data, unpacked_data)
        self.assertEqual(unpacked_confirm_data, non_parsed_data)

        print 'done'


        #============================================================================
        # Generate data for test Case 5
        #============================================================================
        values = (open,
                  10.0,
                  10,
                  self)

        order_data = [MenuItem('testing', 1.0)]

        #============================================================================
        # Case 5: Testing for a non-string given as order name
        print TABS * 3 + 'Testing Case 5...',
        #============================================================================
        for order_name in values:
            self.assertRaises(StandardError, ConfirmationSystem.checkout_confirmed,
                              order_name, (order_data,), order_data)

        print 'done'

        #============================================================================
        print TABS * 2 + 'Finished testing checkout confirmed function'
        #============================================================================
