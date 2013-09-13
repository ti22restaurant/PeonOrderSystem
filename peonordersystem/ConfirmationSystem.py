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

def order_confirmed(order_name, order_list):
    """Confirms an order by dumping a binary
    file representing the confirmed order into
    the parent directories confirmed folder.
    """
    curr_directory = directory + '/confirmed/'
    
    if 'table_' in order_name and len(order_name) < 9:
        order_name = order_name + '.table'
    else:
        order_name = order_name + '.togo'
    
    curr_file = open(curr_directory + order_name, 'w')
    
    cPickle.dump(order_list, curr_file)
            
                