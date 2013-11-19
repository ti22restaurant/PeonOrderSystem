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
import os
import time
import jsonpickle

jsonpickle.set_encoder_options('simplejson', sort_keys=True, indent=4)

from peonordersystem import path
from peonordersystem import MenuItem
from peonordersystem import CheckOperations


DIRECTORY = path.SYSTEM_ORDERS_PATH

if not os.path.exists(DIRECTORY):
    os.mkdir(DIRECTORY)

current_date = time.localtime()[:3]

CURR_ORDER_DIRECTORY = DIRECTORY

for value in current_date:
    CURR_ORDER_DIRECTORY += '{}/'.format(value)
    
    if not os.path.exists(CURR_ORDER_DIRECTORY):
        os.mkdir(CURR_ORDER_DIRECTORY)

TOGO_SEPARATOR = '::@::'
CHECKOUT_SEPARATOR = '::=::'


def unpack_notification_data(curr_directory=CURR_ORDER_DIRECTORY):
    """Unpacks the information stored
    in the notification data area.

    @param curr_directory: str representing
    the system path of the directory.

    @return: list of MenuItem objects that
    represents the MenuItems that were stored
    in the notification data area.
    """
    curr_directory += 'notification_data.log'

    if os.path.exists(curr_directory):
        file_data = file(curr_directory, 'r')

        data = file_data.read()

        return jsonpickle.decode(data)

    else:
        return []

notification_data = unpack_notification_data()


def update_notification_data(curr_directory=CURR_ORDER_DIRECTORY):
    """Updates the stored notification
    data to display the current updated
    notification data.

    @param curr_directory: str representing
    the directory where the data to be updated
    is located.

    @return: list of notification objects
    that represents the notification data
    saved.
    """
    curr_directory += 'notification_data.log'

    file_data = open(curr_directory, 'w')
    data = jsonpickle.encode(notification_data)

    file_data.write(data)

    return notification_data


def unpack_order_data(curr_directory):
    """Unpacks the information stored in
    the given directory and returns
    that information.

    @param curr_directory: str representing
    the system path of the directory

    @return: 2-tuple of dict types. Each
    dict maps a str key to a list of MenuItem
    objects. Each key represents the name of
    an order and each list represents the
    order.
    """

    table_orders = {}
    togo_orders = {}
    itr = os.walk(curr_directory)

    dirpath, dirnames, filenames = itr.next()

    for curr_filename in filenames:
        filename, filetype = curr_filename.split('.')
        filename = filename.replace('_', ' ')

        if filetype == 'table':
            current_orders = table_orders
        else:
            current_orders = togo_orders

        data = open(dirpath + curr_filename)

        loaded_data = jsonpickle.decode(data.read())

        current_orders[filename] = loaded_data

    return table_orders, togo_orders


def unpack_checkout_data(load_date=current_date):
    """Unpacks the information stored
    in the checkout area, of the date
    designated

    @keyword load_date: tuple of 3 str
    indexes represent (YYYY, MM, DD).
    The given information will be loaded
    from that date.

    @return: dict of key tuples, with
    each index a str. Representing
    (name, time). Mapped to values
    representing a list of MenuItem
    objects that represents the checked
    out order
    """
    checkout_data = {}

    curr_directory = DIRECTORY
    curr_directory += str(load_date[0]) + '/' + str(load_date[1]) +\
                      '/' + str(load_date[2]) + '/'
    curr_directory += 'checkout/'

    itr = os.walk(curr_directory)
    dirpath, dirnames, filenames = itr.next()

    for curr_filename in filenames:

        filename, filetype = curr_filename.split('.')
        filetime, filename = filename.split(CHECKOUT_SEPARATOR)

        separator = None
        if TOGO_SEPARATOR in filename:
            separator = TOGO_SEPARATOR
        else:
            separator = '_'

        filename = filename.replace(separator, ' ')


        data = open(dirpath + curr_filename)
        loaded_data = jsonpickle.decode(data.read())

        key = (filename, filetime + ', ' + str(current_date[1]) +
                         '/' + str(current_date[2]))

        checkout_data[key] = loaded_data

    return checkout_data


def add_notification_item(menu_item):
    """Adds a notification to the
    notification data

    @param menu_item: MenuItem object
    that is to be added to the notification
    data.

    @return: None
    """
    notification_data.append(menu_item)


def generate_files():
    """Generates the necessary confirmed and
    checkout files. If those files already exist
    in the parent directory than this function
    returns information regarding those for loading
    purposes.
    
    @return: 2-tuple. Each entry is a dict, where the
    first entry represents the table orders and the
    second entry represents the togo orders. Each
    dict has a key that maps to a list of the MenuItem
    objects that were present in that order.
    """
    curr_directory = CURR_ORDER_DIRECTORY + 'confirmed/'
    
    if not os.path.exists(curr_directory):
        os.mkdir(curr_directory)
        os.mkdir(CURR_ORDER_DIRECTORY + 'checkout/')
        print CURR_ORDER_DIRECTORY + 'checkout/'
    else:
        return unpack_order_data(curr_directory)

    return {}, {}


def standardize_confirm_file_name(order_name):
    """Standardizes the name of the file,
    under the standard format for confirmed
    orders

    @param order_name: str representing the name
    of the order.

    @return: str representing the standardized
    file format.
    """
    order_name = order_name.replace('.', '_')
    order_name = order_name.replace(' ', '_')
    
    if TOGO_SEPARATOR in order_name:
        order_name += '.togo'
    else:
        order_name += '.table'
    
    return order_name


def standardize_checkout_file_name(order_name):
    """Standardizes the name of the file,
    under the standard format for checked out
    orders.

    @param order_name: str representing the orders
    name.

    @return: str representing the standard form for
    check out files.
    """
    order_name = order_name.replace(' ', '_')
    curr_time = time.strftime('%H-%M-%S')
    return curr_time + CHECKOUT_SEPARATOR + order_name + '.checkout'


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
    print_order(order_name, non_priority_list,
                priority_list=priority_list)

    curr_directory = CURR_ORDER_DIRECTORY + 'confirmed/'
    order_name = standardize_confirm_file_name(order_name)
    
    curr_file = open(curr_directory + order_name, 'w')

    obj_info = jsonpickle.encode(full_order)
    curr_file.write(obj_info)


def remove_order_confirmed_file(order_name):
    """Removes the file associated with the
    confirmed order from the necessary
    directory.

    @param order_name: str representing the name
    associated with the given order. The given name
    will be transformed into the standarized format.
    """
    curr_directory = CURR_ORDER_DIRECTORY + 'confirmed/'
    order_name = standardize_confirm_file_name(order_name)

    f_name = curr_directory + order_name

    if os.path.isfile(f_name):
        os.remove(curr_directory + order_name)


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
    remove_order_confirmed_file(order_name)

    curr_directory = CURR_ORDER_DIRECTORY + 'checkout/'
    order_name = standardize_checkout_file_name(order_name)
    curr_file = open(curr_directory + order_name, 'w')
    obj_info = jsonpickle.encode(order_list)
    curr_file.write(obj_info)

    for order in orders:
        print_check(order_name, order)


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
    pass


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

    # to add to notification log
    for menu_item in order_list:

        if menu_item.is_comped() or \
                isinstance(menu_item, MenuItem.DiscountItem):
            add_notification_item(menu_item)
