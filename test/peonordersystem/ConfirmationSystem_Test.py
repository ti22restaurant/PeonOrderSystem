"""

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""

import os
import time
import shutil
import random
import string
import sqlite3
import unittest
import jsonpickle


from src.peonordersystem import path
from src.peonordersystem.Settings import (TOGO_SEPARATOR,
                                          TYPE_SUFFIX_CHECKOUT,
                                          TYPE_SUFFIX_STANDARD_ORDER,
                                          DATE_DATA_COLS,
                                          ORDER_DATA_COLS,
                                          ITEM_DATA_COLS,
                                          RESERVATIONS_DATA_COLS)
from src.peonordersystem.MenuItem import MenuItem

TABS = '    '


class ConfirmationSystemTest(unittest.TestCase):
    """

    """
    @classmethod
    def setUpClass(cls):
        """

        @param cls:
        @return:
        """
        print TABS + 'BEGIN: Testing ConfirmationSystem module'
        print TABS * 2 + 'Testing database generation'

        print TABS * 3 + 'Clearing database data...',
        shutil.rmtree(path.SYSTEM_DATABASE_PATH)
        shutil.rmtree(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY)
        shutil.rmtree(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY)
        print 'done'

        from src.peonordersystem import ConfirmationSystem
        cls.ConfirmationSystem = ConfirmationSystem

        print TABS * 3 + 'Checking for database generation...',
        assert(os.path.exists(path.SYSTEM_DATABASE_PATH) is True)
        print 'done'

        print TABS * 3 + 'Checking for Checkout and Confirmed directories...',
        assert(os.path.exists(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY) is True)
        assert(os.path.exists(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY) is True)
        print 'done'

        print TABS * 2 + 'Finished testing database generation'

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

    def tearDown(self):
        """Override Method

        Used to tear down the ConfirmationSystem test cases.

        @return: None
        """
        if os.path.exists(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY):
            shutil.rmtree(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY)
        if os.path.exists(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY):
            shutil.rmtree(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY)

    @classmethod
    def tearDownClass(cls):
        """

        @param cls:
        @return:
        """
        if not os.path.exists(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY):
            os.mkdir(path.SYSTEM_ORDERS_CHECKOUT_DIRECTORY)
        if not os.path.exists(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY):
            os.mkdir(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY)

    def test_standardize_and_parse_standardized_file_name_functions(self):
        """Test the standardize and parse standardized file
        name functions.

        @return: None
        """
        print TABS * 2 + 'Testing standardize and parse name functions'
        # Checking the extreme cases for potentially bad
        # filenames. This includes a standard normaly file
        # name. File names with known keyword characters used
        # by the system and empty file names.
        #
        # All names when parsed are returned in the format of
        # a tuple with (float, str, str) as their format representing
        # the number of seconds since epoch for date & time, the name
        # of the order and the filetype respectively.
        #
        #   Case 1:
        #       Test general standardize/parse with multiple different strs
        #       some of which contain characters that may conflict.
        #
        #   Case 2:
        #       Test standardize/parse with specific time.
        #
        #   Case 3:
        #       Test standardize/parse with specific bool value given.
        #============================================================================
        # Generate initial data to test
        #============================================================================
        std_file_name = self.ConfirmationSystem.standardize_file_name
        prs_std_file_name = self.ConfirmationSystem.parse_standardized_file_name
        order_names = ['my_test_order',
                       'my_test' + TOGO_SEPARATOR + '_order',
                       '[my_test_order]',
                       '/my/test/order',
                       'my.test.order',
                       '   /  .   [ ] [ / . ']

        names = [''.join(random.sample(string.printable, 100)) for x in xrange(100)]

        #============================================================================
        # Nest test cases from here on in
        #============================================================================
        for order_name in order_names + names:

            #========================================================================
            # Generating Case 1 data: Testing for standard file name.
            #========================================================================
            standardized_name1 = std_file_name(order_name)
            standardized_name2 = std_file_name(order_name)

            fst_parsed_name1 = prs_std_file_name(standardized_name1)
            fst_parsed_name2 = prs_std_file_name(standardized_name2)

            #========================================================================
            # Testing Case 1 data: Testing for standard file name
            #========================================================================

            self.assertEqual(standardized_name1, standardized_name2)
            self.assertEqual(fst_parsed_name1, fst_parsed_name2)

            order_times = (time.time(),
                           time.time() + 1000,
                           time.time() - 1000)

            for order_time in order_times:

                #====================================================================
                # Generate Case 2 data: Testing for standard file name with
                # specific order time
                #====================================================================
                standardized_name_time1 = std_file_name(order_name,
                                                        set_time=order_time)
                standardized_name_time2 = std_file_name(order_name,
                                                        set_time=order_time)

                scnd_parsed_name1 = prs_std_file_name(standardized_name_time1)
                scnd_parsed_name2 = prs_std_file_name(standardized_name_time2)

                #====================================================================
                # Testing case 2: Checking against stored data and previous data.
                #====================================================================
                self.assertEqual(standardized_name_time1, standardized_name_time2)

                self.assertEqual(scnd_parsed_name1, scnd_parsed_name2)
                self.assertEqual(scnd_parsed_name1[1], fst_parsed_name1[1])
                self.assertEqual(scnd_parsed_name2[1], fst_parsed_name2[1])
                self.assertEqual(int(order_time), int(scnd_parsed_name1[0]))

                is_checkouts = (
                    (False, TYPE_SUFFIX_STANDARD_ORDER),
                    (True, TYPE_SUFFIX_CHECKOUT))

                for is_checkout, type_suffix in is_checkouts:

                    #================================================================
                    # Generate case 3: Generate data for case 3
                    #================================================================

                    standardized_name_checkout1 = std_file_name(order_name,
                        is_checkout=is_checkout)
                    standardized_name_checkout2 = std_file_name(order_name,
                        is_checkout=is_checkout)

                    #================================================================
                    # Testing case 3: Testing for specific file bool against
                    # previous file data.
                    #================================================================

                    self.assertEqual(standardized_name_checkout1,
                                     standardized_name_checkout2)

                    thd_parsed_name1 = prs_std_file_name(
                        standardized_name_checkout1)
                    thd_parsed_name2 = prs_std_file_name(
                        standardized_name_checkout2)

                    self.assertEqual(thd_parsed_name1, thd_parsed_name2)
                    self.assertEqual(fst_parsed_name1[1], thd_parsed_name1[1])
                    self.assertEqual(thd_parsed_name1[2], type_suffix)

        print TABS * 2 + 'Finished testing standardize and parse name functions'

    def test_orders_database_creation_functions(self):
        """Tests the functions that are used to generate the
        orders database and its subsequent tables.

        @return: None
        """
        print TABS * 2 + 'Testing database creation functions'
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
        database = self.ConfirmationSystem._check_and_create_orders_database(
            ':memory:')
        cursor = database.cursor()

        schema_data = (('ItemData', ITEM_DATA_COLS),
                       ('OrderData', ORDER_DATA_COLS),
                       ('DateData', DATE_DATA_COLS))

        #============================================================================
        # Case 1: Testing that schema matches with loaded schema data for tables.
        #============================================================================
        print TABS * 3 + 'Testing case 1...',

        for table_name, schema in schema_data:

            values = cursor.execute('PRAGMA table_info({});'.format(table_name))

            for entries in values:
                self.assertTrue(entries[1] in schema)
                self.assertEqual(entries[2], schema[entries[1]])
        print 'done'

        print TABS * 2 + 'Finished testing database creation functions'

    def test_reservations_database_creation_function(self):
        """Tests the generation of the reservations database
        and its subsequent table.

        @return: None
        """
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
        database = self.ConfirmationSystem._check_and_create_reservations_database(
            ':memory:')
        cursor = database.cursor()

        #============================================================================
        # Case 1: Test that schema appropriately is in place in database table.
        #============================================================================
        values = cursor.execute('PRAGMA table_info(ReservationsData);')
        schema_data = RESERVATIONS_DATA_COLS

        for entries in values:
            self.assertTrue(entries[1] in schema_data)
            self.assertEqual(entries[2], schema_data[entries[1]])

    def test_load_data_function(self):
        """Tests the function that loads data from
        a given file.

        @return: None
        """
        print TABS * 2 + 'Beginning testing load data function'
        # Testing the function will have the following
        # cases:
        #
        #   Case 1:
        #
        #   several files that are known to exist. Expect
        #   to receive the same data as using jsonpickle
        #   on the file myself.
        #
        #   Case 2:
        #
        #   several files that are known not to exist. Expect
        #   to receive IOError error.
        #============================================================================
        # Generate initial data for comparison.
        #============================================================================
        file_paths = {}

        for i in range(10):
            file_path = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY + '/' + str(i)

            file_paths[file_path] = [MenuItem(str(x), x) for x in range(10)]

            data_str = jsonpickle.encode(file_paths[file_path])

            with open(file_path, 'w') as curr_file:
                curr_file.write(data_str)

        #============================================================================
        # Case 1: Checking that data loads properly
        #============================================================================
        print TABS * 3 + 'Testing Case 1...',
        for file_path in file_paths:

            data = self.ConfirmationSystem._load_data(file_path)
            self.assertEqual(data, file_paths[file_path])
            os.remove(file_path)
        print 'done'

        #============================================================================
        # Case 2: Checking that data doesn't load and raises IOError instead.
        #============================================================================
        print TABS * 3 + 'Testing Case 2...',
        for file_path in file_paths:
            self.assertRaises(IOError, self.ConfirmationSystem._load_data,
                              file_path)
        print 'done'

        print TABS * 2 + 'Finished testing load data function'

    def test_find_order_name_paths_function(self):
        """Tests the function that is used to search for
        file paths of the given name.

        @return: None
        """
        print TABS * 2 + 'Beginning testing find order name paths function'
        # Testing cases here should check that the correct file
        # has been identified. There will be three possible cases
        # for this:
        #
        #   Case 1: Unique names
        #
        #      This case should test whether the function is
        #      able to retrieve files associated with specific
        #      unique names.
        #
        #   Case 2: Similar names
        #
        #       This case should test whether the function is
        #       able to retrieve files associated with unique,
        #       but similar names.
        #
        #   Case 3: Identical names
        #
        #       This testing case will most certainly fail. The
        #       system cannot decide between near identical names.
        #       As such near identical names (those that only differ
        #       in regards to their time/date stamp) are discouraged
        #       and steps should be taken to prevent users from providing
        #       identical names and utilizing this function.
        #
        #       However Case 3 may still be tested. The function itself
        #       returns a list of paths. It will be considered a success
        #       if the ideal path is contained within the paths that were
        #       returned.
        #============================================================================
        # Generate filler so a comparison can be made
        #============================================================================
        for x in range(50):
            name = str(random.randint(0, 1000)) + str(x)
            name = self.ConfirmationSystem.standardize_file_name(name)

            with open(path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY + '/' + name, 'w') as \
                curr_file:
                curr_file.write(name)

        #============================================================================
        # Generate Case 1: Distinct, unique names.
        #===========================================================================
        file_paths = {}

        for x in range(10):
            name = str(x)
            file_name = self.ConfirmationSystem.standardize_file_name(name)
            file_paths[str(x)] = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY + '/' +\
                                    file_name

            with open(file_paths[name], 'w') as curr_file:
                curr_file.write(file_name)

        #============================================================================
        # Case 1: All values returned should be exactly the correct path.
        #============================================================================
        print TABS * 3 + 'Testing Case 1...',
        for order_name in file_paths:
            results = self.ConfirmationSystem._find_order_name_paths(order_name,
                         path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY)

            for result in results:
                self.assertEqual(result, file_paths[order_name])
        print 'done'

        #============================================================================
        # Generate Case 2: Similar, but unique names.
        #============================================================================
        file_paths = {}

        for x in range(10):
            name = str(x) + '_'
            file_name = self.ConfirmationSystem.standardize_file_name(name)
            file_paths[name] = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY + '/' + \
                               file_name

            with open(file_paths[name], 'w') as curr_file:
                curr_file.write(file_name)

        #============================================================================
        # Case 2: All values returned should be exactly the correct path.
        #============================================================================
        print TABS * 3 + 'Testing Case 2...',
        for order_name in file_paths:
            results = self.ConfirmationSystem._find_order_name_paths(order_name,
                        path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY)

            for result in results:
                self.assertEqual(result, file_paths[order_name])
        print 'done'

        #============================================================================
        # Generate Case 3: Identical, non-unique names.
        #============================================================================
        file_paths = {}

        for x in range(10):
            name = str(x)
            file_name = self.ConfirmationSystem.standardize_file_name(name)
            file_paths[name] = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY + '/' +\
                                    file_name
            with open(file_paths[name], 'w') as curr_file:
                curr_file.write(file_name)

        #============================================================================
        # Case 3: Expect some values returned to contain the appropriate file
        # paths, but not all.
        #============================================================================
        print TABS * 3 + 'Testing Case 3...',
        for order_name in file_paths:
            results = self.ConfirmationSystem._find_order_name_paths(order_name,
                        path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY)

            self.assertTrue(file_paths[order_name] in results)
        print 'done'

        print TABS * 2 + 'Finished testing find order paths names function'

    def test_unpack_order_data_function(self):
        """Tests the unpack order data function
        if it is operating appropriately.

        @return: None
        """
        print TABS * 2 + 'Testing unpack order data function'
        # Testing the unpack order data function requires
        # both testing for standard table orders and togo
        # orders. Thus we have two cases Since this
        # function relies on the load data function we
        # can guarantee its success at retrieving the data,
        # with the only requirement being that we are pulling
        # the correct data, with the correct names, and correct
        # labels.
        #
        #   Case 1:
        #
        #       Standard table order data that is pulled. Needs to
        #       be checked for accurate name, and date/times. Also that
        #       all available data has been pulled.
        #
        #   Case 2:
        #
        #       Much like case one, only pertaining directly to togo orders.
        #       There should be very little difference between the two cases.

        initial_order_data = {}
        initial_togo_data = {}

        #===========================================================================
        # This block generates data to be assessed.
        #===========================================================================
        for x in range(10):
            # Generate data for Case 1
            name = str(x)
            file_name = self.ConfirmationSystem.standardize_file_name(name)
            file_path = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY + '/' + file_name

            key = self.ConfirmationSystem.parse_standardized_file_name(file_name)
            initial_order_data[(key[1], key[0])] = (file_path,)

            with open(file_path, 'w') as data_file:
                data = jsonpickle.encode((file_path,))
                data_file.write(data)

            # Generate data for Case 2
            name = str(x) + TOGO_SEPARATOR + str(x * 2)
            file_name = self.ConfirmationSystem.standardize_file_name(name)
            file_path = path.SYSTEM_ORDERS_CONFIRMED_DIRECTORY + '/' + file_name

            key = self.ConfirmationSystem.parse_standardized_file_name(file_name,
                    togo_separator=TOGO_SEPARATOR)
            initial_togo_data[(key[1], key[0])] = (file_path,)

            with open(file_path, 'w') as data_file:
                data = jsonpickle.encode((file_path,))
                data_file.write(data)

        order_data, togo_data = self.ConfirmationSystem.unpack_order_data()

        #============================================================================
        # Testing Case 1
        #============================================================================
        print TABS * 3 + 'Testing order data unpack...',
        self.assertEqual(order_data, initial_order_data)
        print 'done'

        #============================================================================
        # Testing Case 2
        #============================================================================
        print TABS * 3 + 'Testing togo data unpack...',
        self.assertEqual(togo_data, initial_togo_data)
        print 'done'

        print TABS * 2 + 'Finished testing unpack order data function'

if __name__ == "__main__":
    unittest.main()
