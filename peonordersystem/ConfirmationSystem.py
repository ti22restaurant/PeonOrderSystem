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


directory = path.SYSTEM_ORDERS_PATH

current_date = time.localtime()[:3]

for value in current_date:
    directory = directory + '{}/'.format(value)
    
    if not os.path.exists(directory):
        os.mkdir(directory)



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
    
    @return: str representing the standardized
    file format.
    """
    
    if 'table_' in order_name and len(order_name) < 9:
        order_name = order_name + '.table'
    else:
        order_name = order_name + '.togo'
    
    return order_name

def standardize_checkout_file_name(order_name):
    """Standardizes the name of the file,
    under the standard format for checked out
    orders.
    """
    curr_time = time.strftime('%H-%M-%S')
    return order_name + '_' + curr_time + '.checkout'

def order_confirmed(order_name, order_list):
    """Confirms an order by dumping a binary
    file representing the confirmed order into
    the parent directories confirmed folder.
    """
    curr_directory = directory + '/confirmed/'
    order_name = standardize_confirm_file_name(order_name)
    
    curr_file = open(curr_directory + order_name, 'w')
    
    cPickle.dump(order_list, curr_file)

def remove_order_confirmed_file(order_name):
    """Removes the file associated with the
    confirmed order from the necessary
    directory.
    """
    curr_directory = directory + '/confirmed/'
    order_name = standardize_confirm_file_name(order_name)
    
    os.remove(curr_directory + order_name)
    
def checkout_confirmed(order_name, order_list):
    """Generates the necessary checkout files
    and adds the given order to that file for
    storage. This is utilized later.
    """
    remove_order_confirmed_file(order_name)
    
    curr_directory = directory + '/checkout/'
    
    order_name = standardize_checkout_file_name(order_name)
    
    curr_file = open(curr_directory + order_name, 'w')
    
    cPickle.dump(order_list, curr_file)
    