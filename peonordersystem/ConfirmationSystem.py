'''This module provides functionality for the confirmation system.
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
'''
import os
import cPickle
import time

from peonordersystem import path
from peonordersystem import MenuItem


directory = path.SYSTEM_ORDERS_PATH

if not os.path.exists(directory):
    os.mkdir(directory)

current_date = time.localtime()[:3]

for value in current_date:
    directory = directory + '{}/'.format(value)
    
    if not os.path.exists(directory):
        os.mkdir(directory)

TOGO_SEPARATOR = '::@::'


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
    table_orders = {}
    togo_orders = {}
    
    curr_directory = directory + 'confirmed/'
    
    if not os.path.exists(curr_directory):
        os.mkdir(curr_directory)
        os.mkdir(directory + 'checkout/')
    else:
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
            unpickler = cPickle.Unpickler(data)
            current_orders[filename] = unpickler.load()
                
    return (table_orders, togo_orders)

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
        order_name = order_name + '.togo'
    else:
        order_name = order_name + '.table'
    
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
    return order_name + '_' + curr_time + '.checkout'

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
    # TODO send priority_list, order_list to kitchen

    curr_directory = directory + 'confirmed/'
    order_name = standardize_confirm_file_name(order_name)
    
    curr_file = open(curr_directory + order_name, 'w')
    
    cPickle.dump(full_order, curr_file)

def remove_order_confirmed_file(order_name):
    """Removes the file associated with the
    confirmed order from the necessary
    directory.

    @param order_name: str representing the name
    associated with the given order. The given name
    will be transformed into the standarized format.
    """
    curr_directory = directory + 'confirmed/'
    order_name = standardize_confirm_file_name(order_name)
    
    os.remove(curr_directory + order_name)
    
def checkout_confirmed(order_name, order_list):
    """Generates the necessary checkout files
    and adds the given order to that file for
    storage. This is utilized later.

    @param order_name: str representing the name
    associated with the given order.

    @param order_list: list of MenuItem objects
    that represents the current order.
    """
    # TODO send order_list to checkout printer

    remove_order_confirmed_file(order_name)
    
    curr_directory = directory + 'checkout/'
    order_name = standardize_checkout_file_name(order_name)
    curr_file = open(curr_directory + order_name, 'w')
    
    cPickle.dump(order_list, curr_file)
    